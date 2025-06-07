from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from .models import Workout,Category, MuscleGroup, Exercise, Challenge, LoggedWorkout, \
    PersonalRecord, UserProgress, Notification, WorkoutStatistics, AdminReport, \
    DifficultyLevel, Comment, CommentRating, ProfilePicture, UserSession, WorkoutExercise, \
    LoggedWorkoutExercise, UserWorkout, UserChallenge, ChallengeHistory, WorkoutHistory

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('date_joined',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Dane osobiste', {'fields': ('email',)}),
        ('Uprawnienia', {'fields': ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),
        ('Daty', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

class WorkoutExerciseInline(admin.TabularInline):
    model = WorkoutExercise
    extra = 1  # Liczba dodatkowych pustych formularzy
    fields = ('exercise', 'duration_minutes', 'repetitions', 'sets', 'weight')  # Pola do wyświetlenia w formularzu

@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'difficulty_level']
    search_fields = ['name']
    list_filter = ['difficulty_level']
    inlines = [WorkoutExerciseInline]


admin.site.register(Category)

@admin.register(MuscleGroup)
class MuscleGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']  # Dostosuj według swoich potrzeb
    search_fields = ['name']

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    search_fields = ['name', 'category__name']
    list_filter = ['category', 'muscle_groups']
    filter_horizontal = ('muscle_groups',)


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'end_date', 'goal', 'difficulty_level', 'duration']
    search_fields = ['name']


@admin.register(LoggedWorkout)
class LoggedWorkoutAdmin(admin.ModelAdmin):
    list_display = ['user', 'workout', 'date_logged', 'duration_minutes', 'repetitions', 'sets']
    search_fields = ['user__username', 'workout__name']
    list_filter = ['workout', 'user', 'date_logged']
    fields = ('user', 'workout', 'date_logged', 'duration_minutes', 'repetitions', 'sets', 'comment')  # Dodajemy pola


@admin.register(PersonalRecord)
class PersonalRecordAdmin(admin.ModelAdmin):
    list_display = ['user', 'exercise', 'record_value', 'unit', 'date_achieved']
    search_fields = ['user__username', 'exercise__name']
    list_filter = ['exercise', 'record_value']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'notification_type', 'message', 'date_created', 'is_read']
    search_fields = ['user__username', 'notification_type']
    list_filter = ['is_read', 'notification_type', 'date_created']


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'workout', 'completed_sessions', 'total_time_spent', 'goals_achieved', 'last_updated']
    search_fields = ['user__username', 'workout__name']
    list_filter = ['workout', 'user', 'completed_sessions', 'total_time_spent']


@admin.register(WorkoutStatistics)
class WorkoutStatisticsAdmin(admin.ModelAdmin):
    list_display = ['user', 'workout', 'repetitions', 'duration', 'calories_burned', 'workout_date']
    search_fields = ['user__username', 'workout__name']
    list_filter = ['workout', 'user', 'calories_burned']


@admin.register(AdminReport)
class AdminReportAdmin(admin.ModelAdmin):
    list_display = ['admin_user', 'report_type', 'date_created', 'date_displayed']
    search_fields = ['admin_user__username', 'report_type']
    list_filter = ['report_type', 'date_created', 'date_displayed']


@admin.register(DifficultyLevel)
class DifficultyLevelAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'workout', 'text', 'created_at']
    search_fields = ['user__username', 'workout__name', 'text']
    list_filter = ['workout', 'created_at']


@admin.register(CommentRating)
class CommentRatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'comment', 'rating', 'date_created']
    search_fields = ['user__username', 'comment__id']
    list_filter = ['rating', 'date_created']


admin.site.register(ProfilePicture)


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'session_key', 'created_at', 'expired_at']
    search_fields = ['user__username', 'session_key']
    list_filter = ['created_at', 'expired_at']

@admin.register(WorkoutExercise)
class WorkoutExerciseAdmin(admin.ModelAdmin):
    list_display = ['workout', 'exercise', 'duration_minutes', 'repetitions', 'sets', 'weight']

# @admin.register(ChallengeExercise)
# class ChallengeExerciseAdmin(admin.ModelAdmin):
#     list_display = ['challenge', 'exercise', 'duration_minutes', 'repetitions', 'sets', 'weight']

@admin.register(LoggedWorkoutExercise)
class LoggedWorkoutExerciseAdmin(admin.ModelAdmin):
    list_display = ['user', 'workout_exercise', 'duration_minutes', 'repetitions', 'sets', 'weight']
    search_fields = ['user__username', 'workout_exercise__exercise__name']
    list_filter = ['workout_exercise__workout', 'user']
    fields = ('user', 'workout_exercise', 'duration_minutes', 'repetitions', 'sets', 'weight')

@admin.register(UserWorkout)
class UserWorkoutAdmin(admin.ModelAdmin):
    list_display = ('user', 'workout', 'added_at')  # zamiast 'date_assigned'

@admin.register(UserChallenge)
class UserChallengeAdmin(admin.ModelAdmin):
    list_display = ('user', 'challenge', 'added_at')  # zamiast 'date_assigned'
    #dodane 00:57
    search_fields = ('user__username', 'challenge__name')
    list_filter = ('added_at',)


admin.site.register(ChallengeHistory)

admin.site.register(WorkoutHistory)


