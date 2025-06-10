import logging
from django.shortcuts import render, redirect
from .forms import Exercise, ExerciseForm, ChallengeForm

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import User, Workout, WorkoutStatistics
from .forms import RegisterForm
from django.contrib import messages
from django.http import JsonResponse
from django.db import models

from .forms import CustomAuthenticationForm

logger = logging.getLogger(__name__)

def home_view(request):
    if request.user.is_authenticated:
        return redirect('home_page')

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
            print("Dodano wyzwanie")
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

def home_page_view(request):
    workouts = Workout.objects.prefetch_related('exercises').all()
    return render(request, 'home_page.html', {'workouts': workouts})

def do_workout(request):
    if request.method == 'POST':
        workout_id = request.POST.get('workout_id')
        try:
            workout = Workout.objects.get(id=workout_id)
            user = request.user
            if not user.is_authenticated: #spr
                return JsonResponse({'success': False, 
                                     'error': 'user not authenticated'})
            #dodanie pkt xp
            user.user_score_xp += workout.score_xp
            user.save()

            #dodaje do statystyk
            WorkoutStatistics.objects.create(
                user=user,
                workout=workout,
                duration=workout.exercises.aggregate(models.Sum('duration_minutes'))['duration_minutes__sum'] or 0,
                calories_burned=workout.score_xp * 2 #na razie mnozone przez score
            )

            print("Wykonano trening")
            return JsonResponse({
                'success': True,
                'new_score': user.user_score_xp
            })
        except Workout.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'workout err'
            })
    return JsonResponse({
        'success': False,
        'error': "invalid request"
    })


#do strony profilu uzytkownika
def user_profile_page_view(request):
    user = request.user
    workouts_history = WorkoutStatistics.objects.filter(user=user).select_related('workout').order_by('-workout_date') #treningi w kolejnosci odwrotnej
    #nowe statystyki
    total_workouts = workouts_history.count() #zlicza treningi
    total_time_spent = WorkoutStatistics.objects.filter(user=user).aggregate(models.Sum('duration'))['duration__sum'] or 0  #sumuje czas wszystkich trenigow
    total_calories_burned = WorkoutStatistics.objects.filter(user=user).aggregate(models.Sum('calories_burned'))['calories_burned__sum'] or 0 #sumuje kalorie
    return render(request, 'user_profile_page.html', {'user': user, 
                                                      'workouts_history': workouts_history,
                                                      'total_workouts': total_workouts,
                                                        'total_time_spent': total_time_spent,
                                                        'total_calories_burned': total_calories_burned,
                                                        })
#ranking uzytkownikow
def ranking_view(request):
    users = User.objects.all().order_by('-user_score_xp')
    print("Wyświetlono ranking")
    return render(request, 'ranking.html', {'users': users})
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
