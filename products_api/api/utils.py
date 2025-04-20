from django.db import models


def remove_leading_zeros(code):
    if code[0] != "0":
        return code
    else:
        return remove_leading_zeros(code[1:])


class NoLeadingZerosCharField(models.CharField):
    """
    This is used to remove any leading zeros from a string field
    """

    def __init__(self, *args, **kwargs):
        super(NoLeadingZerosCharField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        return remove_leading_zeros(value)
