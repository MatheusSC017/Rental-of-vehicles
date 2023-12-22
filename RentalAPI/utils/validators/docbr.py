import re
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _
from validate_docbr import CPF, CNH, RENAVAM


@deconstructible
class DocValidator:
    def __call__(self, value):
        cleaned = self.clean(value)

        if not self.doc_validator.validate(cleaned):
            raise ValidationError(self.message, code=self.code)

    @staticmethod
    def clean(x):
        return re.sub('[^0-9]', '', x)


@deconstructible
class CPFValidator(DocValidator):
    message = _('The CPF entered is invalid.')
    code = 'cpf_validator'
    doc_validator = CPF()


@deconstructible
class CNHValidator(DocValidator):
    message = _('The CNH entered is invalid.')
    code = 'cnh_validator'
    doc_validator = CNH()


@deconstructible
class RENAVAMValidator(DocValidator):
    message = _('The Renavam entered is invalid')
    code = 'renavam_validator'
    doc_validator = RENAVAM()
