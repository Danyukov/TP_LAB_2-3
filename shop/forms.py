from django import forms


class PromoCodeForm(forms.Form):
    code = forms.CharField(
        required=False,
        max_length=32,
        label="Промокод",
    )
