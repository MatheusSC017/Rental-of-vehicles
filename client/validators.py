from django.core.validators import BaseValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from validate_docbr import CPF, CNH
import re


class CPFValidator(BaseValidator):
    message = _('The CPF entered is invalid.')
    code = 'cpf_validator'

    def __call__(self, value):
        cleaned = self.clean(value)
        cpf = CPF()

        if not cpf.validate(cleaned):
            raise ValidationError(self.message, code=self.code)

    def clean(self, x):
        return re.sub('[^0-9]', '', x)


class CNHValidator(BaseValidator):
    message = _('The CNH entered is invalid.')
    code = 'cnh_validator'

    def __call__(self, value):
        cleaned = self.clean(value)
        cnh = CNH()

        if not cnh.validate(cleaned):
            raise ValidationError(self.message, code=self.code)

    def clean(self, x):
        return re.sub('[^0-9]', '', x)
