from django import forms
from .models import CustomUser, USER_TYPE_CHOICES
from django.contrib.auth import authenticate

class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='كلمة المرور', widget=forms.PasswordInput)
    password2 = forms.CharField(label='تأكيد كلمة المرور', widget=forms.PasswordInput)
    user_type = forms.ChoiceField(choices=[(k, v) for k, v in USER_TYPE_CHOICES if k != 'admin'], label='نوع المستخدم')
    agree = forms.BooleanField(label='أوافق على <a href="/privacy/" target="_blank" class="text-primary underline">الشروط وسياسة الخصوصية</a>', required=True)

    class Meta:
        model = CustomUser
        fields = ('full_name', 'email', 'user_type')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('هذا البريد الإلكتروني مسجل بالفعل.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'كلمتا المرور غير متطابقتين.')
        if not cleaned_data.get('agree'):
            self.add_error('agree', 'يجب الموافقة على الشروط وسياسة الخصوصية لإنشاء الحساب.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False  # الحساب غير مفعل حتى يتم التحقق من البريد
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    email = forms.EmailField(label='البريد الإلكتروني', widget=forms.EmailInput(attrs={
        'class': 'w-full px-4 py-3 border border-gray-300 rounded-button focus:border-primary focus:ring-1 focus:ring-primary placeholder-transparent',
        'placeholder': 'البريد الإلكتروني',
        'id': 'id_email',
        'required': True,
    }))
    password = forms.CharField(label='كلمة المرور', widget=forms.PasswordInput(attrs={
        'class': 'w-full px-4 py-3 border border-gray-300 rounded-button focus:border-primary focus:ring-1 focus:ring-primary placeholder-transparent',
        'placeholder': 'كلمة المرور',
        'id': 'id_password',
        'required': True,
    }))

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError('البريد الإلكتروني أو كلمة المرور غير صحيحة.')
            if not user.is_active:
                raise forms.ValidationError('الحساب غير مفعل. يرجى التحقق من بريدك الإلكتروني والضغط على رابط التفعيل. إذا لم تصلك الرسالة، تحقق من مجلد الرسائل غير المرغوب فيها (Spam).')
            cleaned_data['user'] = user
        return cleaned_data

class ResendActivationForm(forms.Form):
    email = forms.EmailField(label='البريد الإلكتروني', widget=forms.EmailInput(attrs={
        'class': 'w-full px-4 py-3 border border-gray-300 rounded-button focus:border-primary focus:ring-1 focus:ring-primary placeholder-transparent',
        'placeholder': 'البريد الإلكتروني',
        'id': 'id_email',
        'required': True,
    }))

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'profile_image']
        labels = {
            'full_name': 'الاسم الكامل',
            'profile_image': 'الصورة الشخصية',
        }
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-input w-full px-4 py-3 border border-gray-300 rounded-button focus:border-primary focus:ring-1 focus:ring-primary',
                'placeholder': 'الاسم الكامل',
                'id': 'id_full_name',
                'required': True,
            }),
            'profile_image': forms.ClearableFileInput(attrs={
                'class': 'form-input w-full',
                'id': 'id_profile_image',
            }),
        } 