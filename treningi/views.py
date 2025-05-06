import logging
from django.shortcuts import render, redirect
from .forms import Exercise, ExerciseForm, ChallengeForm

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import User
from .forms import RegisterForm
from django.contrib import messages

from .forms import CustomAuthenticationForm

logger = logging.getLogger(__name__)

def home_view(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')

    if request.method == 'POST':
        #form = AuthenticationForm(request, data=request.POST)
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            logger.info(f"Użytkownik {user.username} zarejestrowany i zalogowany.")
            return redirect('home')
        else:
            logger.warning("Formularz rejestracji zawiera błędy!")
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})

def add_challenge(request):
    if request.method == "POST":
        form = ChallengeForm(request.POST)
        if form.is_valid():
            challenge = form.save(commit=False)

            challenge.save()
            return redirect('challenge_list')

    else:
        form = ChallengeForm()

    return render(request, 'add_challenge.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():  # Sprawdzamy, czy formularz jest poprawny
            user = form.get_user()  # Pobieramy użytkownika

            if not user.is_active:  # Sprawdzamy, czy konto jest aktywne
                messages.error(request, "Twoje konto zostało zablokowane. Skontaktuj się z administratorem.")
                return redirect('login')  # Przekierowanie po błędzie

            # Jeśli konto jest aktywne, logujemy użytkownika
            login(request, user)
            return redirect('home')  # Przekierowanie po udanym logowaniu

        else:  # Jeśli formularz nie jest poprawny
            messages.error(request, "Nieprawidłowy login lub hasło.")  # Komunikat o błędzie
            return redirect('login')  # Przekierowanie z komunikatem o błędzie

    else:
        form = CustomAuthenticationForm()  # Formularz w przypadku GET

    return render(request, 'users/login.html', {'form': form})

# def login_view(request):
#     if request.method == 'POST':
#         form = CustomAuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             # Wyszukaj użytkownika na podstawie formularza
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#
#             # Autentykacja użytkownika
#             user = authenticate(request, username=username, password=password)
#
#             # if user is not None:
#             #     if user.is_active:  # Sprawdzenie, czy konto jest aktywne
#             #         login(request, user)
#             #         return redirect('home')
#             #     else:
#             #         messages.error(request, "Twoje konto zostało zablokowane. Skontaktuj się z administratorem.")
#             #         return redirect('login')
#             # else:
#             #     # Jeśli nie ma użytkownika o podanych danych
#             #     messages.error(request, "Nieprawidłowy login lub hasło.")
#             #     return redirect('login')
#
#             if user is not None and user.is_active:
#                 login(request, user)
#                 return redirect('home')
#             elif user is not None and not user.is_active:
#                 messages.error(request, "Twoje konto zostało zablokowane. Skontaktuj się z administratorem.")
#                 return redirect('login')
#             else:
#                 messages.error(request, "Nieprawidłowy login lub hasło.")
#                 return redirect('login')
#
#     else:
#         form = CustomAuthenticationForm()
#
#     return render(request, 'users/login.html', {'form': form})

# def login_view(request):
#     if request.method == 'POST':
#         #form = AuthenticationForm(request, data=request.POST)
#         form = CustomAuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#
#             if user.is_active:
#                 login(request, user)
#                 return redirect('home')
#             else:
#                 messages.error(request, "Twoje konto zostało zablokowane. Skontaktuj się z administratorem.")
#                 return redirect('login')
#         else:
#             messages.error(request, "Nieprawidłowy login lub hasło.")
#             return redirect('login')
#     else:
#         form = AuthenticationForm()
#
#     return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')