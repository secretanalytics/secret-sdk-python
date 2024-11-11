from __future__ import annotations
from functools import reduce
from typing import Dict, List, Optional

from secret_sdk.core.msg import Msg
from secret_sdk.core import AccAddress, Coins, Numeric
from secret_sdk.core.tx import Tx
from secret_sdk.core.bank import MsgSend, MsgMultiSend
from secret_sdk.key.key import Key, SignOptions
from secret_sdk.client.lcd.api.tx import CreateTxOptions, SignerOptions
from secret_sdk.protobuf.cosmos.tx.v1beta1 import BroadcastMode

__all__ = ["Wallet", "AsyncWallet"]


class AsyncWallet:
    def __init__(self, lcd, key: Key):
        self.lcd = lcd
        self.key = key

    async def account_number(self) -> int:
        res = await self.lcd.auth.account_info(self.key.acc_address)
        return res.account_number

    async def sequence(self) -> int:
        res = await self.lcd.auth.account_info(self.key.acc_address)
        return res.sequence

    async def account_number_and_sequence(self) -> dict:
        res = await self.lcd.auth.account_info(self.key.acc_address)
        return {"account_number": res.account_number, "sequence": res.sequence}

    async def create_tx(self, options: CreateTxOptions) -> Tx:
        sigOpt = [
            SignerOptions(
                address=self.key.acc_address,
                sequence=options.sequence,
                public_key=self.key.public_key,
            )
        ]
        return await self.lcd.tx.create(sigOpt, options)

    async def create_and_sign_tx(self, options: CreateTxOptions) -> Tx:
        account_number = options.account_number
        sequence = options.sequence
        if account_number is None or sequence is None:
            res = await self.account_number_and_sequence()
            if account_number is None:
                account_number = res.get("account_number")
            if sequence is None:
                sequence = res.get("sequence")
        options.sequence = sequence
        options.account_number = account_number
        return self.key.sign_tx(
            tx=(await self.create_tx(options)),
            options=SignOptions(
                account_number=account_number,
                sequence=sequence,
                chain_id=self.lcd.chain_id
            )
        )

    async def execute_tx(
        self,
        contract_addr: str,
        handle_msg: Dict,
        memo: str = "",
        transfer_amount: Coins = None,
        gas: Optional[int] = None,
        gas_prices: Optional[Coins.Input] = None,
        gas_adjustment: Optional[Numeric.Input] = None,
        fee_denoms: Optional[List[str]] = None,
        broadcast_mode: Optional[BroadcastMode] = None
    ):
        execute_msg = await self.lcd.wasm.contract_execute_msg(
            self.key.acc_address, contract_addr, handle_msg, transfer_amount
        )
        if gas is None:
            gas = self.lcd.custom_fees["exec"].gas_limit
        return await self.create_and_broadcast_tx(
            [execute_msg], memo, gas, gas_prices, gas_adjustment, fee_denoms, broadcast_mode
        )

    async def multi_execute_tx(
            self,
            input_msgs: List[Dict],
            memo: str = "",
            gas: Optional[int] = None,
            gas_prices: Optional[Coins.Input] = None,
            gas_adjustment: Optional[Numeric.Input] = None,
            fee_denoms: Optional[List[str]] = None,
            broadcast_mode: Optional[BroadcastMode] = None
    ):
        msgs = []
        for input_msg in input_msgs:
            # input_msg should be a Dict with contract_addr and handle_msg keys
            contract_addr = input_msg['contract_addr']
            handle_msg = input_msg['handle_msg']
            transfer_amount = input_msg.get('transfer_amount', Coins())
            execute_msg = await self.lcd.wasm.contract_execute_msg(self.key.acc_address, contract_addr, handle_msg,
                                                                   transfer_amount)
            msgs.append(execute_msg)
        if gas is None:
            gas = self.lcd.custom_fees["exec"].gas_limit * len(input_msgs)
        return await self.create_and_broadcast_tx(
            msgs, memo, gas, gas_prices, gas_adjustment, fee_denoms, broadcast_mode
        )

    async def send_tokens(
        self,
        recipient_addr: AccAddress,
        memo: str = "",
        transfer_amount: Coins = None,
        gas: Optional[int] = None,
        gas_prices: Optional[Coins.Input] = None,
        gas_adjustment: Optional[Numeric.Input] = None,
        fee_denoms: Optional[List[str]] = None,
        broadcast_mode: Optional[BroadcastMode] = None
    ):
        send_msg = MsgSend(self.key.acc_address, recipient_addr, transfer_amount)
        if gas is None:
            gas = self.lcd.custom_fees["send"].gas_limit

        return await self.create_and_broadcast_tx([send_msg], memo, gas, gas_prices, gas_adjustment, fee_denoms, broadcast_mode)

    async def multi_send_tokens(
        self,
        recipient_addrs: List[AccAddress],
        memo: str = "",
        transfer_amounts: List[Coins] = None,
        gas: Optional[int] = None,
        gas_prices: Optional[Coins.Input] = None,
        gas_adjustment: Optional[Numeric.Input] = None,
        fee_denoms: Optional[List[str]] = None,
        broadcast_mode: Optional[BroadcastMode] = None

    ):
        inputs = [
            {
                'address': self.key.acc_address,
                'coins': reduce(lambda x, y: x + y, transfer_amounts),
            },
        ]
        outputs = [{
            'address': recipient_addr,
            'coins': transfer_amount,
        } for recipient_addr, transfer_amount in zip(recipient_addrs, transfer_amounts)]

        multi_send_msg = MsgMultiSend(inputs, outputs)
        if gas is None:
            gas = self.lcd.custom_fees["send"].gas_limit

        return await self.create_and_broadcast_tx([multi_send_msg], memo, gas, gas_prices, gas_adjustment, fee_denoms,
                                            broadcast_mode)

    async def create_and_broadcast_tx(
            self,
            msg_list: List[Msg],
            memo: str = "",
            gas: Optional[int] = None,
            gas_prices: Optional[Coins.Input] = None,
            gas_adjustment: Optional[Numeric.Input] = None,
            fee_denoms: Optional[List[str]] = None,
            broadcast_mode: Optional[BroadcastMode] = None
    ):
        create_tx_options = CreateTxOptions(
            msgs=msg_list,
            memo=memo,
            gas=str(gas),
            gas_prices=gas_prices,
            gas_adjustment=gas_adjustment or self.lcd.gas_adjustment,
            fee_denoms=fee_denoms
        )

        if gas is None:
            fee = self.lcd.tx.estimate_fee(create_tx_options)
            create_tx_options.fee = fee

        signed_tx = await self.create_and_sign_tx(create_tx_options)
        broadcast_mode = broadcast_mode if broadcast_mode else BroadcastMode.BROADCAST_MODE_SYNC
        tx = await self.lcd.tx.broadcast_adapter(signed_tx, mode=broadcast_mode)
        return tx


