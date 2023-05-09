from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView
from .models import Category, Product


# Отображение главной страницы с продуктами и категориями
class ShopProductsListView(ListView):
    model = Product
    paginate_by = 1
    template_name = 'e_commerce/index.html'
    # (атрибут класса) та переменная, которую мы будем использовать в шаблоне, default переменная называется object_list
    context_object_name = 'products'

    # специальный атрибут здесь можно передавать только статические неизменяемые данные
    # extra_context = {'title': 'Главная страница'}
    # Возвращает данные контекста для отображения объекта.
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(
            **kwargs)  # обращаемся к родительскому классу ListView для получения его контекста
        context['title'] = 'Главная страница'
        context['categories'] = Category.objects.all()
        return context


# Отображение всех товаров определенной категории
class ShopCategoriesListView(ListView):
    model = Product
    paginate_by = 1
    # Под капотом все методы пагинации используют класс Paginator.
    # Он выполняет всю тяжелую работу по разбиению QuerySet на Page объекты.
    template_name = 'e_commerce/index.html'
    context_object_name = 'products'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категория - ' + str(context['products'][0].category)
        context['categories'] = Category.objects.all()
        return context

    # Выбрали те продукты, которые соответствуют данной категории
    def get_queryset(self):
        return Product.objects.filter(category__slug=self.kwargs['category_slug'])  # возвращает коллекцию object_list
    # в зависимости от гет запроса


class ProductDetailView(DetailView):
    """ Страница товара"""
    model = Product
    template_name = 'e_commerce/product.html'
    context_object_name = 'product_detail'
    # без этого атрибута он видит просто slug
    slug_url_kwarg = 'product_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Страница товара'
        context['categories'] = Category.objects.all()
        return context

    # def get_queryset(self):
    #     return Product.objects.filter(slug__in=self.kwargs['product_slug'])


class SearchListView(ListView):
    """ Поиск товаров"""
    # будем выводить по 3 фильма
    paginate_by = 3

    # фильтруем продукты по названию без учета регистра (icontains) и возвращаем queryset
    def get_queryset(self):
        return Product.objects.filter(name__icontains=self.request.GET('query'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET('query')
        return context


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


# представление для извлечения и отображения одного продукта !!! БОЛЬШИЕ ВОПРОСЫ К ОТСУТСТВИЮ СЛАГА
def get_product_detail_by_slug(request, product_slug=None):
    product = None
    if product_slug:
        product = get_object_or_404(Product, slug=product_slug)

    context = {
        'product': product
    }
    # return HttpResponse(f"<h1> Get user {product_slug} login</h1>")
    return render(request, 'e_commerce/product.html', context=context)


def cat(request):
    return render(request, 'e_commerce/categories.html', context={'title': 'Категории'})
