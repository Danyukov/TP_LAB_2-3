from django import forms
from .models import PromoCode


class PromoCodeForm(forms.Form):
    code = forms.CharField(required=False, max_length=32, label="Промокод")

    def clean_code(self):
        code = (self.cleaned_data.get("code") or "").strip().upper()
        if not code:
            return ""

        if not PromoCode.objects.filter(code=code, is_active=True).exists():
            raise forms.ValidationError("Промокод не найден или не активен.")

        return code
