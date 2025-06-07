from .views import home_view, register_view, login_view, logout_view, log_workout_view, available_workouts, add_workout, \
    available_challenges, add_challenge, toggle_workout, toggle_challenge, user_workouts_and_challenges, \
    remove_workout, remove_challenge, update_progress
from django.urls import path, include

urlpatterns = [
    path('', home_view, name='home'),
    path('register/', register_view, name='register'),
    path('users/login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('log-workout/', log_workout_view, name='log_workout'),

    # Treningi
    path('workouts/', available_workouts, name='available_workouts'),
    path('workouts/add/<int:workout_id>/', add_workout, name='add_workout'),

    # Wyzwania
    path('challenges/', available_challenges, name='available_challenges'),
    path('challenges/add/<int:challenge_id>/', add_challenge, name='add_challenge'),

    path('toggle-workout/', toggle_workout, name='toggle_workout'),
    path('toggle-challenge', toggle_challenge, name='toggle_challenge'),

    #path('admin/challenge-history/', challenge_history, name='challenge_history'),
    path('user_workouts_and_challenges/', user_workouts_and_challenges, name='user_workouts_and_challenges'),
    path('remove_workout/', remove_workout, name='remove_workout'),
    path('remove_challenge/', remove_challenge, name='remove_challenge'),

    path('update_progress/', update_progress, name='update_progress'),
]