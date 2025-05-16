from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'price', 'category', 'is_available', 'quantity', 'brand']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-input'}),
            'category': forms.TextInput(attrs={'class': 'form-input'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-input'}),
            'brand': forms.TextInput(attrs={'class': 'form-input'}),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            valid_types = [
                'image/jpeg', 'image/png', 'image/gif', 'image/webp',
                'image/bmp', 'image/svg+xml', 'image/tiff', 'image/x-icon', 'image/vnd.microsoft.icon'
            ]
            if image.content_type not in valid_types:
                raise forms.ValidationError('صيغة الصورة غير مدعومة. الصيغ المسموحة: JPG, PNG, GIF, WEBP, BMP, SVG, TIFF, ICO')
        return image 