from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status

from product.models import Product
from .models import Order, OrderItem
from .serializers import OrderSerializer

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_orders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response({"orders": serializer.data})

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_order(request, id):
    order = get_object_or_404(Order, id=id)
    serializer = OrderSerializer(order, many=False)
    return Response({"order": serializer.data})

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def new_order(request):
    user = request.user
    data = request.data
    order_items = data['order_Items'] # list of item object

    if order_items and len(order_items) == 0:
        return Response({"error": "No order Recived"}, status=status.HTTP_400_BAD_REQUEST)

    else:
        # total_amount = sum( item['price'] * item['quantity'] for item in order_items)
        order = Order.objects.create(
            user = user,
            country = data["country"], 
            state = data["state"], 
            city = data["city"],
            street = data["street"], 
            zip_code = data["zip_code"],
            phone_no = data["phone_no"],
            total_amount = 0,
            )
        
        total_amount = 0
        for i in order_items:
            product = Product.objects.get(id=i['product'])
            item = OrderItem.objects.create(
                product = product,
                order = order,
                name = product.name,
                quantity = i['quantity'],
                price = product.price,
            )
            total_amount += product.price * i['quantity']

            product.stock -= item.quantity
            product.save()

        order.total_amount = total_amount
        order.save()

    serializer = OrderSerializer(order, many=False)
    return Response(serializer.data)



@api_view(["PUT"])
@permission_classes([IsAuthenticated, IsAdminUser])
def update_order(request, id):
    order = get_object_or_404(Order, id=id)
    order.status = request.data['status']
    order.save() 

    serializer = OrderSerializer(order, many=False)
    return Response({"order": serializer.data})

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_order(request, id):
    order = get_object_or_404(Order, id=id)
    order.delete()
    return Response({"details": "Order is delected successfully"})