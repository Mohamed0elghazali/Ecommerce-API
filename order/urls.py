from django.urls import path

from . import views

urlpatterns = [
    path("orders/", view=views.get_orders, name="get_all_orders"),
    path("orders/<str:id>", view=views.get_order, name="get_order_by_id"),
    path("orders/new/", view=views.new_order, name="new_order"),
    path("orders/update/<str:id>", view=views.update_order, name="update_status"),
    path("orders/delete/<str:id>", view=views.delete_order, name="delete_order"),
]

