import django_filters

from .models import Product

class ProductFiter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="iexact")
    keyword = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    minPrice = django_filters.NumberFilter(field_name="price" or 0, lookup_expr="gte") # gte --> greater than or equal
    maxPrice = django_filters.NumberFilter(field_name="price" or 10000, lookup_expr="lte") # lte --> less than or equal
    
    class Meta:
        model = Product
        # fields = "__all__"
        # fields = ['price', 'brand', 'category', 'ratings']
        # must by in a tuple not a list 
        fields = ('price', 'brand', 'category', 'ratings', 'keyword', 'minPrice', 'maxPrice')


