from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import loginForm


def user_login(request):
    if request.user.is_authenticated:
        return redirect('home:home')

    if request.method == "POST":
        form = loginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            return redirect('home:home')
    else:
        form = loginForm()

    return render(request, 'account/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home:home')


def user_register(request):
    context = {"error": []}
    if request.user.is_authenticated:
        return redirect('home:home')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password_1 = request.POST.get('password_1')
        password_2 = request.POST.get('password_2')

        if password_1 != password_2:
            context['error'].append("رمزهای عبور مطابقت ندارند.")
            return render(request, 'account/register.html', context)

        if User.objects.filter(username=username).exists():
            context['error'].append("نام کاربری قبلاً ثبت شده است.")
            return render(request, 'account/register.html', context)

        if User.objects.filter(email=email).exists():
            context['error'].append("ایمیل قبلاً ثبت شده است.")
            return render(request, 'account/register.html', context)

        user = User.objects.create_user(username=username, email=email, password=password_1)
        login(request, user)
        return redirect('home:home')

    return render(request, 'account/register.html', context)