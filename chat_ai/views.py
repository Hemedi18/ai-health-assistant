from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
import json
import google.generativeai as genai
from datetime import datetime

from .models import ChatMessage, ChatSession
from .health_ai_engine import (
    get_health_summary, get_personalized_ai_recommendations,
    HealthRecommendationEngine, HEALTH_DISCLAIMER
)
from .symptom_assistant import process as symptom_process

# Configuration
API_KEY = "AIzaSyD38OvL0zSuVLMMc1mrhq54Dko0F0gdO50"
MODEL_ID = "gemini-2.5-flash"  # Using the latest stable Gemini model


@ensure_csrf_cookie
def chat_home(request):
    """Renders the AI chat home/intro page."""
    return render(request, 'chat_ai/chat_home.html')


@ensure_csrf_cookie
def chat_view(request):
    """Renders the chat interface."""
    return render(request, 'chat_ai/chat.html')



def chat_api(request):
    """Handles chat messages using Gemini AI with health context."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_input = data.get("message")
            session_id = data.get("session_id")
            
            if not user_input:
                return JsonResponse({"error": "Message is required"}, status=400)
            
            # Get or create chat session if authenticated
            session = None
            if request.user.is_authenticated:
                if session_id:
                    # Load existing session
                    try:
                        session = ChatSession.objects.get(id=session_id, user=request.user)
                    except ChatSession.DoesNotExist:
                        # Create new if doesn't exist or wrong user
                        session = ChatSession.objects.create(user=request.user)
                else:
                    # Create new session
                    session = ChatSession.objects.create(user=request.user)
                
                # Save user message
                ChatMessage.objects.create(
                    session=session,
                    user=request.user,
                    message_type='user',
                    content=user_input
                )

            # Add health context if user is authenticated
            context = ""
            if request.user.is_authenticated:
                try:
                    summary = get_health_summary(request.user)
                    context = f"""
User Health Context:
- Latest Health Data: {json.dumps(summary['profile'], default=str, indent=2)}
- Identified Health Risks: {json.dumps(summary['risks'], default=str)}

Remember to include the health disclaimer when giving medical advice."""
                except:
                    pass

            # Enhanced system prompt for health-focused responses
            system_prompt = f"""You are a helpful health education assistant for a health management app in Tanzania.
Your role is to:
1. Help users understand health concepts
2. Provide general wellness information (NOT medical diagnosis)
3. Encourage healthy habits
4. Remind users to consult healthcare professionals for medical issues
5. Be culturally sensitive and consider local context

IMPORTANT: Always include this disclaimer when discussing health: {HEALTH_DISCLAIMER}

{context}"""

            try:
                # Configure the API
                genai.configure(api_key=API_KEY)
                
                # Create a new chat session
                model = genai.GenerativeModel(MODEL_ID, system_instruction=system_prompt)
                
                # Send the message and get response
                response = model.generate_content(user_input)
                ai_response = response.text
                
                # Save AI response to database if authenticated
                if request.user.is_authenticated and session:
                    ChatMessage.objects.create(
                        session=session,
                        user=request.user,
                        message_type='ai',
                        content=ai_response
                    )
                    # Update session title based on first user message
                    if session.title == 'New Chat':
                        session.title = user_input[:50]
                        session.save()
                
                return JsonResponse({
                    "response": ai_response,
                    "session_id": str(session.id) if session else None
                })
            
            except Exception as gemini_error:
                # Fallback response if Gemini API fails
                error_msg = str(gemini_error)
                print(f"Gemini API Error: {error_msg}")  # Debug logging
                
                if "503" in error_msg or "overloaded" in error_msg.lower() or "rate" in error_msg.lower():
                    fallback_response = f"""I appreciate your question about "{user_input[:50]}..."

Currently, my AI services are temporarily busy. However, here are some general health tips:

**General Health Guidance:**
- Stay hydrated - drink at least 8 glasses of water daily
- Exercise regularly - aim for 30 minutes of moderate activity most days
- Get adequate sleep - 7-9 hours per night is recommended
- Eat a balanced diet with fruits, vegetables, and whole grains
- Manage stress through meditation or relaxation techniques

For specific health concerns, please consult with a qualified healthcare professional.

**Try asking me about:**
- General wellness tips
- Healthy lifestyle habits
- Common health concepts
- Nutrition advice
- Exercise recommendations

Feel free to ask your question again in a moment when services are available."""
                    
                    # Save fallback response
                    if request.user.is_authenticated and session:
                        ChatMessage.objects.create(
                            session=session,
                            user=request.user,
                            message_type='ai',
                            content=fallback_response
                        )
                    
                    return JsonResponse({
                        "response": fallback_response,
                        "session_id": str(session.id) if session else None
                    })
                else:
                    error_response = f"I'm having trouble connecting right now. Please try again in a moment."
                    if request.user.is_authenticated and session:
                        ChatMessage.objects.create(
                            session=session,
                            user=request.user,
                            message_type='ai',
                            content=error_response
                        )
                    return JsonResponse({
                        "response": error_response,
                        "session_id": str(session.id) if session else None
                    })
                
        except Exception as e:
            print(f"Chat API Error: {str(e)}")  # Debug logging
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "Method not allowed"}, status=405)


@login_required
def get_chat_history(request):
    """Get user's chat sessions list"""
    try:
        if not request.user.is_authenticated:
            return JsonResponse({'sessions': []})
        
        sessions = ChatSession.objects.filter(user=request.user).values(
            'id', 'title', 'created_at', 'updated_at'
        )
        
        return JsonResponse({
            'sessions': list(sessions),
            'count': len(sessions)
        })
    except Exception as e:
        return JsonResponse({'sessions': [], 'count': 0, 'error': str(e)})


