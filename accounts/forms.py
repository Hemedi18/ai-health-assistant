"""
Django Forms for Authentication and User Management
"""

from django import forms
from django.contrib.auth import authenticate
from .models import (
    User, Profile, HealthVital, NutritionEntry, Exercise,
    MoodEntry, SleepEntry, Medication
)


HEALTH_FOCUS_CHOICES = [
    ('MATERNAL', 'Maternal'),
    ('CHILD', 'Child'),
    ('GENERAL', 'General'),
]

GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
]


class UserLoginForm(forms.Form):
    """Login form with phone number"""
    u_phone_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Phone Number (e.g., +255 7XX XXX XXX)',
            'autofocus': True,
        }),
        label='Phone Number'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Password',
        }),
        label='Password'
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        }),
        label='Remember me'
    )

    def clean(self):
        cleaned_data = super().clean()
        u_phone_number = cleaned_data.get('u_phone_number')
        password = cleaned_data.get('password')

        if u_phone_number and password:
            # Try to authenticate the user
            user = authenticate(username=u_phone_number, password=password)
            if user is None:
                raise forms.ValidationError("Invalid phone number or password")
        
        return cleaned_data



class UserRegistrationForm(forms.Form):
    """Registration form for new users"""
    u_phone_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Phone Number (+255 7XX XXX XXX)',
        }),
        label='Phone Number'
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Password (min 8 characters)',
        }),
        min_length=8,
        label='Password'
    )
    
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Confirm Password',
        }),
        label='Confirm Password'
    )
    
    health_focus = forms.ChoiceField(
        choices=HEALTH_FOCUS_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control form-control-lg',
        }),
        label='Health Focus Area',
        initial='GENERAL'
    )
    
    def clean_u_phone_number(self):
        u_phone_number = self.cleaned_data.get('u_phone_number')
        if User.objects.filter(u_phone_number=u_phone_number).exists():
            raise forms.ValidationError("Phone number already registered")
        return u_phone_number
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match")
        
        return cleaned_data


class UserProfileForm(forms.ModelForm):
    """User Profile form"""
    class Meta:
        model = Profile
        fields = ['health_focus', 'date_of_birth', 'blood_group']
        widgets = {
            'health_focus': forms.Select(attrs={'class': 'form-control'}, choices=HEALTH_FOCUS_CHOICES),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'blood_group': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., O+'}),
        }


class HealthVitalForm(forms.ModelForm):
    class Meta:
        model = HealthVital
        fields = ['weight', 'height', 'blood_pressure_sys', 'blood_pressure_dia', 'heart_rate']
        widgets = {
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'kg'}),
            'height': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'cm'}),
            'blood_pressure_sys': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Systolic (e.g. 120)'}),
            'blood_pressure_dia': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Diastolic (e.g. 80)'}),
            'heart_rate': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'BPM'}),
        }

class NutritionEntryForm(forms.ModelForm):
    class Meta:
        model = NutritionEntry
        fields = ['meal_type', 'food_items', 'calories', 'protein_g', 'carbs_g', 'fat_g']
        widgets = {
            'meal_type': forms.Select(attrs={'class': 'form-control'}),
            'food_items': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'e.g., Rice, Beans, Spinach'}),
            'calories': forms.NumberInput(attrs={'class': 'form-control'}),
            'protein_g': forms.NumberInput(attrs={'class': 'form-control'}),
            'carbs_g': forms.NumberInput(attrs={'class': 'form-control'}),
            'fat_g': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['exercise_type', 'intensity', 'duration_minutes', 'calories_burned', 'notes']
        widgets = {
            'exercise_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Running, Yoga'}),
            'intensity': forms.Select(attrs={'class': 'form-control'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control'}),
            'calories_burned': forms.NumberInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class MoodEntryForm(forms.ModelForm):
    class Meta:
        model = MoodEntry
        fields = ['mood', 'triggers', 'anxiety_level', 'stress_level', 'notes']
        widgets = {
            'mood': forms.Select(attrs={'class': 'form-control'}),
            'triggers': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Work, Family'}),
            'anxiety_level': forms.NumberInput(attrs={'class': 'form-control', 'type': 'range', 'min': 0, 'max': 10}),
            'stress_level': forms.NumberInput(attrs={'class': 'form-control', 'type': 'range', 'min': 0, 'max': 10}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class SleepEntryForm(forms.ModelForm):
    class Meta:
        model = SleepEntry
        fields = ['bed_time', 'wake_time', 'sleep_duration_hours', 'sleep_quality', 'notes']
        widgets = {
            'bed_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'wake_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'sleep_duration_hours': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'sleep_quality': forms.NumberInput(attrs={'class': 'form-control', 'type': 'range', 'min': 1, 'max': 10}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class MedicationForm(forms.ModelForm):
    class Meta:
        model = Medication
        fields = ['medication_name', 'dosage', 'frequency', 'reason', 'start_date', 'end_date', 'notes']
        widgets = {
            'medication_name': forms.TextInput(attrs={'class': 'form-control'}),
            'dosage': forms.TextInput(attrs={'class': 'form-control'}),
            'frequency': forms.Select(attrs={'class': 'form-control'}),
            'reason': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
