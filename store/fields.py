from rest_framework.fields import DateTimeField

class CustomDateTimeField(DateTimeField):
    def __init__(self, format="%a, %d %b %Y %H:%M:%S", **kwargs):
        super().__init__(format=format, **kwargs)
