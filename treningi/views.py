import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Exercise
from .forms import ExerciseForm, ChallengeForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import User
from .forms import RegisterForm, UserWorkoutForm, UserChallengeForm
from django.contrib import messages
from .forms import CustomAuthenticationForm
from .forms import LoggedWorkoutForm
from .models import Workout, LoggedWorkout, LoggedWorkout, LoggedWorkoutExercise, Challenge, UserWorkout, \
    UserChallenge, ChallengeHistory, WorkoutHistory
from django.http import Http404, JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone

logger = logging.getLogger(__name__)


@login_required
def home_view(request):
    workouts = Workout.objects.all()
    now = timezone.now()
    challenges = Challenge.objects.filter(start_date__lte=now, end_date__gte=now)

    user_workouts = list(UserWorkout.objects.filter(user=request.user).values_list('workout_id', flat=True))
    user_challenges = list(UserChallenge.objects.filter(user=request.user).values_list('challenge_id', flat=True))

    return render(request, 'home.html', {
        'workouts': workouts,
        'challenges': challenges,
        'user_workouts': user_workouts,
        'user_challenges': user_challenges,
    })


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

            exercise_ids = request.POST.getlist('exercise_ids')
            for exercise_id in exercise_ids:
                exercise = Exercise.objects.get(id=exercise_id)

            return redirect('challenge_list')

    else:
        form = ChallengeForm()

    exercises = Exercise.objects.all()
    return render(request, 'add_challenge.html', {'form': form, 'exercises': exercises})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()

            if not user.is_active:
                messages.error(request, "Twoje konto zostało zablokowane. Skontaktuj się z administratorem.")
                return redirect('login')

            login(request, user)
            return redirect('home')

        else:
            messages.error(request, "Nieprawidłowy login lub hasło.")
            return redirect('login')

    else:
        form = CustomAuthenticationForm()

    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def log_workout_view(request):
    workouts = Workout.objects.all()
    selected_workout = None
    workout_exercises = []

    if request.method == 'POST':
        workout_id = request.POST.get('workout_id')
        if workout_id:
            selected_workout = Workout.objects.get(id=workout_id)
            workout_exercises = selected_workout.workoutexercise_set.all()

            for we in workout_exercises:
                duration = request.POST.get(f'duration_{we.id}')
                repetitions = request.POST.get(f'repetitions_{we.id}')
                sets = request.POST.get(f'sets_{we.id}')
                weight = request.POST.get(f'weight_{we.id}')

                LoggedWorkoutExercise.objects.create(
                    user=request.user,
                    workout_exercise=we,
                    duration_minutes=duration,
                    repetitions=repetitions,
                    sets=sets,
                    weight=weight
                )

            LoggedWorkout.objects.create(user=request.user, workout=selected_workout)
            return redirect('home')

    elif request.method == 'GET':
        workout_id = request.GET.get('workout_id')
        if workout_id:
            selected_workout = Workout.objects.get(id=workout_id)
            workout_exercises = selected_workout.workoutexercise_set.all()

    return render(request, 'log_workout.html', {
        'workouts': workouts,
        'selected_workout': selected_workout,
        'workout_exercises': workout_exercises
    })

def assign_workout_to_user(request):
    if request.method == 'POST':
        form = UserWorkoutForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserWorkoutForm(user=request.user)
    return render(request, 'assign_workout.html', {'form': form})

def assign_challenge_to_user(request):
    if request.method == 'POST':
        form = UserChallengeForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserChallengeForm(user=request.user)
    return render(request, 'assign_challenge.html', {'form': form})


@login_required
def add_workout(request, workout_id):
    try:
        workout = Workout.objects.get(id=workout_id)
    except Workout.DoesNotExist:
        raise Http404("Trening o tym ID nie istnieje.")

    UserWorkout.objects.get_or_create(user=request.user, workout=workout)

    return redirect('available_workouts')


@login_required
def available_workouts(request):
    workouts = Workout.objects.all()
    user_workouts = UserWorkout.objects.filter(user=request.user).values_list('workout_id', flat=True)

    return render(request, 'workouts/available_workouts.html', {
        'workouts': workouts,
        'user_workouts': user_workouts
    })

