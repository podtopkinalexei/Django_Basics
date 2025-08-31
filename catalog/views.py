from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseForbidden

from catalog.forms import ProductForm
from catalog.models import Product, Category


class OwnerRequiredMixin(UserPassesTestMixin):
    """Миксин для проверки владельца продукта"""

    def test_func(self):
        product = self.get_object()
        user = self.request.user
        # Владелец или модератор
        return user == product.owner or user.has_perm('catalog.delete_product')

    def handle_no_permission(self):
        return HttpResponseForbidden(_("У вас нет прав для выполнения этого действия"))


class ModeratorRequiredMixin(UserPassesTestMixin):
    """Миксин для проверки прав модератора"""

    def test_func(self):
        return self.request.user.has_perm('catalog.can_unpublish_product')


class IndexView(ListView):
    model = Product
    template_name = 'catalog/index.html'
    context_object_name = 'products'
    queryset = Product.objects.filter(is_published=True)[:6]


class CatalogView(ListView):
    model = Product
    template_name = 'catalog/catalog.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_id = self.request.GET.get('category')
        queryset = Product.objects.filter(is_published=True)

        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_category'] = self.request.GET.get('category')
        return context


class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'pk'


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:catalog')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, _('Продукт успешно создан!'))
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:catalog')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, _('Продукт успешно обновлен!'))
        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:catalog')

    def delete(self, request, *args, **kwargs):
        messages.success(request, _('Продукт успешно удален!'))
        return super().delete(request, *args, **kwargs)


class ProductUnpublishView(LoginRequiredMixin, ModeratorRequiredMixin, UpdateView):
    model = Product
    fields = []
    template_name = 'catalog/product_unpublish_confirm.html'

    def form_valid(self, form):
        product = form.save(commit=False)
        product.publish_status = 'rejected'
        product.save()
        messages.success(self.request, _('Публикация продукта отменена!'))
        return redirect('catalog:product_detail', pk=product.pk)


class ProductPublishView(LoginRequiredMixin, ModeratorRequiredMixin, UpdateView):
    model = Product
    fields = []
    template_name = 'catalog/product_publish_confirm.html'

    def form_valid(self, form):
        product = form.save(commit=False)
        product.publish_status = 'published'
        product.save()
        messages.success(self.request, _('Продукт опубликован!'))
        return redirect('catalog:product_detail', pk=product.pk)
