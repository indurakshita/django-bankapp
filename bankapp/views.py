# bankapp/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import requires_csrf_token
from .forms import SignupForm, TransactionForm, LoginForm
from .models import UserProfile, Transaction
import random

def home(request):
    return render(request, 'home.html')

def generate_account_number(username):
   
    username_prefix = username[:2].upper()
    random_number = str(random.randint(10000, 99999))
    account_number = f"{username_prefix}{random_number}" 
    return account_number


@requires_csrf_token
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            account_number = generate_account_number(user.username)
            user_profile = UserProfile.objects.create(user=user, account_number=account_number)
            messages.success(request, 'Account successfully created')  
            return redirect('login')
        else:
            messages.error(request, 'Error creating the account. Please check the form.') 
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})

def custom_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('ac_detail')  
            else:
                messages.error(request, 'Invalid login credentials. Please try again.')  # Add error message
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

@login_required
def ac_detail(request):
    account = UserProfile.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account)
    return render(request, 'ac_detail.html', {'account': account, 'transactions': transactions})

@login_required
def perform_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            account = UserProfile.objects.get(user=request.user)
            transaction = form.save(commit=False)
            transaction.account = account

            if transaction.transaction_type == 'withdrawal' and transaction.amount > account.balance:
                error_message = 'Insufficient funds'
                return render(request, 'transactions.html', {'form': form, 'error_message': error_message})

            transaction.save()

            if transaction.transaction_type == 'deposit':
                account.balance += transaction.amount
            elif transaction.transaction_type == 'withdrawal':
                account.balance -= transaction.amount

            account.save()

            return redirect('ac_detail')
    else:
        form = TransactionForm()

    return render(request, 'transactions.html', {'form': form})


def custom_logout(request):
    logout(request)
    return redirect('home') 