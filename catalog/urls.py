from django.urls import path
from .views import IndexView, CatalogView, ContactsView, ProductDetailView

app_name = 'catalog'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('catalog/', CatalogView.as_view(), name='catalog'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
]

