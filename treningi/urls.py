from .views import home_view, register_view, login_view, logout_view, home_page_view, do_workout, user_profile_page_view, ranking_view
from django.urls import path, include

urlpatterns = [
    path('', home_view, name='home'),
    path('register/', register_view, name='register'),
    path('login', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('home_page/', home_page_view, name='home_page'),
    path('do_workout/', do_workout, name='do_workout'),
    path('user_profile_page/', user_profile_page_view, name='user_profile_page'),
    path('ranking_page/', ranking_view, name='ranking_page'),
]
