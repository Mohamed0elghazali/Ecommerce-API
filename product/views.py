from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product

# Create your views here.

@api_view(["GET"])
def get_all_products(request):
    products = Product.objects.all()
    print(products)
    return Response(
        {"products": "Put Products Here",}
    )