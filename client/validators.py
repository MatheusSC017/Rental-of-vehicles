from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.deconstruct import deconstructible
from validate_docbr import CPF, CNH
import re


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
    message = 'O CPF informado é inválido.'
    code = 'cpf_validator'
    doc_validator = CPF()


@deconstructible
class CNHValidator(DocValidator):
    message = 'A CNH informada é inválida.'
    code = 'cnh_validator'
    doc_validator = CNH()
