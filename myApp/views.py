from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .emails import send_welcome_email


def index(request):
    return render(request, "index.html")


def privacy(request):
    return render(request, "privacy.html")


def terms(request):
    return render(request, "terms.html")


def security(request):
    return render(request, "security.html")


def data_deletion(request):
    return render(request, "data-deletion.html")


def contact(request):
    return render(request, "contact.html")


def login_page(request):
    if request.user.is_authenticated:
        return redirect('launchpad')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')

        if not email or not password:
            return render(request, 'login.html', {
                'error': 'Please enter your email and password.',
                'email': email,
            })

        user = authenticate(request, username=email, password=password)
        if user is None:
            return render(request, 'login.html', {
                'error': 'Invalid email or password.',
                'email': email,
            })

        login(request, user)
        return redirect('launchpad')

    return render(request, 'login.html')


def signup_page(request):
    if request.user.is_authenticated:
        return redirect('launchpad')

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        confirm = request.POST.get('confirm', '')

        ctx = {'name': name, 'email': email}

        if not name:
            ctx['error'] = 'Please enter your name.'
            return render(request, 'signup.html', ctx)
        if '@' not in email or '.' not in email:
            ctx['error'] = 'Please enter a valid email address.'
            return render(request, 'signup.html', ctx)
        if len(password) < 8:
            ctx['error'] = 'Password must be at least 8 characters.'
            return render(request, 'signup.html', ctx)
        if password != confirm:
            ctx['error'] = 'Passwords do not match.'
            return render(request, 'signup.html', ctx)
        if User.objects.filter(username=email).exists():
            ctx['error'] = 'An account with this email already exists. Try signing in.'
            return render(request, 'signup.html', ctx)

        user = User.objects.create_user(username=email, email=email, password=password)
        parts = name.split(' ', 1)
        user.first_name = parts[0][:30]
        if len(parts) > 1:
            user.last_name = parts[1][:30]
        user.save()

        send_welcome_email(user)

        login(request, user)
        return redirect('launchpad')

    return render(request, 'signup.html')


@login_required(login_url='/login')
def launchpad(request):
    return render(request, 'launchpad.html')


def logout_view(request):
    logout(request)
    return redirect('/')
