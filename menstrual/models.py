from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta

User = get_user_model()


class MenstrualProfile(models.Model):
    """User's menstrual cycle baseline settings"""
    PREGNANCY_GOAL_CHOICES = [
        ('avoid', 'Avoid Pregnancy'),
        ('conceive', 'Trying to Conceive'),
        ('track', 'Just Tracking'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='menstrual_profile')
    last_period_start = models.DateField(help_text="Day 1 of the last menstrual period")
    avg_cycle_length = models.IntegerField(default=28, help_text="Average cycle length in days")
    avg_period_length = models.IntegerField(default=5, help_text="Average bleeding duration in days")
    pregnancy_goal = models.CharField(max_length=10, choices=PREGNANCY_GOAL_CHOICES, default='track')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Menstrual Profile"
        verbose_name_plural = "Menstrual Profiles"

    def __str__(self):
        return f"{self.user.username} - Menstrual Cycle"

    def get_current_cycle_day(self, date=None):
        """Calculate which day of cycle the given date falls on (1-indexed)"""
        if date is None:
            date = datetime.now().date()
        days_since_start = (date - self.last_period_start).days
        cycle_day = (days_since_start % self.avg_cycle_length) + 1
        return cycle_day

    def get_cycle_phase(self, cycle_day):
        """Return the phase name for a given cycle day"""
        period_end = self.avg_period_length
        follicular_end = int(self.avg_cycle_length * 0.46)
        ovulation_day = int(self.avg_cycle_length * 0.5)

        if cycle_day <= period_end:
            return 'menstrual'
        elif cycle_day <= follicular_end:
            return 'follicular'
        elif cycle_day <= ovulation_day + 1:
            return 'ovulation'
        else:
            return 'luteal'

    def get_fertility_level(self, cycle_day):
        """Return fertility level: 'high', 'medium', 'low'"""
        high_start = int(self.avg_cycle_length * 0.36)
        high_end = int(self.avg_cycle_length * 0.54)

        if high_start <= cycle_day <= high_end:
            return 'high'
        elif high_start - 2 <= cycle_day <= high_end + 2:
            return 'medium'
        else:
            return 'low'

    def get_next_period_estimate(self):
        """Estimate the next period start date"""
        return self.last_period_start + timedelta(days=self.avg_cycle_length)


class CycleDay(models.Model):
    """Calculated cycle information for each day"""
    PHASE_CHOICES = [
        ('menstrual', 'Menstrual'),
        ('follicular', 'Follicular'),
        ('ovulation', 'Ovulation'),
        ('luteal', 'Luteal'),
    ]

    FERTILITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cycle_days')
    date = models.DateField()
    cycle_day_number = models.IntegerField(help_text="Day 1-N of cycle")
    phase = models.CharField(max_length=15, choices=PHASE_CHOICES)
    fertility_level = models.CharField(max_length=10, choices=FERTILITY_CHOICES)

    class Meta:
        unique_together = ('user', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} - {self.date} (Day {self.cycle_day_number})"


class DailyLog(models.Model):
    """Daily symptom and bleeding logging"""
    BLEEDING_CHOICES = [
        ('none', 'None'),
        ('spotting', 'Spotting'),
        ('light', 'Light'),
        ('medium', 'Medium'),
        ('heavy', 'Heavy'),
    ]

    MOOD_CHOICES = [
        ('great', 'Great'),
        ('good', 'Good'),
        ('neutral', 'Neutral'),
        ('low', 'Low'),
        ('sad', 'Sad'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='menstrual_logs')
    date = models.DateField()
    bleeding_level = models.CharField(max_length=10, choices=BLEEDING_CHOICES, default='none')
    pain_score = models.IntegerField(default=0, help_text="0-5 scale")
    mood = models.CharField(max_length=10, choices=MOOD_CHOICES, null=True, blank=True)
    notes = models.TextField(blank=True)
    symptoms = models.JSONField(default=list, help_text="List of symptoms")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} - {self.date} ({self.bleeding_level})"


class CycleInsight(models.Model):
    """AI-generated insights and patterns"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cycle_insights')
    insight_type = models.CharField(
        max_length=20,
        choices=[
            ('pattern', 'Pattern'),
            ('daily_guidance', 'Daily Guidance'),
            ('alert', 'Alert'),
        ]
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} - {self.insight_type}: {self.title}"