class Wallet:
    """Wraps around a :class:`Key` implementation and provides transaction building and
    signing functionality. It is recommended to create this object through
    :meth:`LCDClient.wallet()<secret_sdk.client.lcd.LCDClient.wallet>`."""

    def __init__(self, lcd, key: Key):
        self.lcd = lcd
        self.key = key

    def account_number(self) -> int:
        """Fetches account number for the account associated with the Key."""
        res = self.lcd.auth.account_info(self.key.acc_address)
        return res.account_number

    def sequence(self) -> int:
        """Fetches the sequence number for the account associated with the Key."""
        res = self.lcd.auth.account_info(self.key.acc_address)
        return res.sequence

    def account_number_and_sequence(self) -> dict:
        """Fetches both account and sequence number associated with the Key."""
        res = self.lcd.auth.account_info(self.key.acc_address)
        return {"account_number": res.account_number, "sequence": res.sequence}

    def create_tx(self, options: CreateTxOptions) -> Tx:
        """Builds an unsigned transaction object. The ``Wallet`` will first
        query the blockchain to fetch the latest ``account`` and ``sequence`` values for the
        account corresponding to its Key, unless the they are both provided. If no ``fee``
        parameter is set, automatic fee estimation will be used (see `fee_estimation`).

        Args:
            options (CreateTxOptions): Options to create a tx

        Returns:
            Tx: unsigned transaction
        """
        sigOpt = [
            SignerOptions(
                address=self.key.acc_address,
                sequence=options.sequence,
                public_key=self.key.public_key,
            )
        ]
        return self.lcd.tx.create(sigOpt, options)

    def create_and_sign_tx(self, options: CreateTxOptions) -> Tx:
        """Creates and signs a :class:`Tx` object in a single step. This is the recommended
        method for preparing transaction for immediate signing and broadcastring. The transaction
        is generated exactly as :meth:`create_tx`.

        Args:
            options (CreateTxOptions): Options to create a tx

        Returns:
            Tx: signed transaction
        """

        account_number = options.account_number
        sequence = options.sequence
        if account_number is None or sequence is None:
            res = self.account_number_and_sequence()
            if account_number is None:
                account_number = res.get("account_number")
            if sequence is None:
                sequence = res.get("sequence")
        options.sequence = sequence
        options.account_number = account_number
        return self.key.sign_tx(
            tx=self.create_tx(options),
            options=SignOptions(
                account_number=account_number,
                sequence=sequence,
                chain_id=self.lcd.chain_id,
            )
        )

    def execute_tx(
            self,
            contract_addr: str,
            handle_msg: Dict,
            memo: str = "",
            transfer_amount: Coins = None,
            gas: Optional[int] = None,
            gas_prices: Optional[Coins.Input] = None,
            gas_adjustment: Optional[Numeric.Input] = None,
            fee_denoms: Optional[List[str]] = None,
            broadcast_mode: Optional[BroadcastMode] = None
    ):

        execute_msg = self.lcd.wasm.contract_execute_msg(
            self.key.acc_address, contract_addr, handle_msg, transfer_amount
        )
        if gas is None:
            gas = self.lcd.custom_fees["exec"].gas_limit
        return self.create_and_broadcast_tx(
            [execute_msg], memo, gas, gas_prices, gas_adjustment, fee_denoms, broadcast_mode
        )

    def multi_execute_tx(
            self,
            input_msgs: List[Dict],
            memo: str = "",
            gas: Optional[int] = None,
            gas_prices: Optional[Coins.Input] = None,
            gas_adjustment: Optional[Numeric.Input] = None,
            fee_denoms: Optional[List[str]] = None,
            broadcast_mode: Optional[BroadcastMode] = None
    ):
        msgs = []
        for input_msg in input_msgs:
            # input_msg should be a Dict with contract_addr and handle_msg keys
            contract_addr = input_msg['contract_addr']
            handle_msg = input_msg['handle_msg']
            transfer_amount = input_msg.get('transfer_amount', Coins())
            execute_msg = self.lcd.wasm.contract_execute_msg(self.key.acc_address, contract_addr, handle_msg,
                                                                   transfer_amount)
            msgs.append(execute_msg)
        if gas is None:
            gas = self.lcd.custom_fees["exec"].gas_limit * len(input_msgs)
        return self.create_and_broadcast_tx(
            msgs, memo, gas, gas_prices, gas_adjustment, fee_denoms, broadcast_mode
        )

    def send_tokens(
        self,
        recipient_addr: AccAddress,
        memo: str = "",
        transfer_amount: Coins = None,
        gas: Optional[int] = None,
        gas_prices: Optional[Coins.Input] = None,
        gas_adjustment: Optional[Numeric.Input] = None,
        fee_denoms: Optional[List[str]] = None,
        broadcast_mode: Optional[BroadcastMode] = None

    ):
        send_msg = MsgSend(self.key.acc_address, recipient_addr, transfer_amount)
        if gas is None:
            gas = self.lcd.custom_fees["send"].gas_limit

        return self.create_and_broadcast_tx([send_msg], memo, gas, gas_prices, gas_adjustment, fee_denoms,
                                            broadcast_mode)

    def multi_send_tokens(
        self,
        recipient_addrs: List[AccAddress],
        memo: str = "",
        transfer_amounts: List[Coins] = None,
        gas: Optional[int] = None,
        gas_prices: Optional[Coins.Input] = None,
        gas_adjustment: Optional[Numeric.Input] = None,
        fee_denoms: Optional[List[str]] = None,
        broadcast_mode: Optional[BroadcastMode] = None

    ):
        inputs = [
            {
                'address': self.key.acc_address,
                'coins': reduce(lambda x, y: x + y, transfer_amounts),
            },
        ]
        outputs = [{
            'address': recipient_addr,
            'coins': transfer_amount,
        } for recipient_addr, transfer_amount in zip(recipient_addrs, transfer_amounts)]

        multi_send_msg = MsgMultiSend(inputs, outputs)
        if gas is None:
            gas = self.lcd.custom_fees["send"].gas_limit

        return self.create_and_broadcast_tx([multi_send_msg], memo, gas, gas_prices, gas_adjustment, fee_denoms,
                                            broadcast_mode)

    def create_and_broadcast_tx(
            self,
            msg_list: List[Msg],
            memo: str = "",
            gas: Optional[int] = None,
            gas_prices: Optional[Coins.Input] = None,
            gas_adjustment: Optional[Numeric.Input] = None,
            fee_denoms: Optional[List[str]] = None,
            broadcast_mode: Optional[BroadcastMode] = None
    ):
        create_tx_options = CreateTxOptions(
            msgs=msg_list,
            memo=memo,
            gas=str(gas),
            gas_prices=gas_prices,
            gas_adjustment=gas_adjustment or self.lcd.gas_adjustment,
            fee_denoms=fee_denoms
        )

        if gas is None:
            fee = self.lcd.tx.estimate_fee(create_tx_options)
            create_tx_options.fee = fee

        signed_tx = self.create_and_sign_tx(create_tx_options)
        broadcast_mode = broadcast_mode if broadcast_mode else BroadcastMode.BROADCAST_MODE_SYNC
        tx = self.lcd.tx.broadcast_adapter(signed_tx, mode=broadcast_mode)
        return tx

