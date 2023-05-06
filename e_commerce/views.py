from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from .models import Category, Product


def get_home_page(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {
        'title': 'Hello world',
        'products': products,
        'categories': categories

    }
    return render(request, 'e_commerce/index.html', context=context)


class ShopProducts(ListView):
    model = Product
    template_name = 'e_commerce/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'


class ShopCategories(ListView):
    model = Product
    template_name = 'e_commerce/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        contex = super().get_context_data(**kwargs)

    # Выбрали те продукты, которые соответствуют данной категории
    def get_queryset(self):
        return Product.objects.filter(category__slug=self.kwargs['category_slug'])


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


# class RegisterUser(DataMixin, CreateView):
#     form_class = UserCreationForm # django предоставляет форму для регистрации пользователей
#     template_name = 'e_commerce/register.html'
#     success_url = reverse_lazy('login')
#     def context
