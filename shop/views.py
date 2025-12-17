from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import CreateView

from .models import Product, Purchase, PromoCode
from .forms import PromoCodeForm


def index(request):
    form = PromoCodeForm(request.GET)
    discount_percent = 0
    promo_error = ""

    if form.is_valid():
        code = form.cleaned_data.get("code")  # уже upper и проверен
        if code:
            promo = PromoCode.objects.get(code=code, is_active=True)
            discount_percent = promo.discount_percent
    else:
        promo_error = form.errors.get("code", [""])[0]

    products = []
    for p in Product.objects.all():
        discounted_price = None
        if discount_percent:
            discounted_price = float(p.price) * (100 - discount_percent) / 100

        products.append({
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "discounted_price": discounted_price,
        })

    return render(
        request,
        "shop/index.html",
        {
            "products": products,
            "promo_form": form,
            "discount_percent": discount_percent,
            "promo_error": promo_error,
        },
    )


class PurchaseCreate(CreateView):
    model = Purchase
    fields = ["product", "person", "address"]

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponse(f"Спасибо за покупку, {self.object.person}!")
