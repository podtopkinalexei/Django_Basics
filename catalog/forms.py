from django import forms
from django.core.exceptions import ValidationError

from .models import Product

FORBIDDEN_WORDS = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево',
                   'бесплатно', 'обман', 'полиция', 'радар']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price', 'publish_status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'publish_status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.user and not self.user.has_perm('catalog.can_change_publish_status'):
            self.fields.pop('publish_status')

        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                if 'class' not in field.widget.attrs:
                    field.widget.attrs['class'] = 'form-control'

    def clean_name(self):
        name = self.cleaned_data['name'].lower()
        for word in FORBIDDEN_WORDS:
            if word in name:
                raise ValidationError(f'Название не может содержать запрещенное слово: "{word}"')
        return self.cleaned_data['name']

    def clean_description(self):
        description = self.cleaned_data['description'].lower()
        if description:
            for word in FORBIDDEN_WORDS:
                if word in description:
                    raise ValidationError(f'Описание не может содержать запрещенное слово: "{word}"')
        return self.cleaned_data['description']

    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise ValidationError('Цена не может быть отрицательной')
        return price

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:

            if not image.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                raise ValidationError('Разрешены только файлы форматов JPEG и PNG')

            if image.size > 5 * 1024 * 1024:
                raise ValidationError('Размер файла не должен превышать 5 МБ')

        return image

    def save(self, commit=True):
        product = super().save(commit=False)
        if not product.pk and self.user:
            product.owner = self.user
        if commit:
            product.save()
        return product
