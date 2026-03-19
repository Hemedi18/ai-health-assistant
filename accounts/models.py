from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid

# This class handles how users are created
class UserManager(BaseUserManager):
    def create_user(self, u_phone_number, password=None):
        if not u_phone_number:
            raise ValueError("Users must have a phone number")
        user = self.model(u_phone_number=u_phone_number)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, u_phone_number, password=None):
        user = self.create_user(u_phone_number, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# This is your main User model
class User(AbstractBaseUser, PermissionsMixin):
    u_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    u_phone_number = models.CharField(max_length=15, unique=True)
    trial_start = models.DateTimeField(auto_now_add=True)
    is_premium = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    # Required for Django Admin
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) 

    objects = UserManager()

    USERNAME_FIELD = 'u_phone_number' # Log in using phone number
    REQUIRED_FIELDS = [] # Nothing else is required to create a user

    def __str__(self):
        return self.u_phone_number

class Profile(models.Model):
    FOCUS_CHOICES = [
        ('MATERNAL', 'Maternal'),
        ('CHILD', 'Child'),
        ('GENERAL', 'General'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    health_focus = models.CharField(max_length=10, choices=FOCUS_CHOICES, default='GENERAL')
    date_of_birth = models.DateField(null=True, blank=True)
    blood_group = models.CharField(max_length=5, null=True, blank=True)

    def __str__(self):
        return f"Profile for {self.user.u_phone_number}"
    
# --- Existing User and Profile models remain above ---

class HealthVital(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vitals')
    recorded_at = models.DateTimeField(auto_now_add=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True) # kg
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True) # cm
    blood_pressure_sys = models.IntegerField(null=True, blank=True)
    blood_pressure_dia = models.IntegerField(null=True, blank=True)
    heart_rate = models.IntegerField(null=True, blank=True)
    
    @property
    def bmi(self):
        if self.weight and self.height:
            # Formula: weight (kg) / [height (m)]^2
            height_m = self.height / 100
            return round(float(self.weight) / (float(height_m) ** 2), 2)
        return None

class MedicalHistory(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    allergies = models.TextField(blank=True)
    chronic_conditions = models.TextField(blank=True) # e.g. Asthma, Diabetes
    family_history = models.TextField(blank=True)

class ChildProfile(models.Model):
    parent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='children')
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    vaccination_status = models.TextField(blank=True)


# ==================== NUTRITION & DIET ====================

class NutritionEntry(models.Model):
    MEAL_TYPE_CHOICES = [
        ('BREAKFAST', 'Breakfast'),
        ('LUNCH', 'Lunch'),
        ('DINNER', 'Dinner'),
        ('SNACK', 'Snack'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='nutrition_entries')
    meal_type = models.CharField(max_length=10, choices=MEAL_TYPE_CHOICES)
    recorded_at = models.DateTimeField(auto_now_add=True)
    food_items = models.TextField()  # JSON: [{"name": "rice", "quantity": "2 cups"}]
    calories = models.IntegerField(null=True, blank=True)
    protein_g = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    carbs_g = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    fat_g = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    fiber_g = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-recorded_at']


class DailyNutritionGoal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='nutrition_goal')
    target_calories = models.IntegerField(default=2000)
    target_protein_g = models.IntegerField(default=50)
    target_carbs_g = models.IntegerField(default=300)
    target_fat_g = models.IntegerField(default=65)
    target_fiber_g = models.IntegerField(default=25)
    target_water_ml = models.IntegerField(default=2000)
    special_diet = models.CharField(max_length=50, blank=True)  # diabetic, low-salt, etc.
    last_updated = models.DateTimeField(auto_now=True)


class WaterIntake(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='water_intake')
    recorded_at = models.DateTimeField(auto_now_add=True)
    amount_ml = models.IntegerField()

    class Meta:
        ordering = ['-recorded_at']


# ==================== PHYSICAL ACTIVITY & FITNESS ====================

class Exercise(models.Model):
    INTENSITY_CHOICES = [
        ('LOW', 'Low'),
        ('MODERATE', 'Moderate'),
        ('HIGH', 'High'),
        ('VERY_HIGH', 'Very High'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exercises')
    exercise_type = models.CharField(max_length=100)  # Running, Swimming, Yoga, etc.
    intensity = models.CharField(max_length=10, choices=INTENSITY_CHOICES)
    duration_minutes = models.IntegerField()
    calories_burned = models.IntegerField(null=True, blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-recorded_at']


class DailySteps(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_steps')
    recorded_date = models.DateField(auto_now_add=True, db_index=True)
    steps = models.IntegerField()
    distance_km = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    class Meta:
        unique_together = ['user', 'recorded_date']
        ordering = ['-recorded_date']


class FitnessGoal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='fitness_goal')
    target_steps_daily = models.IntegerField(default=10000)
    target_exercise_minutes_weekly = models.IntegerField(default=150)
    target_workouts_weekly = models.IntegerField(default=3)
    last_updated = models.DateTimeField(auto_now=True)


# ==================== MENTAL HEALTH & WELL-BEING ====================

class MoodEntry(models.Model):
    MOOD_CHOICES = [
        ('EXCELLENT', 'Excellent 😄'),
        ('GOOD', 'Good 😊'),
        ('NEUTRAL', 'Neutral 😐'),
        ('POOR', 'Poor 😞'),
        ('VERY_POOR', 'Very Poor 😢'),
    ]
    
    TRIGGER_CHOICES = [
        ('WORK', 'Work stress'),
        ('RELATIONSHIP', 'Relationship'),
        ('HEALTH', 'Health concerns'),
        ('FINANCES', 'Financial stress'),
        ('FAMILY', 'Family issues'),
        ('SOCIAL', 'Social pressure'),
        ('OTHER', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mood_entries')
    mood = models.CharField(max_length=10, choices=MOOD_CHOICES)
    triggers = models.CharField(max_length=200, blank=True)  # Comma-separated or JSON
    anxiety_level = models.IntegerField(default=0, help_text="0-10 scale")
    stress_level = models.IntegerField(default=0, help_text="0-10 scale")
    notes = models.TextField(blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-recorded_at']


class SleepEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sleep_entries')
    sleep_duration_hours = models.DecimalField(max_digits=3, decimal_places=1)
    sleep_quality = models.IntegerField(default=5, help_text="1-10 scale")
    bed_time = models.TimeField()
    wake_time = models.TimeField()
    recorded_date = models.DateField(auto_now_add=True, db_index=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-recorded_date']


class MindfulnessSession(models.Model):
    SESSION_TYPE_CHOICES = [
        ('MEDITATION', 'Meditation'),
        ('BREATHING', 'Breathing Exercise'),
        ('YOGA', 'Yoga'),
        ('STRETCHING', 'Stretching'),
        ('JOURNALING', 'Journaling'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mindfulness_sessions')
    session_type = models.CharField(max_length=20, choices=SESSION_TYPE_CHOICES)
    duration_minutes = models.IntegerField()
    feeling_before = models.CharField(max_length=100, blank=True)
    feeling_after = models.CharField(max_length=100, blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-recorded_at']


# ==================== MEDICATION & TREATMENT ====================

class Medication(models.Model):
    FREQUENCY_CHOICES = [
        ('ONCE_DAILY', 'Once daily'),
        ('TWICE_DAILY', 'Twice daily'),
        ('THRICE_DAILY', 'Three times daily'),
        ('FOUR_TIMES_DAILY', 'Four times daily'),
        ('WEEKLY', 'Weekly'),
        ('MONTHLY', 'Monthly'),
        ('AS_NEEDED', 'As needed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medications')
    medication_name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    reason = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    side_effects = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-start_date']


class MedicationReminder(models.Model):
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE, related_name='reminders')
    reminder_time = models.TimeField()
    is_active = models.BooleanField(default=True)


class MedicationAdherence(models.Model):
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE, related_name='adherence')
    scheduled_date = models.DateField()
    was_taken = models.BooleanField()
    time_taken = models.TimeField(null=True, blank=True)
    skipped_reason = models.CharField(max_length=200, blank=True)

    class Meta:
        unique_together = ['medication', 'scheduled_date']
        ordering = ['-scheduled_date']


class MedicalAppointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    doctor_name = models.CharField(max_length=100)
    clinic_name = models.CharField(max_length=100)
    appointment_date = models.DateTimeField()
    reason = models.CharField(max_length=200)
    notes = models.TextField(blank=True)
    reminder_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['appointment_date']


# ==================== BLOOD SUGAR TRACKING (For Diabetes) ====================

class BloodSugarEntry(models.Model):
    MEASUREMENT_TIME_CHOICES = [
        ('FASTING', 'Fasting (before meal)'),
        ('POSTPRANDIAL', 'Post-prandial (after meal)'),
        ('BEDTIME', 'Bedtime'),
        ('RANDOM', 'Random'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blood_sugar_entries')
    blood_sugar_mg_dl = models.IntegerField()
    measurement_time = models.CharField(max_length=15, choices=MEASUREMENT_TIME_CHOICES)
    recorded_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-recorded_at']


# ==================== HEALTH REPORT & INSIGHTS ====================

class HealthReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='health_reports')
    report_date = models.DateField(auto_now_add=True)
    
    # Summary data
    avg_weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    avg_blood_pressure = models.CharField(max_length=10, blank=True)  # "120/80"
    avg_heart_rate = models.IntegerField(null=True, blank=True)
    avg_blood_sugar = models.IntegerField(null=True, blank=True)
    total_calories = models.IntegerField(null=True, blank=True)
    total_exercise_minutes = models.IntegerField(null=True, blank=True)
    total_steps = models.IntegerField(null=True, blank=True)
    avg_mood_score = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    avg_sleep_hours = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    
    # Risk indicators
    health_risks = models.TextField(blank=True)  # JSON: ["high_bp", "low_activity"]
    recommendations = models.TextField(blank=True)  # JSON recommendations
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-report_date']