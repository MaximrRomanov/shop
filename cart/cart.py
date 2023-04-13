from decimal import Decimal
from django.conf import settings
from e_commerce.models import Product


class Cart(object):
    def __init__(self, request):
        """
           Инициализируем корзину
        """
        # храним текущую сессию
        self.session = request.session
        # пытаемся получить корзину с текущей сессии
        cart = self.session.get(settings.CART_SESSION_ID)
        # Если в сессии отсутствует корзина, то мы создадим сессию с пустой корзиной,
        # установив пустой словарь в сессии
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        # cart - это словарь
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """
         Добавить продукт в корзину или обновить его количество.
        """
        product_id = str(product.id)
        # проверка на наличие товара в корзине
        # id продукта — это ключ, а значение, которое мы сохраняем,
        # — словарь с количеством и ценой для продукта.
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }
        # если мы хотим обновлять кол-во товаров в корзине, то
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        # иначе
        else:
            self.cart[product_id]['quantity'] += quantity

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    # Метод remove() удаляет заданный продукт из словаря корзины
    # и вызывает метод save() для обновления корзины в сессии.
    def remove(self, product):
        """
           Удаление товара из корзины.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
            Перебор элементов в корзине и получение продуктов из базы данных.
        """
        # извлекаем экземпляры продукта, присутствующие в корзине
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        # получение объектов product и добавление их в корзину
        for product in products:
            self.cart[str(product.id)]['product'] = product

        # получение всех значений в корзине
        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    # способ вернуть общее количество товаров в корзине.
    def __len__(self):
        """
            Подсчет всех товаров в корзине.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
            Подсчет стоимости товаров в корзине.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
