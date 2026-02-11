from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegistrationForm, UserProfileForm
from .models import User


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('shop:product_list')
    else:
        form = UserRegistrationForm()
    
    context = {
        'form': form,
        'title': 'Регистрация'
    }
    return render(request, 'accounts/register.html', context)


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.email}!')
            
            next_url = request.GET.get('next', 'shop:product_list')
            return redirect(next_url)
    else:
        form = AuthenticationForm()
    
    context = {
        'form': form,
        'title': 'Вход в систему'
    }
    return render(request, 'accounts/login.html', context)


def user_logout(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('shop:product_list')


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    context = {
        'form': form,
        'title': 'Мой профиль'
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def order_history(request):
    from orders.models import Order
    
    orders = Order.objects.filter(user=request.user).order_by('-created')
    
    context = {
        'orders': orders,
        'title': 'История заказов'
    }
    return render(request, 'accounts/order_history.html', context)
