from django.urls import path
from catalog.views import index, catalog, contacts, product_detail


app_name = 'catalog'

urlpatterns = [
    path('', index, name='index'),
    path('catalog/', catalog, name='catalog'),
    path('product/<int:pk>/', product_detail, name='product_detail'),
    path('contacts/', contacts, name='contacts'),
]
