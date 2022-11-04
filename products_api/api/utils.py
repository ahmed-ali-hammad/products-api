from django.db import models


class NoLeadingZerosCharField(models.CharField):
    """
    This is used to remove any leading zeros from a string field
    """
    def __init__(self, *args, **kwargs):
        super(NoLeadingZerosCharField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        if value[0] != '0':
            return value
        else:
            self.get_prep_value(value[1:])