@login_required
def available_challenges(request):
    challenges = Challenge.objects.all()
    user_challenges = UserChallenge.objects.filter(user=request.user).values_list('challenge_id', flat=True)
    return render(request, 'challenges/available_challenges.html', {
        'challenges': challenges,
        'user_challenges': user_challenges
    })

def add_challenge(request, challenge_id):
    challenge = get_object_or_404(Challenge, id=challenge_id)
    request.user.profile.challenges.add(challenge)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True})

    return redirect('available_challenges')


@login_required
@require_POST
def toggle_challenge(request):
    challenge_id = request.POST.get('challenge_id')
    challenge = get_object_or_404(Challenge, id=challenge_id)
    user = request.user

    user_challenge, created = UserChallenge.objects.get_or_create(user=user, challenge=challenge)

    if not created:
        user_challenge.delete()

        ChallengeHistory.objects.create(
            admin_user=user,
            challenge=challenge,
            action='deleted'
        )
        return JsonResponse({'status': 'removed'})

    ChallengeHistory.objects.create(
        admin_user=user,
        challenge=challenge,
        action='added'
    )
    return JsonResponse({'status': 'added'})

@login_required
def challenge_history(request):
    if not request.user.is_superuser:
        return redirect('home')

    history = ChallengeHistory.objects.all().order_by('-action_date')

    return render(request, 'admin/challenge_history.html', {'history': history})


@login_required
def toggle_workout(request):
    if request.method == 'POST':
        workout_id = request.POST.get('workout_id')
        workout = get_object_or_404(Workout, id=workout_id)
        user = request.user

        user_workout, created = UserWorkout.objects.get_or_create(user=user, workout=workout)

        if not created:
            user_workout.delete()
            WorkoutHistory.objects.create(user=user, workout=workout, action='removed')
            return JsonResponse({'status': 'removed'})
        else:
            WorkoutHistory.objects.create(user=user, workout=workout, action='added')
            return JsonResponse({'status': 'added'})

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def workout_history(request):
    if not request.user.is_superuser:
        return redirect('home')

    history = WorkoutHistory.objects.all().order_by('-action_date')

    return render(request, 'admin/workout_history.html', {'history': history})


@login_required
def user_workouts_and_challenges(request):
    user_workouts_qs = UserWorkout.objects.filter(user=request.user)
    workouts = Workout.objects.filter(id__in=user_workouts_qs.values_list('workout_id', flat=True))

    user_challenges_qs = UserChallenge.objects.filter(user=request.user).select_related('challenge')
    challenges = Challenge.objects.filter(id__in=user_challenges_qs.values_list('challenge_id', flat=True))

    user_challenges_dict = {uc.challenge_id: uc for uc in user_challenges_qs}

    return render(request, 'users/user_workouts_and_challenges.html', {
        'workouts': workouts,
        'challenges': challenges,
        'user_workouts': list(user_workouts_qs.values_list('workout_id', flat=True)),
        'user_challenges': user_challenges_dict,
    })


def remove_workout(request):
    if request.method == "POST":
        workout_id = request.POST.get("workout_id")
        workout = get_object_or_404(Workout, id=workout_id)

        user_workout = UserWorkout.objects.filter(user=request.user, workout=workout).first()
        if user_workout:
            user_workout.delete()
            return JsonResponse({'status': 'removed'})
        else:
            return JsonResponse({'status': 'not_found'}, status=404)


def remove_challenge(request):
    if request.method == "POST":
        challenge_id = request.POST.get("challenge_id")
        challenge = get_object_or_404(Challenge, id=challenge_id)

        user_challenge = UserChallenge.objects.filter(user=request.user, challenge=challenge).first()
        if user_challenge:
            user_challenge.delete()
            return JsonResponse({'status': 'removed'})
        else:
            return JsonResponse({'status': 'not_found'}, status=404)

@login_required
@require_POST
def update_progress(request):
    user_challenge_id = request.POST.get('user_challenge_id')
    delta = int(request.POST.get('delta', 0))

    user_challenge = get_object_or_404(UserChallenge, id=user_challenge_id, user=request.user)

    new_progress = user_challenge.progress + delta
    if new_progress < 0:
        new_progress = 0
    elif new_progress > user_challenge.challenge.duration:
        new_progress = user_challenge.challenge.duration

    user_challenge.progress = new_progress
    user_challenge.save()

    return JsonResponse({'status': 'success', 'new_progress': new_progress})
