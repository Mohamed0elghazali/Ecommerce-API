from django.shortcuts import get_object_or_404, render
from django.db.models import Avg

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from .models import Product, Review
from .serializers import ProductSerializer, ReviewSerializer
from .fitlers import ProductFiter

# Create your views here.

@api_view(["GET"])
def get_all_products(request):
    products = Product.objects.all()
    # print(products)
    serializer = ProductSerializer(products, many=True)
    # print(serializer.data)
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


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def new_product(request):
    data = request.data
    serializer = ProductSerializer(data=data)
    if serializer.is_valid():
        product = Product.objects.create(**data, user=request.user)
        res = ProductSerializer(product, many=False)

        return Response({"Product": res.data})
    else:
        return Response({"Product": serializer.errors})


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_product(request, pk):
    product = Product.objects.get(pk=pk)
    if product.user != request.user:
        return Response({"error": "Sorry You Can`t update this product"},
                        status=status.HTTP_403_FORBIDDEN)

    product.name = request.data["name"]
    product.description = request.data["description"]
    product.price = request.data["price"]
    product.brand = request.data["brand"]
    product.category = request.data["category"]
    product.ratings = request.data["ratings"]
    product.stock = request.data["stock"]
    product.save()
  
    serializer = ProductSerializer(product, many=False)
    return Response({"product": serializer.data})

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_product(request, pk):
    product = Product.objects.get(pk=pk)
    if product.user != request.user:
        return Response({"error": "Sorry You Can`t delete this product"},
                        status=status.HTTP_403_FORBIDDEN)
    product.delete()
    return Response({"details": "product deleted successfully"},
                    status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_review(request, pk):
    user = request.user
    product = Product.objects.get(pk=pk)
    data = request.data
    # get the product and user
    review = product.reviews.filter(user=user)

    # check if a previous review exist from the same user on same product
    if review.exists():
        # update review
        update_review = {'rating': data['rating'], 'comment':data['comment']}
        review.update(**update_review)
        message = 'Prodcut review updated'
    else:
        # create review
        Review.objects.create(user=user,
                            product=product,
                            rating=data['rating'],
                            comment=data['comment'])
        message = 'Prodcut review created'

    # update product ratings from take average of users rating
    rating = product.reviews.aggregate(avg_ratings=Avg('rating'))
    product.ratings = rating['avg_ratings']
    product.save()
    return Response({'details': message})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_review(request, pk):
    user = request.user
    product = Product.objects.get(pk=pk)
    data = request.data
    # get the product and user
    review = product.reviews.filter(user=user)

    # check if a previous review exist from the same user on same product
    if review.exists():
        # delete review
        review.delete()
        message = 'Prodcut review deleted'
    else:
        # no review exist
        message = 'No review existed'

    # update product ratings from take average of users rating
    rating = product.reviews.aggregate(avg_ratings=Avg('rating'))
    if rating['avg_ratings'] is None:
        product.ratings = 0
        product.save()

    return Response({'details': message})