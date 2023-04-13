from django.urls import path
from . import views

urlpatterns = [
    # path("", views.get_home_page, name="home_page"),
    path("category/<slug:category_slug>", views.get_products_list_by_slug, name="products_list_by_slug"),  # по слагу категории получили товары
    path("product/<slug:product_slug>/", views.get_product_detail_by_slug, name="product_detail_by_slug"),  # по первичному ключу

]
