from datetime import date

def get_health_advice(user):
    profile = user.profile
    age = (date.today() - profile.date_of_birth).days // 365
    
    # Simple logic for the MVP
    if age < 12:
        return "Focus on developmental milestones and vaccinations."
    elif profile.health_focus == 'MATERNAL':
        return "Ensure you are tracking iron and calcium intake today."
    elif age > 46:
        return "Prioritize joint health and regular blood pressure checks."
    else:
        return "Stay active! Aim for 10,000 steps today."