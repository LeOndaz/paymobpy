from typing import List, Optional
from uuid import uuid4

from pydantic import BaseModel, root_validator, validator


class AuthResponse(BaseModel):
    token: str


class Address(BaseModel):
    apartment: str
    email: str
    floor: str
    first_name: str
    last_name: str
    street: str
    building: str
    phone_number: str
    postal_code: str
    city: str
    country: str
    state: str


class ShippingData(Address):
    extra_description: str


class ShippingDetails(BaseModel):
    number_of_packages: int
    contents: str
    notes: str
    weight: int
    weight_unit: str
    length: int
    width: int
    height: int


class OrderLine(BaseModel):
    name: str
    amount_cents: str
    description: str
    quantity: str


class CreateOrderRequest(BaseModel):
    delivery_needed: Optional[bool] = False
    amount_cents: str
    currency: str
    merchant_order_id: Optional[str]
    items: List[OrderLine]

    # TODO 1: shipping_data should be optional,
    #  but a bug in paymob API makes it required even when delivery_needed is False
    shipping_data: ShippingData
    shipping_details: Optional[ShippingDetails]

    @validator("merchant_order_id", always=True)
    def validate_merchant_order_id(cls, value):
        if value is None:
            return str(uuid4())

        return value

    @validator("currency")
    def validate_currency(cls, value):
        assert value in ("EGP", "USD"), "Unsupported currency"
        return value

    @root_validator()
    def validate_needs_shipping(cls, values):
        if values.get("delivery_needed"):
            # TODO 2: The first check is useless, it depends on TODO: 1
            assert (
                "shipping_data" in values
            ), "You must provide shipping_data when delivery_needed=True"
            assert (
                "shipping_details" in values
            ), "You must provide shipping_details when delivery_needed=True"

        return values


class CreateOrderResponse(BaseModel):
    id: int
    token: str
    url: str
    order_url: str
    delivery_fees_cents: int
    delivery_vat_cents: int
    commission_fees: int
    notify_user_with_email: bool
    paid_amount_cents: bool
    is_payment_locked: bool
    is_return: bool
    is_cancel: bool
    is_returned: bool
    is_canceled: bool
    merchant_order_id: str


class CreatePaymentKeyRequest(BaseModel):
    expiration: int
    billing_data: Address
    integration_id: int


class CreatePaymentKeyResponse(BaseModel):
    token: str
