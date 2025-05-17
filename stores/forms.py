from django import forms
from .models import Store

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'description', 'image', 'logo', 'cover', 'primary_color']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-button focus:border-primary focus:ring-1 focus:ring-primary',
                'placeholder': 'اسم المتجر',
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-button focus:border-primary focus:ring-1 focus:ring-primary',
                'placeholder': 'وصف المتجر',
                'rows': 4,
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'hidden',
                'accept': 'image/*',
                'id': 'store_image',
            }),
            'logo': forms.ClearableFileInput(attrs={
                'class': 'hidden',
                'accept': 'image/*',
                'id': 'store_logo',
            }),
            'cover': forms.ClearableFileInput(attrs={
                'class': 'hidden',
                'accept': 'image/*',
                'id': 'store_cover',
            }),
            'primary_color': forms.TextInput(attrs={
                'type': 'color',
                'class': 'w-16 h-10 p-0 border-0 bg-transparent',
                'style': 'cursor:pointer;',
            }),
        } 