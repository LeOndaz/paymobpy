import pytest

from paymobpy import CreateOrderResponse, Paymob

fake_shipping_data = {
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
}

items = [
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
]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "delivery_needed, currency, shipping_data",
    [
        (True, "EGP", fake_shipping_data),
        (False, "EGP", fake_shipping_data),
        (True, "USD", fake_shipping_data),
        (False, "USD", fake_shipping_data),
    ],
)
async def test_create_order(paymob, delivery_needed, currency, shipping_data):
    order = await paymob.create_order(
        data={
            "delivery_needed": delivery_needed,
            "amount_cents": 500,
            "currency": currency,
            "shipping_data": shipping_data,
            "items": items,
        }
    )

    return order.id


@pytest.mark.xfail
@pytest.mark.asyncio
async def test_create_order_without_shipping_with_delivery(paymob):
    order = await paymob.create_order(
        data={
            "items": items,
            "currency": "EGP",
            "shipping_data": {},
            "delivery_needed": True,
        }
    )


@pytest.mark.asyncio
async def test_create_payment(
    paymob: Paymob, order_with_delivery_needed: CreateOrderResponse
):
    payment = await paymob.pay(
        500,
        "EGP",
        order_with_delivery_needed.id,
        2020230,
        data={
            "billing_data": {
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
            "expiration": 3600,
            "lock_order_when_paid": False,
        },
    )
