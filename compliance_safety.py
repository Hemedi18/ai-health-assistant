"""
Health App Compliance & Safety Module
=====================================

This module handles all health disclaimers, safety protocols, and ethical guidelines
for the health management application.

CRITICAL: This app is for health tracking and education ONLY, not medical diagnosis.
"""

# ==================== HEALTH DISCLAIMER ====================

HEALTH_DISCLAIMER_FULL = """
⚠️ **IMPORTANT HEALTH AND SAFETY DISCLAIMER** ⚠️

THIS APPLICATION IS NOT A MEDICAL DIAGNOSIS TOOL

This health management application (Afya Yako AI) is designed as a personal health tracking
and educational tool ONLY. It is NOT a substitute for professional medical advice, diagnosis,
or treatment.

## What This App IS:
✅ A health data tracking and logging tool
✅ A source of general health information and education
✅ A wellness companion for personal health management
✅ A reminder system for medications and appointments
✅ An AI-powered health insight and recommendation engine

## What This App IS NOT:
❌ A medical diagnosis tool
❌ A substitute for professional healthcare providers
❌ Licensed to treat, cure, or manage diseases
❌ Qualified to provide medical advice
❌ A replacement for emergency medical services
❌ Certified by medical regulatory bodies

## IMPORTANT MEDICAL ADVICE:

### When to Consult a Healthcare Professional:
- Before making significant changes to your health routine
- When experiencing new or unusual symptoms
- For any concerns about your health or medications
- For proper diagnosis of health conditions
- For prescription of medications or treatments

### EMERGENCY RED FLAGS - SEEK IMMEDIATE MEDICAL ATTENTION:
🚨 Call your local emergency number (911 in USA, 112 in Europe, 999 in UK, 112 in Tanzania)
if you experience:

- Chest pain or pressure
- Severe shortness of breath
- Sudden severe headache or dizziness
- Loss of consciousness or fainting
- Difficulty speaking or understanding speech
- Weakness on one side of body
- Sudden vision changes
- Severe allergic reactions (difficulty breathing, swelling)
- Uncontrollable bleeding
- Severe abdominal pain
- Signs of stroke (facial drooping, arm weakness, speech difficulty)
- Confusion or disorientation
- Severe injuries or trauma
- Poisoning or overdose
- Any life-threatening condition

### For Non-Emergency Medical Concerns:
Contact your doctor, visit a clinic, or use telemedicine services.

## USE AT YOUR OWN RISK

By using this application, you acknowledge that:

1. You understand this is NOT a medical diagnosis tool
2. You will consult qualified healthcare professionals for medical concerns
3. You take full responsibility for decisions made based on this app's information
4. You understand the limitations and disclaimers
5. You will seek emergency help when needed
6. This app cannot replace professional medical judgment

## DATA PRIVACY & SECURITY

- Your health data is sensitive and should be protected
- Use strong passwords and secure connections
- Do not share your login credentials
- Be cautious about what health information you enter
- Review our privacy policy for data handling practices
- Report any security concerns immediately

## MEDICATION SAFETY

If you are using this app to track medications:

⚠️ IMPORTANT:
- Only take medications prescribed by a healthcare professional
- Follow your doctor's dosage and timing instructions
- Report any side effects to your healthcare provider
- Do not self-diagnose or self-prescribe
- Inform all your doctors about all medications you're taking
- Never skip doses without consulting your doctor
- Store medications safely and as directed

## AI LIMITATIONS

The AI features in this app use artificial intelligence to provide educational guidance:

- AI is NOT a healthcare professional
- AI suggestions are for information only
- Always verify AI information with healthcare professionals
- AI can make mistakes
- AI does not provide medical diagnosis
- Individual health needs vary significantly

## SPECIAL POPULATIONS

### Pregnancy:
This app is NOT appropriate as a medical guide during pregnancy.
Pregnant individuals MUST work with qualified prenatal care providers.

### Children:
Parents/guardians are responsible for child health decisions.
Consult pediatricians for children's health concerns.

### Chronic Conditions:
If you have diabetes, hypertension, heart disease, asthma, or other chronic conditions,
you MUST work with your healthcare team. This app is a supplement only.

### Mental Health:
If you experience depression, anxiety, suicidal thoughts, or mental health crises:
- Contact a mental health professional immediately
- Call a mental health crisis line
- Do not rely solely on this app for mental health support

## GEOGRAPHIC SPECIFICS - TANZANIA

This app is developed with Tanzania in mind, but:

- The app does not replace the Tanzanian healthcare system
- Healthcare providers registered with the Tanzania Medical Council should be consulted
- Local clinics and hospitals should be your primary healthcare source
- Traditional and complementary medicine should be discussed with healthcare providers
- Government health information should be consulted when available

## LIABILITY LIMITATION

The creators and maintainers of this application:

- Are NOT liable for any health consequences from app use
- Provide information "as is" without warranties
- Do not guarantee accuracy of health information
- Do not accept liability for user decisions
- Recommend professional medical consultation
- Cannot be held responsible for missed diagnoses

## REPORTING ISSUES

If you experience problems with the app:
- Report technical issues to support
- Report health concerns to healthcare professionals
- Report inaccurate information to the app team
- Do NOT delay medical care to use this app

## UPDATES & CHANGES

This disclaimer may be updated as needed. Check for updates regularly.
Continued use of the app constitutes acceptance of current disclaimer.

---
Last Updated: January 30, 2026
Version: 1.0
"""