@login_required
def get_session_messages(request, session_id):
    """Get all messages in a specific session"""
    try:
        if not request.user.is_authenticated:
            return JsonResponse({'messages': []})
        
        # Verify session belongs to user
        session = ChatSession.objects.get(id=session_id, user=request.user)
        messages = session.messages.values('id', 'message_type', 'content', 'created_at')
        
        return JsonResponse({
            'session_id': str(session.id),
            'session_title': session.title,
            'messages': list(messages),
            'count': len(messages)
        })
    except ChatSession.DoesNotExist:
        return JsonResponse({'error': 'Session not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_http_methods(["POST"])
def create_new_session(request):
    """Create a new chat session"""
    try:
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Not authenticated'}, status=401)
        
        session = ChatSession.objects.create(user=request.user)
        return JsonResponse({
            'session_id': str(session.id),
            'title': session.title,
            'created_at': session.created_at.isoformat()
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_http_methods(["POST"])
def delete_session(request, session_id):
    """Delete a chat session"""
    try:
        session = ChatSession.objects.get(id=session_id, user=request.user)
        session.delete()
        return JsonResponse({'status': 'success', 'message': 'Session deleted'})
    except ChatSession.DoesNotExist:
        return JsonResponse({'error': 'Session not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ==================== AI HEALTH FEATURES API ====================

@api_view(['GET'])
def health_summary_view(request):
    """Get personalized health summary and AI recommendations"""
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=401)
    
    try:
        recommendations = get_personalized_ai_recommendations(request.user)
        return Response(recommendations)
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['POST'])
def symptom_assessment_view(request):
    """Structured symptom assessment endpoint.

    Expects JSON: { action: 'start'|'answer', text: string, context: optional dict }
    Returns the assistant response dict.
    """
    try:
        payload = request.data or {}
        result = symptom_process(payload)
        return Response(result)
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['GET'])
def health_disclaimer_view(request):
    """Get health disclaimer"""
    return Response({'disclaimer': HEALTH_DISCLAIMER})


@api_view(['POST'])
def ask_health_question_view(request):
    """Ask health-related questions and get AI responses"""
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=401)
    
    try:
        question = request.data.get('question')
        if not question:
            return Response({'error': 'Question is required'}, status=400)
        
        # Get health context
        summary = get_health_summary(request.user)
        
        context_prompt = f"""You are a health education assistant. A user is asking: '{question}'

User's Health Profile:
{json.dumps(summary['profile'], default=str, indent=2)}

Identified Health Risks: {json.dumps(summary['risks'], default=str)}

Guidelines:
1. Provide educational information only, NOT medical diagnosis
2. Suggest consulting healthcare professionals for specific medical concerns
3. Include practical, actionable advice
4. Be culturally sensitive (Tanzania context)
5. Always include health disclaimers when appropriate

User Question: {question}"""

        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel(MODEL_ID, system_instruction=context_prompt)
        response = model.generate_content(question)
        
        return Response({
            'question': question,
            'response': response.text,
            'disclaimer': HEALTH_DISCLAIMER
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['GET'])
def nutrition_advice_view(request):
    """Get AI-powered nutrition advice"""
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=401)
    
    try:
        engine = HealthRecommendationEngine()
        advice = engine.get_nutrition_advice(request.user)
        return Response({
            'nutrition_advice': advice,
            'disclaimer': HEALTH_DISCLAIMER
        })
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['GET'])
def wellness_tips_view(request):
    """Get AI-powered mental wellness tips"""
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=401)
    
    try:
        engine = HealthRecommendationEngine()
        tips = engine.get_mental_wellness_tips(request.user)
        return Response({
            'wellness_tips': tips,
            'disclaimer': HEALTH_DISCLAIMER
        })
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['GET'])
def exercise_recommendations_view(request):
    """Get exercise recommendations based on health profile"""
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=401)
    
    try:
        summary = get_health_summary(request.user)
        profile = summary['profile']
        
        age = profile.get('age')
        avg_steps = profile.get('activity', {}).get('average_daily_steps', 0)
        latest_weight = profile.get('latest_vital', {}).get('weight')
        bmi = profile.get('latest_vital', {}).get('bmi')
        
        prompt = f"""Provide 5 specific exercise recommendations for someone with this profile:
- Age: {age} years
- Current daily steps: {avg_steps:.0f}
- BMI: {bmi if bmi else 'Not recorded'}
- Location: Tanzania

Consider:
1. Local climate and environment
2. Available resources
3. Injury prevention
4. Progressive difficulty

Format as numbered list with brief descriptions."""

        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel(MODEL_ID)
        response = model.generate_content(prompt)
        
        return Response({
            'exercise_recommendations': response.text,
            'profile_summary': profile.get('activity', {}),
            'disclaimer': HEALTH_DISCLAIMER
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=500)
