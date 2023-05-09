from django.urls import path
from . import views
from .views import ShopCategoriesListView, ShopProductsListView, ProductDetailView, SearchListView

urlpatterns = [
    path("", ShopProductsListView.as_view(), name="home_page"),
    path("category/<slug:category_slug>", ShopCategoriesListView.as_view(), name="products_list_by_slug"),  # по слагу категории получили товары
    path("product/<slug:product_slug>/", ProductDetailView.as_view(), name="product_detail_by_slug"),  # по первичному ключу
    path("search/", SearchListView.as_view(), name="search_products"),  # по первичному ключу
    path("cat/", views.cat, name="cat")



]
