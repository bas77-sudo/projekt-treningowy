from django import forms
from .models import Exercise, Category, MuscleGroup, Challenge
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
# dwie linijki dodane
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

User = get_user_model()

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['name', 'description', 'category', 'muscle_groups','duration_minutes', 'repetitions', 'sets', 'weight', 'image']

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
        fields = ['name', 'description', 'start_date', 'end_date', 'goal', 'difficulty_level', 'exercise']

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
# dodane 5 linijek
class CustomAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError("To konto jest nieaktywne.", code='inactive')
        # Można dodać inne warunki, np. sprawdzenie roli użytkownika itd.
