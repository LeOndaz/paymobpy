import asyncio
import json
from uuid import uuid4

import httpx
from paymobpy.exceptions import PaymobError
from paymobpy.http_clients import PaymobClient
from paymobpy.schemas import AuthResponse, CreateOrderResponse, CreateOrderRequest

API_KEY = """
ZXlKaGJHY2lPaUpJVXpVeE1pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SnVZVzFsSWpvaWFXNXBkR2xoYkNJc0ltTnNZWE56SWpvaVRXVnlZMmhoYm5RaUxDSndjbTltYVd4bFgzQnJJam94TnpFM056bDkuX2hxcEp2Q1F0NFFpeWNDUXozYS1abGQ4dHhpeTI2QnBFS0ZuWC1HRmxIRldIalJ6OFEtVzBoa0RVaDEyaTk1RW9CRmMtZ0V6bmhDVUZXMVlqVzBCVWc=
"""


class URLs:
    BASE_URL = "https://accept.paymob.com/api"
    AUTH = "/auth/tokens"
    CREATE_ORDER = "/ecommerce/orders"


class Paymob:
    api_calls = 0

    def __init__(self, api_key):
        self.api_key = api_key

        self._client = PaymobClient(base_url=URLs.BASE_URL)
        self._token = None

    async def authenticate(self) -> str:
        response = await self._client.post(URLs.AUTH, json=dict(api_key=self.api_key))

        try:
            response = response.json()
        except json.JSONDecodeError as e:
            raise PaymobError('Response is not valid json:\n {}', str(e))

        response = AuthResponse(**response)
        self._token = response.token
        return response.token

    async def create_order(self, data) -> CreateOrderResponse:
        self.api_calls += 1

        data = CreateOrderRequest(**data)

        response = await self._client.post(URLs.CREATE_ORDER, json={
            "auth_token": self._token,
            **data.dict(),
        })

        try:
            response = response.json()
        except json.JSONDecodeError as e:
            raise PaymobError('Response is not valid json:\n {}', str(e))

        if response.get('message') == "duplicate":
            raise PaymobError("Order with merchant_order_id={id} already exists.".format(
                id=data.merchant_order_id
            ))

        return CreateOrderResponse(**response)


async def main():
    paymob = Paymob(api_key=API_KEY)

    await paymob.authenticate()
    order = await paymob.create_order(data={
        "delivery_needed": False,
        "amount_cents": 500,
        "currency": "EGP",
        "items": [
            dict(name="Item 3", amount_cents=200, description="Item 1 desc", quantity=1),
            dict(name="Item 4", amount_cents=300, description="Item 1 desc", quantity=1),
        ],
        "shipping_data": {
            "apartment": "803",
            "email": "claudette09@exa.com",
            "floor": "42",
            "first_name": "Clifford",
            "street": "Ethan Land",
            "building": "8028",
            "phone_number": "+86(8)9135210487",
            "postal_code": "01898",
            "extra_description": "8 Ram , 128 Giga",
            "city": "Jaskolskiburgh",
            "country": "CR",
            "last_name": "Nicolas",
            "state": "Utah"
        }
    })

    print(paymob.api_calls)
    print(order)


asyncio.run(main())
