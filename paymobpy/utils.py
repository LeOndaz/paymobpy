from pydantic import ValidationError

from paymobpy.logger import logger


def pretty_print(e: ValidationError):
    errors = []

    for error in e.errors():
        fields = error['loc']
        err_type = error['type']

        if err_type == "value_error.missing":
            errors.append({
                "fields": fields,
                "type": "MISSING"
            })

    logger.error(errors)