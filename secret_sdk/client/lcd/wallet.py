from __future__ import annotations

from typing import List, Optional, Dict

from secret_sdk.core import Coins, Numeric
from secret_sdk.core.auth import StdFee, StdSignMsg, StdTx
from secret_sdk.core.msg import Msg
from secret_sdk.key.key import Key

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

    async def create_tx(self, *args, **kwargs) -> StdSignMsg:
        return await self.lcd.tx.create(self.key.acc_address, *args, **kwargs)

    async def create_and_sign_tx(self, *args, **kwargs) -> StdTx:
        tx = await self.create_tx(*args, **kwargs)
        return self.key.sign_tx(tx)

    async def execute_tx(self, handle_msg: Dict, contract_addr: str, transfer_amount: Coins = None, memo: str = "",
                         gas_price: float = 0.25, gas_cost: int = 500_000) -> StdTx:
        #TODO figure out where we want to move this, generate fee in a smarter way, decrypt the final tx
        fee = StdFee(gas_cost, Coins.from_data([{"amount": int(gas_cost * gas_price), "denom": "uscrt"}]))
        execute_msg = await self.lcd.wasm.contract_execute_msg(self.key.acc_address, contract_addr, handle_msg,
                                                                 transfer_amount)
        signed_tx = await self.create_and_sign_tx([execute_msg], fee=fee, memo = memo)
        tx = await self.lcd.tx.broadcast(signed_tx)
        return tx

    async def multi_execute_tx(self, input_msgs: List[Dict], memo: str = "", gas_price: float = 0.25, gas_cost: int = 500_000):
        fee = StdFee(gas_cost, Coins.from_data([{"amount": int(gas_cost * gas_price), "denom": "uscrt"}]))
        msgs = []
        for input_msg in input_msgs:
            # input_msg should be a Dict with contract_addr and handle_msg keys
            contract_addr = input_msg['contract_addr']
            handle_msg = input_msg['handle_msg']
            transfer_amount = input_msg.get('transfer_amount', Coins())
            execute_msg = await self.lcd.wasm.contract_execute_msg(self.key.acc_address, contract_addr, handle_msg,
                                                                   transfer_amount)
            msgs.append(execute_msg)
        signed_tx = await self.create_and_sign_tx(msgs, fee=fee, memo=memo)
        tx = await self.lcd.tx.broadcast(signed_tx)
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

    def create_tx(
        self,
        msgs: List[Msg],
        fee: Optional[StdFee] = None,
        memo: str = "",
        gas_prices: Optional[Coins.Input] = None,
        gas_adjustment: Optional[Numeric.Input] = None,
        fee_denoms: Optional[List[str]] = None,
        account_number: Optional[int] = None,
        sequence: Optional[int] = None,
    ) -> StdSignMsg:
        """Builds an unsigned transaction object. The ``Wallet`` will first
        query the blockchain to fetch the latest ``account`` and ``sequence`` values for the
        account corresponding to its Key, unless the they are both provided. If no ``fee``
        parameter is set, automatic fee estimation will be used (see `fee_estimation`).

        Args:
            msgs (List[Msg]): list of messages to include
            fee (Optional[StdFee], optional): transaction fee. If ``None``, will be estimated.
                See more on `fee estimation`_.
            memo (str, optional): optional short string to include with transaction.
            gas_prices (Optional[Coins.Input], optional): gas prices for fee estimation.
            gas_adjustment (Optional[Numeric.Input], optional): gas adjustment for fee estimation.
            fee_denoms (Optional[List[str]], optional): list of denoms to use for fee after estimation.
            account_number (Optional[int], optional): account number (overrides blockchain query if
                provided)
            sequence (Optional[int], optional): sequence (overrides blockchain qu ery if provided)

        Returns:
            StdSignMsg: unsigned transaction
        """
        return self.lcd.tx.create(
            sender=self.key.acc_address,
            msgs=msgs,
            fee=fee,
            memo=memo,
            gas=None,
            gas_prices=gas_prices,
            gas_adjustment=gas_adjustment,
            fee_denoms=fee_denoms,
            account_number=account_number,
            sequence=sequence,
        )

    def create_and_sign_tx(
        self,
        msgs: List[Msg],
        fee: Optional[StdFee] = None,
        memo: str = "",
        gas_prices: Optional[Coins.Input] = None,
        gas_adjustment: Optional[Numeric.Input] = None,
        fee_denoms: Optional[List[str]] = None,
        account_number: Optional[int] = None,
        sequence: Optional[int] = None,
    ) -> StdTx:
        """Creates and signs a :class:`StdTx` object in a single step. This is the recommended
        method for preparing transaction for immediate signing and broadcastring. The transaction
        is generated exactly as :meth:`create_tx`.

        Args:
            msgs (List[Msg]): list of messages to include
            fee (Optional[StdFee], optional): transaction fee. If ``None``, will be estimated.
                See more on `fee estimation`_.
            memo (str, optional): optional short string to include with transaction.
            gas_prices (Optional[Coins.Input], optional): gas prices for fee estimation.
            gas_adjustment (Optional[Numeric.Input], optional): gas adjustment for fee estimation.
            fee_denoms (Optional[List[str]], optional): list of denoms to use for fee after estimation.
            account_number (Optional[int], optional): account number (overrides blockchain query if
                provided)
            sequence (Optional[int], optional): sequence (overrides blockchain qu ery if provided)

        Returns:
            StdTx: signed transaction
        """
        return self.key.sign_tx(
            self.create_tx(
                msgs,
                fee,
                memo,
                gas_prices,
                gas_adjustment,
                fee_denoms,
                account_number,
                sequence,
            )
        )

    def execute_tx(self, handle_msg: Dict, contract_addr: str, transfer_amount: Coins = None, memo: str = "",
                         gas_price: float = 0.25, gas_cost: int = 150_000) -> StdTx:
        #TODO figure out where we want to move this, generate fee in a smarter way, decrypt the final tx
        fee = StdFee(gas_cost, Coins.from_data([{"amount": int(gas_cost * gas_price), "denom": "uscrt"}]))
        execute_msg = self.lcd.wasm.contract_execute_msg(self.key.acc_address, contract_addr, handle_msg,
                                                                 transfer_amount)
        signed_tx = self.create_and_sign_tx([execute_msg], fee=fee, memo = memo)
        tx = self.lcd.tx.broadcast(signed_tx)
        return tx

    def multi_execute_tx(self, input_msgs: List[Dict], memo: str = "", gas_price: float = 0.25, gas_cost: int = 150_000):
        fee = StdFee(gas_cost, Coins.from_data([{"amount": int(gas_cost * gas_price), "denom": "uscrt"}]))
        msgs = []
        for input_msg in input_msgs:
            # input_msg should be a Dict with contract_addr and handle_msg keys
            contract_addr = input_msg['contract_addr']
            handle_msg = input_msg['handle_msg']
            transfer_amount = input_msg.get('transfer_amount', Coins())
            execute_msg = self.lcd.wasm.contract_execute_msg(self.key.acc_address, contract_addr, handle_msg,
                                                                   transfer_amount)
            msgs.append(execute_msg)
        signed_tx = self.create_and_sign_tx(msgs, fee=fee, memo=memo)
        tx = self.lcd.tx.broadcast(signed_tx)
        return tx