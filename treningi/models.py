from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)

    @property
    def profile_picture(self):
        return getattr(self, 'profile_picture_relation', None)

class MuscleGroup(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class ProfilePicture(models.Model):
    user = models.OneToOneField(
        'User',
        on_delete=models.CASCADE,
        related_name='profile_picture_relation'
    )
    image = models.ImageField(upload_to='profile_pictures/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Profile picture of {self.user.username}'

class DifficultyLevel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Exercise(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    muscle_groups = models.ManyToManyField(MuscleGroup, blank=True)
    image = models.ImageField(upload_to='exercises/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class WorkoutExercise(models.Model):
    workout = models.ForeignKey('Workout', on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)
    repetitions = models.PositiveIntegerField(null=True, blank=True)
    sets = models.PositiveIntegerField(null=True, blank=True)
    weight = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.workout.name} - {self.exercise.name}"

# class ChallengeExercise(models.Model):
#     challenge = models.ForeignKey('Challenge', on_delete=models.CASCADE)
#     exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
#     duration_minutes = models.PositiveIntegerField(null=True, blank=True)
#     repetitions = models.PositiveIntegerField(null=True, blank=True)
#     sets = models.PositiveIntegerField(null=True, blank=True)
#     weight = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
#
#     def __str__(self):
#         return f"{self.challenge.name} - {self.exercise.name}"


class Workout(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    difficulty_level = models.ForeignKey(DifficultyLevel, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='workouts/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Challenge(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    goal = models.CharField(max_length=255)
    # exercise = models.ForeignKey(Exercise, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    difficulty_level = models.CharField(max_length=50, choices=[
        ('easy', 'Łatwy'),
        ('medium', 'Średni'),
        ('hard', 'Trudny'),
    ])
    duration = models.IntegerField(default=1, help_text="Czas trwania w dniach")

    def __str__(self):
        return self.name


class LoggedWorkout(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    date_logged = models.DateTimeField(auto_now_add=True)
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)
    repetitions = models.PositiveIntegerField(null=True, blank=True)
    sets = models.PositiveIntegerField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} - {self.workout.name} - {self.date_logged}'

class PersonalRecord(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    record_value = models.FloatField()
    unit = models.CharField(max_length=50)
    date_achieved = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.exercise.name} - {self.record_value} {self.unit}'


class UserProgress(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    completed_sessions = models.PositiveIntegerField(default=0)
    total_time_spent = models.PositiveIntegerField(default=0)  # czas w minutach
    goals_achieved = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} - {self.workout.name} - {self.completed_sessions} sessions'

class Notification(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=100)
    message = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    date_read = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Notification for {self.user.username} - {self.notification_type}'


class WorkoutStatistics(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    repetitions = models.PositiveIntegerField(default=0)
    duration = models.PositiveIntegerField(default=0)  # czas w minutach
    calories_burned = models.PositiveIntegerField(default=0)
    workout_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.workout.name} - {self.workout_date.strftime("%Y-%m-%d %H:%M:%S")}'

class AdminReport(models.Model):
    admin_user = models.ForeignKey('User', on_delete=models.CASCADE)
    report_type = models.CharField(max_length=100)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_displayed = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Report by {self.admin_user.username} on {self.date_created.strftime("%Y-%m-%d %H:%M:%S")}'


class Comment(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.workout.name}'



class CommentRating(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} rated {self.comment.id} with {self.rating}'

class UserSession(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='sessions')
    session_key = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Session {self.session_key} for {self.user.username}'

class LoggedWorkoutExercise(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workout_exercise = models.ForeignKey(WorkoutExercise, on_delete=models.CASCADE)
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)
    repetitions = models.PositiveIntegerField(null=True, blank=True)
    sets = models.PositiveIntegerField(null=True, blank=True)
    weight = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.workout_exercise.exercise.name} ({self.created_at})"

class UserWorkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.workout.name}"

class UserChallenge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    progress = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.challenge.name} (Progress: {self.progress})"


class ChallengeHistory(models.Model):
    ACTION_CHOICES = [
        ('created', 'Utworzono'),
        ('deleted', 'Usunięto'),
        ('updated', 'Zaktualizowano'),
    ]

    admin_user = models.ForeignKey('User', on_delete=models.CASCADE)
    challenge = models.ForeignKey('Challenge', on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    action_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.admin_user.username} {self.action} {self.challenge.name} at {self.action_date}"


class WorkoutHistory(models.Model):
    ACTION_CHOICES = [
        ('added', 'Dodano'),
        ('removed', 'Usunięto'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    action = models.CharField(max_length=7, choices=ACTION_CHOICES)
    action_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} {self.action} {self.workout.name} on {self.action_date}"