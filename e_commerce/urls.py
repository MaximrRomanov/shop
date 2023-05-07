from django.urls import path
from . import views
from .views import ShopCategoriesListView, ShopProductsListView

urlpatterns = [
    path("", ShopProductsListView.as_view(), name="home_page"),
    path("category/<slug:category_slug>", ShopCategoriesListView.as_view(), name="products_list_by_slug"),  # по слагу категории получили товары
    path("product/<slug:product_slug>/", ShopProductsListView.as_view(), name="product_detail_by_slug"),  # по первичному ключу
    # path("login/", views.get_user_login, name="user_login"),
    # path("register/", views.register, name="register"),
    # path("logout/", views.logout, name="logout"),
    path("cat/", views.cat, name="cat")


]
