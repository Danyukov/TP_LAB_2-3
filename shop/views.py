from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import CreateView

from .models import Product, Purchase
from .forms import PromoCodeForm

PROMO_CODES = {
    "TOYS5": 5,
    "TOYS10": 10,
    "TOYS15": 15,
}


def index(request):
    products = Product.objects.all()

    form = PromoCodeForm(request.GET)
    discount_percent = 0

    if form.is_valid():
        code = (form.cleaned_data.get("code") or "").strip().upper()
        discount_percent = PROMO_CODES.get(code, 0)

    context = {
        "products": products,
        "promo_form": form,
        "discount_percent": discount_percent,
    }
    return render(request, "shop/index.html", context)


class PurchaseCreate(CreateView):
    model = Purchase
    fields = ["product", "person", "address"]

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponse(f"Спасибо за покупку, {self.object.person}!")
