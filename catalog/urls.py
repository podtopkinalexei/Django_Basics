from django.urls import path
from catalog.views import index, category, catalog, contacts

app_name = 'catalog'

urlpatterns = [
    path('', index, name='index'),
    path('category/', category, name='category'),
    path('catalog/', catalog, name='catalog'),
    path('contacts/', contacts, name='contacts'),
]
