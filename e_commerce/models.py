from django.db import models


class Category(models.Model):
    name = models.CharField(verbose_name="Название", max_length=200, db_index=True)
    slug = models.SlugField(verbose_name="Слаг", max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    AVAILABLE_STATUS = [
        ("ДО", "Доступен"),
        ("НД", "Не доступен")
    ]
    name = models.CharField(verbose_name="Название", max_length=200, db_index=True)
    slug = models.SlugField(verbose_name="Слаг", max_length=200, db_index=True, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    description = models.TextField(verbose_name="Описание", blank=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', verbose_name="Изображение", blank=True)
    stock = models.PositiveIntegerField(verbose_name="Количество")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, verbose_name="Категория", max_length=200)
    available = models.CharField(choices=AVAILABLE_STATUS, verbose_name="Статус")

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return self.name
