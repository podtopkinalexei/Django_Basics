from django.urls import path
from .views import (
    IndexView, CatalogView, ContactsView, 
    ProductDetailView, ProductCreateView, 
    ProductUpdateView, ProductDeleteView,
    ProductUnpublishView, ProductPublishView
)

app_name = 'catalog'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('catalog/', CatalogView.as_view(), name='catalog'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('product/<int:pk>/unpublish/', ProductUnpublishView.as_view(), name='product_unpublish'),
    path('product/<int:pk>/publish/', ProductPublishView.as_view(), name='product_publish'),
]