from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from .models import Category, Product


# def get_home_page(request):
#     products = Product.objects.all()
#     categories = Category.objects.all()
#     context = {
#         'title': 'Hello world',
#         'products': products,
#         'categories': categories
#
#     }
#     return render(request, 'e_commerce/index.html', context=context)

class ShopProductsListView(ListView):
    model = Product
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
        return context


class ShopCategoriesListView(ListView):
    model = Product
    template_name = 'e_commerce/index.html'
    extra_context = 'categories'

    def get_context_data(self, *, object_list=None, **kwargs):
        contex = super().get_context_data(**kwargs)

    # Выбрали те продукты, которые соответствуют данной категории
    def get_queryset(self):
        return Product.objects.filter(category__slug=self.kwargs['category_slug'])  # возвращает коллекцию object_list


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


def get_user_login(request):
    return HttpResponse(f"<h1> Get user  login</h1>")


def register(request):
    return HttpResponse("<h1> Ura Register!</h1>")


def logout(request):
    return HttpResponse("<h1> Ura Logout!</h1>")


def cat(request):
    return render(request, 'e_commerce/categories.html', context={'title': 'Категории'})


# для регистрации новых пользователей
class RegisterUser(CreateView):
    form_class = UserCreationForm  # django предоставляет форму для регистрации пользователей
    template_name = 'e_commerce/register.html'
    # атрибут, отвечающий за перенаправление на страницу входа после успешной регистрации
    success_url = reverse_lazy('login')

    # метод возвращает данные контекста для отображения объекта.
    def get_context_data(self, **kwargs):
        pass

