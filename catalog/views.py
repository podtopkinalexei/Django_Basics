from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import get_object_or_404
from catalog.models import Product, Category


class IndexView(ListView):
    model = Product
    template_name = 'catalog/index.html'
    context_object_name = 'products'
    queryset = Product.objects.all()[:6]


class CatalogView(ListView):
    model = Product
    template_name = 'catalog/catalog.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_id = self.request.GET.get('category')
        if category_id:
            return Product.objects.filter(category_id=category_id)
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_category'] = self.request.GET.get('category')
        return context


class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'pk'