# ==================== SHORT DISCLAIMER ====================

HEALTH_DISCLAIMER_SHORT = """
⚠️ **DISCLAIMER:** This app is for health tracking and education only, NOT medical diagnosis.
Always consult healthcare professionals. Seek emergency care for urgent health issues.
"""

# ==================== EMERGENCY CONTACT NUMBERS ====================

EMERGENCY_CONTACTS = {
    'TANZANIA': {
        'ambulance': '112',
        'police': '112',
        'fire': '112',
        'main_number': '112',
        'info': 'Call 112 for all emergencies in Tanzania',
        'poison_control': 'National Poison Control: Not widely available, go to nearest hospital'
    },
    'EMERGENCY_SYMPTOMS': [
        'Chest pain or pressure',
        'Severe shortness of breath',
        'Sudden severe headache',
        'Loss of consciousness',
        'Difficulty speaking',
        'Weakness on one side of body',
        'Sudden vision changes',
        'Severe allergic reaction',
        'Uncontrollable bleeding',
        'Severe abdominal pain',
        'Signs of stroke',
        'Severe injuries or trauma'
    ]
}

# ==================== SAFETY PROTOCOLS ====================

class HealthSafetyProtocol:
    """Handles health and safety checks"""
    
    @staticmethod
    def check_emergency_symptoms(symptoms_list):
        """Check if user is reporting emergency symptoms"""
        emergency_keywords = [
            'chest pain', 'difficulty breathing', 'shortness of breath',
            'severe headache', 'unconscious', 'fainting', 'stroke',
            'difficulty speaking', 'weakness', 'sudden vision',
            'severe allergic', 'bleeding', 'severe pain',
            'heart attack', 'emergency'
        ]
        
        text = ' '.join(symptoms_list).lower()
        
        for keyword in emergency_keywords:
            if keyword in text:
                return True
        
        return False
    
    @staticmethod
    def get_emergency_response():
        """Get emergency response message"""
        return {
            'is_emergency': True,
            'message': f"""
🚨 **EMERGENCY ALERT** 🚨

Based on your symptoms, this may be a medical emergency.

**SEEK IMMEDIATE MEDICAL ATTENTION:**

{EMERGENCY_CONTACTS['TANZANIA']['info']}

**Do NOT delay - Call emergency services NOW**

Go to the nearest hospital or clinic immediately.

This app cannot provide emergency medical care.
Only trained healthcare professionals can diagnose and treat emergencies.
            """,
            'action': 'CALL_EMERGENCY',
            'phone': EMERGENCY_CONTACTS['TANZANIA']['main_number']
        }
    
    @staticmethod
    def check_blood_pressure_alert(systolic, diastolic):
        """Check for dangerous blood pressure readings"""
        alerts = []
        
        if systolic >= 180 or diastolic >= 120:
            alerts.append({
                'severity': 'CRITICAL',
                'message': 'Critical blood pressure reading. Seek medical attention immediately.',
                'action': 'CONSULT_DOCTOR'
            })
        elif systolic >= 140 or diastolic >= 90:
            alerts.append({
                'severity': 'HIGH',
                'message': 'High blood pressure. Consult your healthcare provider.',
                'action': 'CONSULT_DOCTOR'
            })
        
        return alerts
    
    @staticmethod
    def check_blood_sugar_alert(blood_sugar):
        """Check for dangerous blood sugar readings"""
        alerts = []
        
        if blood_sugar < 70:
            alerts.append({
                'severity': 'HIGH',
                'message': 'Low blood sugar (hypoglycemia). Consume fast-acting carbs immediately.',
                'action': 'TAKE_ACTION'
            })
        elif blood_sugar > 300:
            alerts.append({
                'severity': 'HIGH',
                'message': 'Very high blood sugar. Consult your healthcare provider.',
                'action': 'CONSULT_DOCTOR'
            })
        
        return alerts
    
    @staticmethod
    def check_mental_health_alert(mood_score, anxiety, stress):
        """Check for mental health concerns"""
        alerts = []
        
        if mood_score < 2 and anxiety > 7:
            alerts.append({
                'severity': 'HIGH',
                'message': 'You may be experiencing significant mental health concerns. Consider speaking with a mental health professional.',
                'action': 'SEEK_SUPPORT',
                'resources': [
                    'Mental health counselor',
                    'Psychologist',
                    'Psychiatrist',
                    'Crisis support line'
                ]
            })
        
        return alerts
    
    @staticmethod
    def get_health_disclaimer():
        """Get appropriate disclaimer based on context"""
        return {
            'short': HEALTH_DISCLAIMER_SHORT,
            'full': HEALTH_DISCLAIMER_FULL,
            'emergency_numbers': EMERGENCY_CONTACTS
        }


