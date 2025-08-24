from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView

from .forms import ProductForm
from .models import Product, Category


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


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:catalog')


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:catalog')


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:catalog')
