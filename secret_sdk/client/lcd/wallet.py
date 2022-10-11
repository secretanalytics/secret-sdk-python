from __future__ import annotations

from typing import Dict, List, Optional

from secret_sdk.core import AccAddress, Coins, Numeric
from secret_sdk.core.tx import Tx
from secret_sdk.core.bank import MsgSend
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
            ),
            encryption_utils=self.lcd.encrypt_utils
        )

    async def execute_tx(
        self,
        contract_addr: str,
        handle_msg: List[Dict],
        memo: str = "",
        transfer_amount: Coins = None,
        gas: Optional[int] = None,
        gas_prices: Optional[Coins.Input] = None,
        gas_adjustment: Optional[Numeric.Input] = None,
        fee_denoms: Optional[List[str]] = None,
        broadcast_mode: Optional[BroadcastMode] = None
    ):

        msg_list = []
        for msg in handle_msg:
            execute_msg = await self.lcd.wasm.contract_execute_msg(
                self.key.acc_address, contract_addr, msg, transfer_amount
            )
            msg_list.append(execute_msg)

        create_tx_options = CreateTxOptions(
            msgs=msg_list,
            memo=memo,
            gas=str(gas),
            gas_prices=gas_prices,
            gas_adjustment=gas_adjustment,
            fee_denoms=fee_denoms
        )

        if gas is None or gas_prices is None:
            fee = self.lcd.custom_fees["exec"]
            create_tx_options.fee=fee

        signed_tx = await self.create_and_sign_tx(create_tx_options)
        broadcast_mode = broadcast_mode if broadcast_mode else BroadcastMode.BROADCAST_MODE_BLOCK
        tx = await self.lcd.tx.broadcast_adapter(signed_tx, mode = broadcast_mode)
        return tx

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
        create_tx_options = CreateTxOptions(
            msgs=[send_msg],
            memo=memo,
            gas=str(gas),
            gas_prices=gas_prices,
            gas_adjustment=gas_adjustment,
            fee_denoms=fee_denoms
        )

        if gas is None or gas_prices is None:
            fee = self.lcd.custom_fees["send"]
            create_tx_options.fee = fee

        signed_tx = await self.create_and_sign_tx(create_tx_options)
        broadcast_mode = broadcast_mode if broadcast_mode else BroadcastMode.BROADCAST_MODE_BLOCK
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
            ),
            encryption_utils=self.lcd.encrypt_utils
        )

    def execute_tx(
        self,
        contract_addr: str,
        handle_msg: List[Dict],
        memo: str = "",
        transfer_amount: Coins = None,
        gas: Optional[int] = None,
        gas_prices: Optional[Coins.Input] = None,
        gas_adjustment: Optional[Numeric.Input] = None,
        fee_denoms: Optional[List[str]] = None,
        broadcast_mode: Optional[BroadcastMode] = None

    ):
        msg_list = []
        for msg in handle_msg:
            execute_msg = self.lcd.wasm.contract_execute_msg(
                self.key.acc_address, contract_addr, msg, transfer_amount
            )
            msg_list.append(execute_msg)

        create_tx_options = CreateTxOptions(
            msgs=msg_list,
            memo=memo,
            gas=str(gas),
            gas_prices=gas_prices,
            gas_adjustment=gas_adjustment or 0,
            fee_denoms=fee_denoms
        )

        if gas is None or gas_prices is None:
            fee = self.lcd.custom_fees["exec"]
            create_tx_options.fee = fee

        signed_tx = self.create_and_sign_tx(create_tx_options)
        broadcast_mode = broadcast_mode if broadcast_mode else BroadcastMode.BROADCAST_MODE_BLOCK
        tx = self.lcd.tx.broadcast_adapter(signed_tx, mode=broadcast_mode)
        return tx

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
        create_tx_options = CreateTxOptions(
            msgs=[send_msg],
            memo=memo,
            gas=str(gas),
            gas_prices=gas_prices,
            gas_adjustment=gas_adjustment,
            fee_denoms=fee_denoms
        )

        if gas is None or gas_prices is None:
            fee = self.lcd.custom_fees["send"]
            create_tx_options.fee = fee

        signed_tx = self.create_and_sign_tx(create_tx_options)
        broadcast_mode = broadcast_mode if broadcast_mode else BroadcastMode.BROADCAST_MODE_BLOCK
        tx = self.lcd.tx.broadcast_adapter(signed_tx, mode=broadcast_mode)
        return tx
