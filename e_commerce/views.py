from django.shortcuts import render, get_object_or_404
from .models import Category, Product


# Чтобы отобразить каталог продуктов, необходимо создать представление для списка всех
# продуктов или фильтрации продуктов по данной категории (получение продуктов по слагу категории)
def get_products_list_by_slug(request, category_slug=None):
    # если слаг категории не установлен, то
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)  # фильтруем продукты по доступности
    # если слаг категории установлен, то
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)  # ищем категорию по слагу
        products = Product.objects.filter(category=category)  # фильтруем продукты по соответствующей категории

    context = {
        'category': category,
        'categories': categories,
        'products': products
    }
    return render(request, '', context=context)


# представление для извлечения и отображения одного продукта
def get_product_detail_by_slug(request, product_slug=None):
    product = None
    if product_slug:
        product = get_object_or_404(Product, slug=product_slug, available=True)

    context = {
        'product': product
    }
    return render(request, '', context=context)
