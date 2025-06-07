from django import forms
from .models import Exercise, Category, MuscleGroup, Challenge
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from .models import LoggedWorkout, Workout, WorkoutExercise, UserWorkout, UserChallenge

User = get_user_model()

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['name', 'description', 'category', 'muscle_groups', 'image']

    category = forms.ModelChoiceField(
        queryset=Category.objects.all()
    )

    muscle_groups = forms.ModelMultipleChoiceField(
        queryset=MuscleGroup.objects.all(),
        widget=forms.CheckboxSelectMultiple  # możesz zmienić na np. SelectMultiple jeśli chcesz rozwijaną listę
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
        self.fields['category'].label_from_instance = self.category_label_with_description
        self.fields['muscle_groups'].queryset = MuscleGroup.objects.all()
        self.fields['muscle_groups'].label_from_instance = lambda obj: f"{obj.name} — {obj.description}"

    def category_label_with_description(self, obj):
        return f"{obj.name} — {obj.description}"

class ChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenge
        fields = ['name', 'description', 'start_date', 'end_date', 'goal', 'difficulty_level', 'duration']

    exercise = forms.ModelChoiceField(
        queryset=Exercise.objects.all(),
        required=False,
        label="Wybierz ćwiczenie z listy"
    )


    def clean(self):
        cleaned_data = super().clean()
        exercise = cleaned_data.get('exercise')

        if exercise:
            raise forms.ValidationError("Nie możesz wybrać ćwiczenia z listy i jednocześnie podać własnego ćwiczenia.")

        return cleaned_data

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="Nazwa użytkownika",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="Hasło",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError("To konto jest nieaktywne.", code='inactive')

class LoggedWorkoutForm(forms.ModelForm):
    class Meta:
        model = LoggedWorkout
        fields = ['workout']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pokazuj tylko treningi dodane przez administratora
        self.fields['workout'].queryset = Workout.objects.all()

class WorkoutExerciseForm(forms.ModelForm):
    class Meta:
        model = WorkoutExercise
        fields = ['workout', 'exercise', 'duration_minutes', 'repetitions', 'sets', 'weight']

# class ChallengeExerciseForm(forms.ModelForm):
#     class Meta:
#         model = ChallengeExercise
#         fields = ['challenge', 'exercise', 'duration_minutes', 'repetitions', 'sets', 'weight']

#dodane 20.20 12.05.2025

class UserWorkoutForm(forms.ModelForm):
    class Meta:
        model = UserWorkout
        fields = ['workout']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['workout'].queryset = Workout.objects.filter(user=user)  # Tylko dostępne treningi dla użytkownika

class UserChallengeForm(forms.ModelForm):
    class Meta:
        model = UserChallenge
        fields = ['challenge']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['challenge'].queryset = Challenge.objects.filter(user=user)  # Tylko dostępne wyzwania dla użytkownika