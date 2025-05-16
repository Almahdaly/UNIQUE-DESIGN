from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm, LoginForm, ResendActivationForm, ProfileForm
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser
from django.contrib.auth import login as auth_login, logout as auth_logout
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

# سيتم لاحقًا ربط التوكن بجدول منفصل أو استخدام مكتبة جاهزة، الآن سنستخدمه بشكل مبسط
activation_tokens = {}
TOKEN_EXPIRY_HOURS = 1

def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # توليد رمز تحقق عشوائي مع وقت الإنشاء
            token = get_random_string(32)
            activation_tokens[user.email] = {'token': token, 'created': datetime.now()}
            activation_link = request.build_absolute_uri(f'/accounts/activate/{token}/')
            send_mail(
                subject='تفعيل حسابك في المنصة',
                message=f'يرجى الضغط على الرابط التالي لتفعيل حسابك (صالح لمدة ساعة واحدة): {activation_link}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            messages.success(request, 'تم إنشاء الحساب بنجاح. يرجى التحقق من بريدك الإلكتروني لتفعيل الحساب.')
            return redirect('accounts:register_success')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def register_success(request):
    return render(request, 'accounts/register_success.html')

def activate_account(request, token):
    # البحث عن المستخدم المرتبط بالتوكن
    email = None
    for user_email, data in activation_tokens.items():
        if data['token'] == token:
            email = user_email
            created = data['created']
            break
    if email:
        now = datetime.now()
        if now - created > timedelta(hours=TOKEN_EXPIRY_HOURS):
            # انتهت صلاحية التوكن
            del activation_tokens[email]
            messages.error(request, 'انتهت صلاحية رابط التفعيل. يمكنك إعادة إرسال رابط جديد من <a href="/accounts/resend-activation/" class="text-primary underline">هنا</a>.')
            return redirect('accounts:login')
        try:
            user = CustomUser.objects.get(email=email)
            user.is_active = True
            user.save()
            del activation_tokens[email]
            messages.success(request, 'تم تفعيل الحساب بنجاح. يمكنك الآن تسجيل الدخول.')
            return redirect('accounts:login')
        except CustomUser.DoesNotExist:
            messages.error(request, 'حدث خطأ أثناء تفعيل الحساب.')
    else:
        messages.error(request, 'رمز التفعيل غير صالح أو منتهي.')
    return redirect('accounts:register')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            auth_login(request, user)
            messages.success(request, 'تم تسجيل الدخول بنجاح.')
            return redirect('/')  # يمكنك تغيير المسار للوحة التحكم أو الصفحة الرئيسية
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    messages.success(request, 'تم تسجيل الخروج بنجاح.')
    return redirect('accounts:login')

def resend_activation(request):
    if request.method == 'POST':
        form = ResendActivationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = CustomUser.objects.get(email=email)
                if not user.is_active:
                    token = get_random_string(32)
                    activation_tokens[user.email] = {'token': token, 'created': datetime.now()}
                    activation_link = request.build_absolute_uri(f'/accounts/activate/{token}/')
                    send_mail(
                        subject='إعادة إرسال تفعيل الحساب في المنصة',
                        message=f'يرجى الضغط على الرابط التالي لتفعيل حسابك (صالح لمدة ساعة واحدة): {activation_link}',
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[user.email],
                        fail_silently=False,
                    )
            except CustomUser.DoesNotExist:
                pass
            messages.success(request, 'إذا كان البريد غير مفعل ستصلك رسالة تفعيل جديدة (تحقق من البريد أو مجلد الرسائل غير المرغوب فيها).')
            return redirect('accounts:resend_activation')
    else:
        form = ResendActivationForm()
    return render(request, 'accounts/resend_activation.html', {'form': form})

@login_required(login_url='accounts:login')
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تحديث البيانات بنجاح.')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=user)
    return render(request, 'accounts/profile.html', {'form': form, 'user': user})

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('accounts:password_change_done')
    def form_valid(self, form):
        messages.success(self.request, 'تم تغيير كلمة المرور بنجاح.')
        return super().form_valid(form)

def password_change_done(request):
    return render(request, 'accounts/password_change_done.html')
