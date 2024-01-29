from django.shortcuts import get_object_or_404, render

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product
from .serializers import ProductSerializer
from .fitlers import ProductFiter

# Create your views here.

@api_view(["GET"])
def get_all_products(request):
    products = Product.objects.all()
    print(products)
    serializer = ProductSerializer(products, many=True)
    print(serializer.data)
    return Response(
        {"products": serializer.data}
    )
 
@api_view(["GET"])
def get_product(request, pk):
    # product = Product.objects.get(pk=pk)
    product = get_object_or_404(Product, id=pk)
    serializer = ProductSerializer(product, many=False)
    return Response(
        {"Product": serializer.data}
    )

@api_view(["GET"])
def get_by_filter(request):
    filterset = ProductFiter(request.GET, queryset=Product.objects.all())
    serializer = ProductSerializer(filterset.qs, many=True)
    return Response(
        {"products": serializer.data}
    )