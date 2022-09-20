from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _
import re


@deconstructible
class PhoneValidator:
    message = _('Invalid phone number, please enter a phone number in the format (XX) X XXXX-XXXX')
    code = 'phone_validator'

    def __call__(self, value):
        search = re.findall('^\(?[0-9]{2}\)? ?9? ?[0-9]{4}[ -]?[0-9]{4}$', value)

        if not search:
            raise ValidationError(self.message, code=self.code)
