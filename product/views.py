from django.shortcuts import get_object_or_404, render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
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

@api_view(["GET"])
def get_by_page(request):
    filterset = ProductFiter(request.GET, queryset=Product.objects.all())
    count = filterset.qs.count()
    
    resPage = 2
    paginator = PageNumberPagination()
    paginator.page_size = resPage

    queryset = paginator.paginate_queryset(filterset.qs, request)
    serializer = ProductSerializer(queryset, many=True)
    return Response(
        {"Product": serializer.data, "Per Page": resPage, "Count": count}
    )