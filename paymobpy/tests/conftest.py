import confik
import pytest_asyncio

from paymobpy import Paymob

API_KEY = confik.get("PAYMOB_API_KEY")


def get_order_data(items=True, shipping=True, delivery_needed=False):
    data = {
        "delivery_needed": delivery_needed,
    }

    if shipping:
        data = {
            **data,
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
                "state": "Utah",
            },
        }

    if items:
        data = {
            **data,
            "items": [
                dict(
                    name="Item 3",
                    amount_cents=200,
                    description="Item 1 desc",
                    quantity=1,
                ),
                dict(
                    name="Item 4",
                    amount_cents=300,
                    description="Item 1 desc",
                    quantity=1,
                ),
            ],
        }

    return data


@pytest_asyncio.fixture()
async def paymob():
    instance = Paymob(api_key=API_KEY)
    await instance.authenticate()
    return instance


@pytest_asyncio.fixture()
async def order_with_delivery_needed(paymob):
    return await paymob.create_order(
        data={
            "amount_cents": 500,
            "currency": "EGP",
            **get_order_data(True, True, True),
        }
    )


@pytest_asyncio.fixture()
async def order_without_delivery_needed(paymob: Paymob):
    return await paymob.create_order(
        data={
            "delivery_needed": False,
            "amount_cents": 500,
            "currency": "EGP",
            **get_order_data(True, True, False),
        }
    )


@pytest_asyncio.fixture()
async def order_without_shipping_with_delivery_needed(paymob: Paymob):
    return await paymob.create_order(
        data={
            "amount_cents": 500,
            "currency": "EGP",
            **get_order_data(True, False, True),
        }
    )


@pytest_asyncio.fixture()
async def order_without_data(paymob: Paymob):
    return await paymob.create_order(data={})
