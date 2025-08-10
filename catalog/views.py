from django.shortcuts import render, get_object_or_404
from catalog.models import Product, Category

def index(request):
    products = Product.objects.all()[:6]
    return render(request, 'index.html', {'products': products})


def catalog(request):
    category_id = request.GET.get('category')

    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()

    categories = Category.objects.all()

    return render(request, 'catalog.html', {
        'products': products,
        'categories': categories,
        'current_category': category_id
    })

def contacts(request):
    return render(request, 'contacts.html')

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})