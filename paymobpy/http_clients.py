import json

from httpx import AsyncClient, Response

from paymobpy import PaymobError


class PaymobClient(AsyncClient):
    async def request(self, *args, **kwargs) -> Response:
        response: Response = await super().request(*args, **kwargs)

        if response.status_code == 401:
            raise PaymobError(
                "Unauthorized, did you forget to call authenticate() on your paymob instance?",
                response=response,
            )

        try:
            response.json()
        except json.JSONDecodeError as e:
            raise PaymobError(
                "API responded with non valid json, check your DNS settings {}".format(
                    str(e)
                ),
                response=response,
                wrapped_exception=e,
            )

        return response
