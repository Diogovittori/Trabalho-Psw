from django import forms


class DateInput(forms.DateInput):
    input_type = "date"

    def __init__(self, attrs=None):
        # O HTML date exige ISO, mesmo com LANGUAGE_CODE='pt-br'.
        super().__init__(attrs=attrs, format="%Y-%m-%d")
