"""Menstrual cycle tracking forms"""
from django import forms
from .models import DailyLog, MenstrualProfile
from datetime import datetime


class MenstrualProfileForm(forms.ModelForm):
    """Form for setting up menstrual profile"""
    
    last_period_start = forms.DateField(
        label='Last Period Start Date',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control animated-input',
            'placeholder': 'YYYY-MM-DD'
        }),
        help_text='When did your last menstrual period start?'
    )
    
    avg_cycle_length = forms.IntegerField(
        label='Average Cycle Length (days)',
        initial=28,
        min_value=20,
        max_value=45,
        widget=forms.NumberInput(attrs={
            'class': 'form-control animated-input',
            'placeholder': '28'
        }),
        help_text='Typical cycle is 28 days (normal range: 21-35)'
    )
    
    avg_period_length = forms.IntegerField(
        label='Average Period Length (days)',
        initial=5,
        min_value=2,
        max_value=10,
        widget=forms.NumberInput(attrs={
            'class': 'form-control animated-input',
            'placeholder': '5'
        }),
        help_text='How many days does your period typically last?'
    )
    
    pregnancy_goal = forms.ChoiceField(
        label='Pregnancy Goal',
        choices=[
            ('track', 'Track only (not trying to conceive or avoid)'),
            ('conceive', 'Trying to conceive'),
            ('avoid', 'Trying to avoid pregnancy'),
        ],
        required=False,
        initial='track',
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input'
        }),
        help_text='This helps personalize guidance and fertility information'
    )
    
    class Meta:
        model = MenstrualProfile
        fields = ['last_period_start', 'avg_cycle_length', 'avg_period_length']


class DailyLogForm(forms.ModelForm):
    """Form for logging daily menstrual data"""
    
    BLEEDING_CHOICES = [
        ('none', 'None'),
        ('spotting', 'Spotting'),
        ('light', 'Light'),
        ('medium', 'Medium'),
        ('heavy', 'Heavy'),
    ]
    
    MOOD_CHOICES = [
        ('happy', '😊 Happy'),
        ('neutral', '😐 Neutral'),
        ('sad', '😢 Sad'),
        ('anxious', '😰 Anxious'),
        ('irritable', '😠 Irritable'),
    ]
    
    date = forms.DateField(
        label='Date',
        initial=datetime.now().date(),
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control animated-input',
        }),
        required=False
    )
    
    bleeding_level = forms.ChoiceField(
        label='Bleeding Level',
        choices=BLEEDING_CHOICES,
        initial='none',
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input bleeding-radio'
        }),
        help_text='Select your bleeding intensity'
    )
    
    pain_score = forms.IntegerField(
        label='Pain Score',
        initial=0,
        min_value=0,
        max_value=5,
        widget=forms.NumberInput(attrs={
            'type': 'range',
            'class': 'form-range animated-range',
            'min': '0',
            'max': '5',
            'id': 'painSlider'
        }),
        help_text='0 = No pain, 5 = Severe pain'
    )
    
    mood = forms.ChoiceField(
        label='Mood',
        choices=MOOD_CHOICES,
        required=False,
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input mood-radio'
        }),
        help_text='How are you feeling today?'
    )
    
    notes = forms.CharField(
        label='Notes',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control animated-input',
            'placeholder': 'Add any additional notes or observations...',
            'rows': 4
        }),
        help_text='Optional: Any symptoms, observations, or notes'
    )
    
    class Meta:
        model = DailyLog
        fields = ['date', 'bleeding_level', 'pain_score', 'mood', 'notes']
        exclude = ['user', 'symptoms']
