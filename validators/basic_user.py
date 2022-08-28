from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
import re


@deconstructible
class PhoneValidator:
    message = 'Telefone inválido, favor informar um telefone no formato (12) 3 4567-8901'
    code = 'phone_validator'

    def __call__(self, value):
        search = re.findall('^\(?[0-9]{2}\)? ?9? ?[0-9]{4}[ -]?[0-9]{4}$', value)

        if not search:
            raise ValidationError(self.message, code=self.code)
