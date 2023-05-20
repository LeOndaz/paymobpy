from typing import Mapping

from paymobpy.consts import URLs
from paymobpy.exceptions import PaymobError
from paymobpy.http_clients import PaymobClient
from paymobpy.schemas import (
    AuthResponse,
    CreateOrderRequest,
    CreateOrderResponse,
    CreatePaymentKeyRequest,
    CreatePaymentKeyResponse,
)


class Paymob:
    def __init__(self, api_key):
        self.api_key = api_key

        self._client = PaymobClient(base_url=URLs.BASE_URL)
        self._token = None

    @property
    def auth_token(self):
        if self._token:
            return self._token

        raise PaymobError("No token found, did you forget to call .authenticate() ?")

    async def authenticate(self) -> str:
        response = await self._client.post(URLs.AUTH, json=dict(api_key=self.api_key))
        response = response.json()
        response = AuthResponse(**response)
        self._token = response.token
        return response.token

    async def create_order(self, data: Mapping) -> CreateOrderResponse:
        data = CreateOrderRequest(**data)

        response = await self._client.post(
            URLs.CREATE_ORDER,
            json={
                "auth_token": self.auth_token,
                **data.dict(),
            },
        )

        response = response.json()

        if response.get("message") == "duplicate":
            raise PaymobError(
                "Order with merchant_order_id={id} already exists.".format(
                    id=data.merchant_order_id
                )
            )

        return CreateOrderResponse(**response)

    async def request_payment(
        self,
        cents: int,
        currency: str,
        order_id: int,
        integration_id: int,
        data: Mapping,
    ) -> CreatePaymentKeyResponse:
        data = CreatePaymentKeyRequest(**data)

        response = await self._client.post(
            URLs.REQUEST_PAYMENT_KEY,
            json={
                "auth_token": self.auth_token,
                "order_id": order_id,
                "amount_cents": str(cents),
                "currency": currency,
                "lock_order_when_paid": False,
                "integration_id": integration_id,
                **data.dict(),
            },
        )

        return response.json()

    async def close_connection(self):
        await self._client.aclose()

    async def __aenter__(self):
        await self.authenticate()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close_connection()