# ==================== CONSENT & PRIVACY ====================

class HealthDataConsent:
    """Manages user consent for health data usage"""
    
    CONSENT_TYPES = {
        'DATA_COLLECTION': 'Agree to collect health data',
        'AI_ANALYSIS': 'Agree to AI analysis of health data',
        'RECOMMENDATIONS': 'Agree to receive AI recommendations',
        'ANONYMIZED_RESEARCH': 'Agree to use anonymized data for research',
    }
    
    @staticmethod
    def get_consent_text():
        """Get consent agreement text"""
        return """
HEALTH DATA CONSENT AGREEMENT

By using this health app, I acknowledge and agree that:

1. HEALTH DATA COLLECTION
   - I agree to provide my personal health information
   - I understand this data will be stored on the app
   - I am responsible for accuracy of information

2. DATA USAGE
   - My data will be used to track my health
   - AI will analyze my data for insights and recommendations
   - My data will NOT be sold to third parties

3. CONFIDENTIALITY
   - I understand my health data is confidential
   - I will keep my login credentials secure
   - I am responsible for who accesses my account

4. MEDICAL DISCLAIMER
   - I understand this app is NOT a medical diagnosis tool
   - I agree to consult healthcare professionals for medical advice
   - I accept full responsibility for decisions based on this app
   - I will seek emergency care when needed

5. DATA ACCURACY
   - I will provide accurate health information
   - I understand inaccurate data leads to inaccurate insights
   - I will update information as it changes

6. SECURITY
   - I will use strong passwords
   - I will not share my login information
   - I will report any security concerns

I agree to these terms and the health disclaimer above.

Date: _______________
Signature: _______________
"""


# ==================== COMPLIANCE CHECKLIST ====================

COMPLIANCE_CHECKLIST = {
    'HEALTH_DISCLAIMERS': {
        'full_disclaimer_displayed': True,
        'short_disclaimer_on_health_features': True,
        'emergency_protocol_implemented': True,
        'red_flag_detection': True,
    },
    'DATA_PRIVACY': {
        'user_consent_required': True,
        'data_encryption': False,  # TODO: Implement
        'privacy_policy_accessible': True,
        'data_export_available': False,  # TODO: Implement
    },
    'SAFETY_FEATURES': {
        'emergency_contacts_available': True,
        'symptom_emergency_check': True,
        'vital_sign_alerts': True,
        'medication_warnings': True,
    },
    'CONTENT_ACCURACY': {
        'health_info_reviewed': True,
        'local_context_considered': True,
        'updated_regularly': False,  # TODO: Set schedule
    },
    'USER_SUPPORT': {
        'help_section_available': False,  # TODO: Implement
        'contact_support_available': False,  # TODO: Implement
        'faq_section': False,  # TODO: Implement
    }
}

# ==================== HELPER FUNCTIONS ====================

def get_app_disclaimer(context='general'):
    """Get appropriate disclaimer for context"""
    disclaimers = {
        'general': HEALTH_DISCLAIMER_SHORT,
        'full': HEALTH_DISCLAIMER_FULL,
        'vitals': 'Remember: Abnormal readings should be confirmed with a healthcare provider.',
        'nutrition': 'Always consult a nutritionist or doctor for personalized diet advice.',
        'mental_health': 'If experiencing mental health crisis, contact a mental health professional or crisis line immediately.',
        'medication': 'Only take medications prescribed by healthcare professionals. Report side effects to your doctor.',
        'appointment': 'Use this to organize appointments, but always attend professional medical consultations.',
    }
    
    return disclaimers.get(context, HEALTH_DISCLAIMER_SHORT)


def validate_health_input(data_type, value):
    """Validate health input data"""
    validations = {
        'blood_pressure_systolic': lambda v: 0 <= v <= 200,
        'blood_pressure_diastolic': lambda v: 0 <= v <= 130,
        'heart_rate': lambda v: 0 <= v <= 200,
        'weight': lambda v: 20 <= v <= 300,
        'blood_sugar': lambda v: 0 <= v <= 500,
        'mood_score': lambda v: 1 <= v <= 5,
        'stress_level': lambda v: 0 <= v <= 10,
    }
    
    validator = validations.get(data_type)
    if validator:
        return validator(value)
    
    return True


"""
Compliance Module
Version: 1.0
Created: January 30, 2026
"""
