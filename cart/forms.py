from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


# Форма будет использоваться для добавления продуктов в корзину.
class CartAddProductForm(forms.Form):
    # Позволяет пользователю выбрать количество между 1-20.
    # Мы используем поле TypedChoiceField с coerce=int для преобразования ввода в целое число
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

