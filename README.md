A client library for [Paymob API](https://docs.paymob.com/docs/)

To intsall:

```bash
pip install paymobpy
```

### Usage

```python
import confik
from paymobpy import Paymob
import asyncio

API_KEY = confik.get("PAYMOB_API_KEY")


async def main():
    async with Paymob(api_key=API_KEY) as paymob:
        order = await paymob.create_order(data={})  # put order data here
        payment = await paymob.pay(500, 'EGP', order.id, 'INTEGRATION_ID', data={})


if __name__ == "__main__":
    asyncio.run(main())
```

order.data is a dict implementing the interface paymobpy.schemas.CreateOrderRequest
payment.data is a dict implementing the interface paymobpy.schemas.CreatePaymentKeyRequest

The library has type hints and any linter will work perfectly (thanks to pydantic).
