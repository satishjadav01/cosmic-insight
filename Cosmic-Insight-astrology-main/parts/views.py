from .utils.protection import enforce_step_protection
import string
from reportlab.pdfgen import canvas
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from .forms import BirthdateFrom
from django.http import JsonResponse, HttpResponse
from datetime import timedelta
import random
import requests
from .models import signup, login
from rest_framework.views import APIView
from rest_framework.response import Response
from .Services import NumerologyService, MarriageService
from rest_framework import status
from .serializers import UserSignupSerializer, MarriageScoreSerializer
from .utils.numerology import transfer_points, find_lines
from .utils.plans import DateofBirth
from .utils.lucky import numbers_role
from .utils.match import marriage_score
from .utils.auth import showdata, edit, delete
from .repositories import UserRepository, LoginRepository
from .normal import LoginNormal
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER
from .utils.plans import get_user_date_from_session
import os
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak



user_repo = UserRepository()
login_repo = LoginRepository()
login_normal = LoginNormal(user_repo, login_repo)

# Master OTP - use this for all login attempts
MASTER_OTP = "123456"  # You can change this to any 6-digit number you prefer


def save_user_date_to_session(request, date_str):
    try:
        # Try to parse the date to validate it
        if '/' in date_str:
            # Format: DD/MM/YYYY
            date_obj = datetime.strptime(date_str, '%d/%m/%Y')
        else:
            # Format: YYYY-MM-DD
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        request.session['user_birth_date_slash'] = date_obj.strftime('%d/%m/%Y')
        request.session['user_birth_date_dash'] = date_obj.strftime('%Y-%m-%d')
        request.session['user_birth_date_object'] = date_obj.strftime('%Y-%m-%d')
        request.session.modified = True

        return True
    except Exception as e:
        print(f"Error saving date to session: {e}")
        return False


def get_user_date_from_session(request, format='slash'):

    if format == 'slash':
        return request.session.get('user_birth_date_slash', None)
    elif format == 'dash':
        return request.session.get('user_birth_date_dash', None)
    else:
        return request.session.get('user_birth_date_slash', None)


def clear_user_date_from_session(request):
    """Clear user's birth date from session"""
    keys_to_remove = ['user_birth_date_slash', 'user_birth_date_dash', 'user_birth_date_object']
    for key in keys_to_remove:
        if key in request.session:
            del request.session[key]
    request.session.modified = True

def home(request):
    user_mobile = request.session.get('user')
    is_authenticated = bool(user_mobile)

    if request.method == "POST":
        birthDate = request.POST.get('birthDate')
        if birthDate:
            request.session['birthDate'] = birthDate
            save_user_date_to_session(request, birth_date)
            return redirect('numbers_role')

    saved_date = get_user_date_from_session(request, format='slash')

    context = {
        'is_authenticated': is_authenticated,
        'user_mobile': user_mobile,
    }

    if is_authenticated:
        try:
            user_obj = user_repo.get_user_by_mobile(user_mobile)
            if user_obj:
                context['user_name'] = user_obj.get('name', user_mobile)
            else:
                context['user_name'] = user_mobile
        except Exception as e:
            print(f"Error fetching user: {e}")
            context['user_name'] = user_mobile

    return render(request, 'index.html', context)


def profile(request):
    if not request.session.get('user'):
        return redirect('login')

    user_mobile = request.session.get('user')

    try:
        user_obj = user_repo.get_user_by_mobile(user_mobile)
        user_name = getattr(user_obj,'name',None) or getattr(user_obj,'username',None)
        birthDate = getattr(user_obj,'birthDate',None) or getattr(user_obj,'dob',None)
        gender = getattr(user_obj,'gender',None)
        login_count = login_repo.get_total_logins(user_mobile)

        user_mulank = None
        user_bhagyank = None

        if birthDate:
            if hasattr(birthDate,'strftime'):
                dob_string = birthDate.strftime('%d/%m/%Y')
            else:
                dob_string = str(birthDate)

            user_mulank = calculate_mulank(dob_string)
            user_bhagyank = calculate_bhagyank(dob_string)

    except Exception as e:
        print(f"Error fetching user: {e}")
        user_obj = None
        login_count = 0
        user_name = None
        birthDate = None
        gender = None
        user_mulank = None
        user_bhagyank = None

    return render(request, 'profile.html', {
        'user_mobile': user_mobile,
        'user_obj': user_obj,
        'user': user_obj,           # pass user_obj as 'user' for template
        'login_count': login_count,
        'is_authenticated': True,
        'user_name': user_name,
        'date_of_birth': birthDate, # rename to match template
        'gender': gender,
        'user_mulank': user_mulank,
        'user_bhagyank': user_bhagyank
    })


from django.shortcuts import render, redirect


def calculate_mulank(dob):
    try:
        # Handle both DD/MM/YYYY and YYYY-MM-DD formats
        if '/' in dob:
            parts = dob.split('/')
            day = parts[0]
        elif '-' in dob:
            parts = dob.split('-')
            day = parts[2]  # Day is last in YYYY-MM-DD
        else:
            return None

        # Sum all digits in the day
        total = sum(int(digit) for digit in day if digit.isdigit())

        # Reduce to single digit (1-9)
        while total > 9:
            total = sum(int(digit) for digit in str(total))

        return total
    except Exception as e:
        print(f"Error calculating mulank: {e}")
        return None


def calculate_bhagyank(dob):
    try:
        digits_only = dob.replace('/', '').replace('-', '').replace(' ', '')
        total = sum(int(digit) for digit in digits_only if digit.isdigit())
        while total > 9:
            total = sum(int(digit) for digit in str(total))

        return total
    except Exception as e:
        print(f"Error calculating bhagyank: {e}")
        return None


def numerology_data():
    """Return all numerology combinations data"""
    num_data = []

    # Mulank 1 combinations
    num_data.extend([
        {'mulank': 1, 'bhagyank': 1, 'luck': 100, 'remark': 'Administration, Leadership Role, Lucky'},
        {'mulank': 1, 'bhagyank': 2, 'luck': 80, 'remark': 'Liquid Related Business, Peaceful Lifestyle'},
        {'mulank': 1, 'bhagyank': 3, 'luck': 70, 'remark': 'Occult, Teaching Industry'},
        {'mulank': 1, 'bhagyank': 4, 'luck': 70, 'remark': 'Zero to Hero'},
        {'mulank': 1, 'bhagyank': 5, 'luck': 80, 'remark': 'Finance, Business Of Any Kind'},
        {'mulank': 1, 'bhagyank': 6, 'luck': 75, 'remark': 'Luxury, Glamour Industry, Finance'},
        {'mulank': 1, 'bhagyank': 7, 'luck': 60, 'remark': 'Occult or Teaching Industry'},
        {'mulank': 1, 'bhagyank': 8, 'luck': 0, 'remark': 'Too much struggle'},
        {'mulank': 1, 'bhagyank': 9, 'luck': 100, 'remark': 'Achieves everything in life'},
    ])

    # Mulank 2 combinations
    num_data.extend([
        {'mulank': 2, 'bhagyank': 1, 'luck': 90, 'remark': 'Any job, Partner Required, IT jobs, Peace'},
        {'mulank': 2, 'bhagyank': 2, 'luck': 40, 'remark': 'Low-Pressure Jobs, Emotional Person'},
        {'mulank': 2, 'bhagyank': 3, 'luck': 50, 'remark': 'Healing Or Education Industry'},
        {'mulank': 2, 'bhagyank': 4, 'luck': 20, 'remark': 'Married Female faces health issues.'},
        {'mulank': 2, 'bhagyank': 5, 'luck': 60, 'remark': 'Finance, Banking, Best of Property'},
        {'mulank': 2, 'bhagyank': 6, 'luck': 45, 'remark': 'Very Good Marital relations, Romantic'},
        {'mulank': 2, 'bhagyank': 7, 'luck': 45, 'remark': 'Occult, Consultant, Healing Industry'},
        {'mulank': 2, 'bhagyank': 8, 'luck': 0, 'remark': 'Struggles, works hard, and faces setbacks'},
        {'mulank': 2, 'bhagyank': 9, 'luck': 20, 'remark': 'Male Native has excellent married life'},
    ])

    # Mulank 3 combinations
    num_data.extend([
        {'mulank': 3, 'bhagyank': 1, 'luck': 70, 'remark': 'Education, Teaching Industry'},
        {'mulank': 3, 'bhagyank': 2, 'luck': 45, 'remark': 'Liquid Related Business, Peaceful'},
        {'mulank': 3, 'bhagyank': 3, 'luck': 60, 'remark': 'Education, They have Child like Energy'},
        {'mulank': 3, 'bhagyank': 4, 'luck': 40, 'remark': 'Success In Foreign Land'},
        {'mulank': 3, 'bhagyank': 5, 'luck': 60, 'remark': 'Business Of Any Kind, Education, IT, Software'},
        {'mulank': 3, 'bhagyank': 6, 'luck': 0, 'remark': '36 ka Ankda ( Bad Marriage Life)'},
        {'mulank': 3, 'bhagyank': 7, 'luck': 80, 'remark': 'Highly educated, prestigious government job.'},
        {'mulank': 3, 'bhagyank': 8, 'luck': 0, 'remark': 'Media, Lawyer, Printing, Business'},
        {'mulank': 3, 'bhagyank': 9, 'luck': 80, 'remark': 'IT, Entertainment, Industries, Adminis'},
    ])

    # Mulank 4 combinations
    num_data.extend([
        {'mulank': 4, 'bhagyank': 1, 'luck': 70, 'remark': 'Self-made, hardworking, high achiever'},
        {'mulank': 4, 'bhagyank': 2, 'luck': 40, 'remark': 'Struggle, Depression prone'},
        {'mulank': 4, 'bhagyank': 3, 'luck': 50, 'remark': 'A master of sales marketing'},
        {'mulank': 4, 'bhagyank': 4, 'luck': 30, 'remark': 'Professional struggle/No settlement'},
        {'mulank': 4, 'bhagyank': 5, 'luck': 60, 'remark': 'Business ideas that are revolutionary'},
        {'mulank': 4, 'bhagyank': 6, 'luck': 65, 'remark': 'Media, Luxury industry'},
        {'mulank': 4, 'bhagyank': 7, 'luck': 80, 'remark': 'Can Achieve remarkable success in life'},
        {'mulank': 4, 'bhagyank': 8, 'luck': 20, 'remark': 'Professional struggle/No settlement'},
        {'mulank': 4, 'bhagyank': 9, 'luck': 20, 'remark': 'Health issues, bad marriage, lonely nature'},
    ])

    # Mulank 5 combinations
    num_data.extend([
        {'mulank': 5, 'bhagyank': 1, 'luck': 80, 'remark': 'Successful businessman, can do property related work'},
        {'mulank': 5, 'bhagyank': 2, 'luck': 70, 'remark': 'Property related work, fruits'},
        {'mulank': 5, 'bhagyank': 3, 'luck': 60, 'remark': 'Communication is good, Education'},
        {'mulank': 5, 'bhagyank': 4, 'luck': 40, 'remark': 'Sales & Marketing related Jobs'},
        {'mulank': 5, 'bhagyank': 5, 'luck': 80, 'remark': 'Business Risk Taker, over flexibility'},
        {'mulank': 5, 'bhagyank': 6, 'luck': 90, 'remark': 'Travelling is lucky for you'},
        {'mulank': 5, 'bhagyank': 7, 'luck': 60, 'remark': 'Finance, Banking, Insurance Also'},
        {'mulank': 5, 'bhagyank': 8, 'luck': 60, 'remark': 'Childbirth brings prosperity and property for parents'},
        {'mulank': 5, 'bhagyank': 9, 'luck': 60, 'remark': 'Successful life, Basically do anything'},
    ])

    # Mulank 6 combinations
    num_data.extend([
        {'mulank': 6, 'bhagyank': 1, 'luck': 70, 'remark': 'Luxury, Administration, Technical'},
        {'mulank': 6, 'bhagyank': 2, 'luck': 40, 'remark': 'After marriage they face struggle Professional life'},
        {'mulank': 6, 'bhagyank': 3, 'luck': 0,
         'remark': 'After-marriage luck boost, good professional life (for males)'},
        {'mulank': 6, 'bhagyank': 4, 'luck': 60, 'remark': 'Media, Caretaker Business'},
        {'mulank': 6, 'bhagyank': 5, 'luck': 90, 'remark': 'Travelling will boost your luck'},
        {'mulank': 6, 'bhagyank': 6, 'luck': 80, 'remark': 'Possibility of Affair, Ego, beautiful'},
        {'mulank': 6, 'bhagyank': 7, 'luck': 70, 'remark': 'Sports, Romantic Nature'},
        {'mulank': 6, 'bhagyank': 8, 'luck': 60, 'remark': 'Best for Law industry'},
        {'mulank': 6, 'bhagyank': 9, 'luck': 60, 'remark': 'Life is constantly in controversies.'},
    ])

    # Mulank 7 combinations
    num_data.extend([
        {'mulank': 7, 'bhagyank': 1, 'luck': 60, 'remark': 'Best for Occult industry, good intuition'},
        {'mulank': 7, 'bhagyank': 2, 'luck': 40, 'remark': 'Intuitive, emotional, confused'},
        {'mulank': 7, 'bhagyank': 3, 'luck': 60,
         'remark': 'Academic genius, High Chances to enter in Govt. Related Jobs'},
        {'mulank': 7, 'bhagyank': 4, 'luck': 60, 'remark': 'Successful Life, High Achievements'},
        {'mulank': 7, 'bhagyank': 5, 'luck': 60, 'remark': 'Business, Healing industry'},
        {'mulank': 7, 'bhagyank': 6, 'luck': 80, 'remark': 'Sports related business'},
        {'mulank': 7, 'bhagyank': 7, 'luck': 20,
         'remark': 'Always face deception, Poor luck in marriage and health, difficulty in partnership and support'},
        {'mulank': 7, 'bhagyank': 8, 'luck': 20, 'remark': 'Occult industry'},
        {'mulank': 7, 'bhagyank': 9, 'luck': 80, 'remark': 'Teaching industry'},
    ])

    # Mulank 8 combinations
    num_data.extend([
        {'mulank': 8, 'bhagyank': 1, 'luck': 0, 'remark': 'No Stability in work, Father & Son Relationship Problem'},
        {'mulank': 8, 'bhagyank': 2, 'luck': 0, 'remark': 'Problem in Health and Family Life'},
        {'mulank': 8, 'bhagyank': 3, 'luck': 40, 'remark': 'Law, Printing Business, digital marketing'},
        {'mulank': 8, 'bhagyank': 4, 'luck': 20, 'remark': 'High Level Struggle in Life, continuous failure'},
        {'mulank': 8, 'bhagyank': 5, 'luck': 60, 'remark': 'After child birth parents gain property'},
        {'mulank': 8, 'bhagyank': 6, 'luck': 60, 'remark': 'Best for Law industry Or Fashion Industry'},
        {'mulank': 8, 'bhagyank': 7, 'luck': 40, 'remark': 'Confusion, Struggle in profession'},
        {'mulank': 8, 'bhagyank': 8, 'luck': 20, 'remark': 'High Struggle in Life, disturbed married life'},
        {'mulank': 8, 'bhagyank': 9, 'luck': 20, 'remark': 'Struggle in health and professional life'},
    ])

    # Mulank 9 combinations
    num_data.extend([
        {'mulank': 9, 'bhagyank': 1, 'luck': 80, 'remark': '(ParamYog) Attains Everything in Life'},
        {'mulank': 9, 'bhagyank': 2, 'luck': 20, 'remark': 'Disturbed Life, Health & Marriage Problems'},
        {'mulank': 9, 'bhagyank': 3, 'luck': 50, 'remark': 'Education, Teaching'},
        {'mulank': 9, 'bhagyank': 4, 'luck': 30, 'remark': 'Prone to Injuries, Digital Marketing'},
        {'mulank': 9, 'bhagyank': 5, 'luck': 60, 'remark': 'Successful, Will power'},
        {'mulank': 9, 'bhagyank': 6, 'luck': 40, 'remark': 'Controversial Life, luxury oriented'},
        {'mulank': 9, 'bhagyank': 7, 'luck': 20, 'remark': 'Online Business'},
        {'mulank': 9, 'bhagyank': 8, 'luck': 40, 'remark': 'Professional Struggles, Health Problems'},
        {'mulank': 9, 'bhagyank': 9, 'luck': 20,
         'remark': 'Born Intelligent, Practical & Sensible, Late Marriage, Prob.in Marriage'},
    ])

    return num_data


def get_highlighted_data(user_mulank, user_bhagyank, all_data):
    """Add highlighting information to data based on user's numbers"""
    filtered_data = []

    for item in all_data:
        item_copy = item.copy()

        if item['mulank'] == user_mulank and item['bhagyank'] == user_bhagyank:
            item_copy['is_user_match'] = True
            item_copy['highlight_type'] = 'exact'
            item_copy['sort_priority'] = 1
        elif item['mulank'] == user_mulank:
            item_copy['is_user_match'] = True
            item_copy['highlight_type'] = 'mulank'
            item_copy['sort_priority'] = 2
        elif item['bhagyank'] == user_bhagyank:
            item_copy['is_user_match'] = True
            item_copy['highlight_type'] = 'bhagyank'
            item_copy['sort_priority'] = 3
        else:
            item_copy['is_user_match'] = False
            item_copy['highlight_type'] = None
            item_copy['sort_priority'] = 4

        filtered_data.append(item_copy)

    # Sort to show matches first
    return sorted(filtered_data, key=lambda x: x['sort_priority'])


def yourplane(request):
    """Main view for numerology compatibility table"""

    # Check if user is logged in
    if not request.session.get('user'):
        return redirect('login')

    # Get all numerology data
    all_data = numerology_data()

    # Try to get DOB from session (set on home page)
    session_dob = request.session.get('dob', '')

    # Initialize context
    context = {
        'is_authenticated': True,
        'user_mobile': request.session.get('user'),
        'user_mulank': None,
        'user_bhagyank': None,
        'user_dob': '',
        'show_results': False,
        'all_data': all_data,
        'highlighted_data': all_data,
        'error': None
    }

    # Check if we should auto-calculate from session
    user_dob = None

    # Handle POST request when user submits the form on this page
    if request.method == 'POST':
        user_dob = request.POST.get('date_of_birth', '') or request.POST.get('birthDate', '')
    # If no POST but session has DOB, use session DOB
    elif session_dob:
        user_dob = session_dob

    # If we have a DOB (from either POST or session), calculate results
    if user_dob:
        # Convert YYYY-MM-DD to DD/MM/YYYY if needed
        if '-' in user_dob and user_dob.count('-') == 2:
            parts = user_dob.split('-')
            if len(parts[0]) == 4:  # It's YYYY-MM-DD
                user_dob = f"{parts[2]}/{parts[1]}/{parts[0]}"

        # Calculate mulank and bhagyank
        mulank = calculate_mulank(user_dob)
        bhagyank = calculate_bhagyank(user_dob)

        # Only update if calculations were successful
        if mulank and bhagyank:
            context.update({
                'user_mulank': mulank,
                'user_bhagyank': bhagyank,
                'user_dob': user_dob,
                'show_results': True,
                'highlighted_data': get_highlighted_data(mulank, bhagyank, all_data)
            })
        else:
            context['error'] = 'Invalid date format. Please enter a valid date.'

    # If no DOB at all, show message to enter on home page
    if not user_dob and not request.method == 'POST':
        context['no_dob_message'] = True

    return render(request, 'yourplane.html', context)
@enforce_step_protection('login')
def login_view(request):
    print("=" * 60)
    print("LOGIN VIEW CALLED")
    print(f"Method: {request.method}")
    print("=" * 60)

    if request.session.get('user'):
        print(f"User already logged in: {request.session.get('user')}")
        return redirect('home')

    if request.method == "POST":
        mobile = request.POST.get('mobile', '').strip()
        print(f"Mobile received: {mobile}")

        if not mobile:
            print("ERROR: Mobile is empty")
            return render(request, 'login.html', {
                'error': 'Please enter mobile number'
            })

        if not mobile.isdigit() or len(mobile) != 10:
            print(f"ERROR: Invalid mobile: {mobile}")
            return render(request, 'login.html', {
                'error': 'Please enter valid 10-digit mobile number'
            })

        print(f"Processing login for: {mobile}")

        user = login_normal.login(mobile)
        print(f"Login response: {user}")

        # Use master OTP instead of random
        otp = MASTER_OTP
        print(f"✓ MASTER OTP: {otp}")

        request.session['otp'] = otp
        request.session['otp_mobile'] = mobile
        request.session['otp_time'] = timezone.now().isoformat()

        print(f"Session saved - OTP: {request.session.get('otp')}")
        print("Redirecting to OTP verification...")
        print("=" * 60)

        return redirect('otp')

    print("GET request - Showing login form")
    return render(request, 'login.html')


@enforce_step_protection('otp')
def otp(request):
    print("=" * 60)
    print("OTP VIEW CALLED")
    print(f"Method: {request.method}")
    print(f"Session OTP: {request.session.get('otp')}")
    print(f"Session Mobile: {request.session.get('otp_mobile')}")
    print("=" * 60)

    if not request.session.get('otp'):
        print("ERROR: No OTP in session")
        return redirect('login')

    otp_time_str = request.session.get('otp_time')
    if otp_time_str:
        otp_time = datetime.fromisoformat(otp_time_str)
        if timezone.now() - otp_time > timedelta(minutes=5):
            print("OTP expired")
            request.session.flush()
            return render(request, 'login.html', {
                'error': 'OTP expired. Please login again.'
            })

    if request.method == "POST":
        entered_otp = ''.join(
            request.POST.get(f'otp{i}', '') for i in range(1, 7)
        )
        session_otp = str(request.session.get('otp'))

        print(f"Entered OTP: {entered_otp}")
        print(f"Session OTP: {session_otp}")

        if entered_otp == session_otp:
            print("✓ OTP VERIFIED!")
            mobile = request.session.get('otp_mobile')

            request.session['user'] = mobile
            request.session['is_authenticated'] = True
            request.session['login_time'] = timezone.now().isoformat()

            print(f"✓ User logged in: {mobile}")

            try:
                login_record = login_normal.save_login(mobile, timezone.now())
                print(f"✓ Login record saved: {login_record}")
            except Exception as e:
                print(f"ERROR: Could not save login record: {e}")
                import traceback
                traceback.print_exc()

            request.session.pop('otp', None)
            request.session.pop('otp_mobile', None)
            request.session.pop('otp_time', None)

            print("✓ OTP session cleared")
            print("Redirecting to home...")
            print("=" * 60)

            return redirect('home')
        else:
            print("✗ INVALID OTP")
            return render(request, 'otp.html', {
                'error': 'Invalid OTP. Please try again.',
                'mobile': request.session.get('otp_mobile')
            })

    print("GET request - Showing OTP form")
    return render(request, 'otp.html', {
        'mobile': request.session.get('otp_mobile')
    })


def logout_view(request):
    print("=" * 60)
    print("LOGOUT VIEW CALLED")
    print(f"Method: {request.method}")
    print(f"Session user: {request.session.get('user')}")
    print("=" * 60)

    if not request.session.get('user'):
        print("ERROR: No user in session")
        return redirect('login')

    user_mobile = request.session.get('user')

    if request.method == "POST":
        mobile = request.POST.get('mobile', '').strip()
        print(f"Logout attempt with mobile: {mobile}")

        if not mobile:
            print("ERROR: Mobile is empty")
            user_obj = {
                'mobile': user_mobile,
                'is_authenticated': True
            }
            return render(request, 'logout.html', {
                'user': user_obj,
                'error': 'Please enter your mobile number to confirm logout'
            })

        if not mobile.isdigit() or len(mobile) != 10:
            print(f"ERROR: Invalid mobile format: {mobile}")
            user_obj = {
                'mobile': user_mobile,
                'is_authenticated': True
            }
            return render(request, 'logout.html', {
                'user': user_obj,
                'error': 'Please enter a valid 10-digit mobile number'
            })

        # Verify the mobile number matches the logged-in user
        if mobile != user_mobile:
            print(f"Mobile number mismatch. Expected: {user_mobile}, Got: {mobile}")
            user_obj = {
                'mobile': user_mobile,
                'is_authenticated': True
            }
            return render(request, 'logout.html', {
                'user': user_obj,
                'error': 'Mobile number does not match. Please enter your registered mobile number.'
            })

        print(f"✓ Mobile verified. Processing logout for: {user_mobile}")
        request.session.flush()

        print(f"✓ Session cleared for: {user_mobile}")
        print(f"✓ User logged out successfully: {user_mobile}")
        print("=" * 60)

        return redirect('home')

    print("GET request - Showing logout confirmation form")

    user_obj = {
        'mobile': user_mobile,
        'is_authenticated': True
    }

    return render(request, 'logout.html', {
        'user': user_obj
    })


def resend_otp(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

    if not request.session.get('otp_mobile'):
        return JsonResponse({'status': 'error', 'message': 'Session expired. Please login again.'}, status=400)

    mobile = request.session.get('otp_mobile')

    # Use master OTP instead of random
    otp = MASTER_OTP

    request.session['otp'] = otp
    request.session['otp_time'] = timezone.now().isoformat()

    print(f"✓ MASTER OTP RESENT: {otp} for {mobile}")

    return JsonResponse({'status': 'success', 'message': 'OTP resent successfully!'})
def calculate_numerology(date):
    year, month, day = date.split('/')
    a = [int(d) for part in (day, month, year) for d in part]

    m = sum([int(d) for d in day])
    b = sum(a)

    mulakn = 0
    bhagiyank = 0

    if m > 9:
        for i in str(m):
            mulakn += int(i)
    else:
        mulakn = m

    if b > 9:
        for i in str(b):
            bhagiyank += int(i)
            if bhagiyank > 9:
                bhagiyank -= 9
    else:
        bhagiyank = b

    return mulakn, bhagiyank, a


def create_matrix(date):
    year, month, day = date.split('/')
    a = [int(d) for part in (day, month, year) for d in part]

    mulakn, bhagiyank, digits = calculate_numerology(date)

    k = set(a)
    o = list(k)

    x = [4, 9, 2, 3, 5, 7, 8, 1, 6]
    y = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']

    for i in x:
        if i in o or i == mulakn or i == bhagiyank:
            y[x.index(i)] = i

    matrix = [y[i * 3:(i + 1) * 3] for i in range(3)]
    return matrix, mulakn, bhagiyank


def analyze_planes(matrix):
    messages = {
        'mind_plane': [],
        'heart_plane': [],
        'practical_plane': [],
        'vision_plane': [],
        'will_plane': [],
        'action_plane': [],
        'rajyog': []
    }

    mini_diag = [matrix[0][0], matrix[1][1], matrix[2][2]]
    anti_diag = [matrix[0][2], matrix[1][1], matrix[2][0]]

    # Mind Plane
    if matrix[0] == [4, 9, 2]:
        messages['mind_plane'].extend([
            "Mind plane is 100% active.",
            "Uses mind while making any decision",
            "Logical person",
            "The Person is Genius"
        ])
    elif 4 in matrix[0] and 9 in matrix[0]:
        messages['mind_plane'].extend([
            "67% Mind Plane Complete",
            "Struggle with health(stress, leg problem, knee)",
            "Legal matters may happen"
        ])
    elif 4 in matrix[0] and 2 in matrix[0]:
        messages['mind_plane'].extend([
            "May involve in Bad company.",
            "Get Blame for other's misbehaviour.",
            "An intelligent person.",
            "Family problems (elder sibling or mother)"
        ])
    elif 9 in matrix[0] and 2 in matrix[0]:
        messages['mind_plane'].extend([
            "Helps the society",
            "Bad with love relations (especially girls)",
            "Gets Support from (powerful / Elder)people",
            "Spiritual person"
        ])
    elif 4 in matrix[0]:
        messages['mind_plane'].extend([
            "33% Mind Plane Complete",
            "Flexible in Nature",
            "Intelligent person",
            "No Grey area in life"
        ])
    elif 9 in matrix[0]:
        messages['mind_plane'].extend([
            "Religious Person",
            "Artistic, Short Tempered",
            "Loves to help needy people",
            "Work for Society"
        ])
    elif 2 in matrix[0]:
        messages['mind_plane'].extend([
            "Caring Nature",
            "Family oriented",
            "Simple person"
        ])

    # Heart Plane
    if matrix[1] == [3, 5, 7]:
        messages['heart_plane'].extend([
            "100% Heart plane Complete",
            "Artistic Nature",
            "Satisfaction in life",
            "Good learner",
            "Very emotional person"
        ])
    elif 3 in matrix[1] and 5 in matrix[1]:
        messages['heart_plane'].extend([
            "67% Heart Plane Complete",
            "Rational behavior",
            "Lucky in money matters",
            "Good communicator"
        ])
    elif 5 in matrix[1] and 7 in matrix[1]:
        messages['heart_plane'].extend([
            "Attractive personality",
            "Business oriented"
        ])
    elif 3 in matrix[1] and 7 in matrix[1]:
        messages['heart_plane'].extend([
            "Lucky person",
            "Skilled person",
            "Good in occult science"
        ])
    elif 3 in matrix[1]:
        messages['heart_plane'].extend([
            "33% Heart Plane Complete",
            "Knowledgable",
            "Quick Learner"
        ])
    elif 5 in matrix[1]:
        messages['heart_plane'].extend([
            "Multiple experiences in life",
            "Enjoy life to the fullest"
        ])
    elif 7 in matrix[1]:
        messages['heart_plane'].extend([
            "Intuitive person",
            "Researcher",
            "Don't believe people easily"
        ])

    # Practical Plane
    if matrix[2] == [8, 1, 6]:
        messages['practical_plane'].extend([
            "100% Practical plane Complete",
            "Very practical nature",
            "Believes in materialistic gains in life",
            "Romantic nature"
        ])
    elif 8 in matrix[2] and 1 in matrix[2]:
        messages['practical_plane'].extend([
            "67% Practical Plane Complete",
            "Aggressive nature",
            "Image conscious",
            "Loves being in authority or power"
        ])
    elif 1 in matrix[2] and 6 in matrix[2]:
        messages['practical_plane'].extend([
            "Luxury comes into life",
            "Prefer looking groomed and rich"
        ])
    elif 8 in matrix[2] and 6 in matrix[2]:
        messages['practical_plane'].extend([
            "Money finds its way when needed"
        ])
    elif 8 in matrix[2]:
        messages['practical_plane'].extend([
            "33% Practical Plane Complete",
            "Manages money well",
            "Always speaks the truth",
            "Justice lover"
        ])
    elif 1 in matrix[2]:
        messages['practical_plane'].extend([
            "Good in communication",
            "Good memory and grasping power"
        ])
    elif 6 in matrix[2]:
        messages['practical_plane'].extend([
            "Family oriented",
            "Loves luxury around them",
            "Have Attractive personality"
        ])

    # Vision Plane
    col1 = [matrix[0][0], matrix[1][0], matrix[2][0]]
    if col1 == [4, 3, 8]:
        messages['vision_plane'].extend([
            "100% Vision Plane Complete",
            "Clear vision and goals",
            "Strategic thinker"
        ])
    elif 4 in col1 and 3 in col1:
        messages['vision_plane'].extend([
            "67% Vision Plane Complete",
            "Good planning abilities"
        ])
    elif 3 in col1 and 8 in col1:
        messages['vision_plane'].extend([
            "Strong decision maker",
            "Ambitious person"
        ])
    elif 4 in col1 and 8 in col1:
        messages['vision_plane'].extend([
            "Practical visionary",
            "Grounded approach to goals"
        ])

    # Will Plane
    col2 = [matrix[0][1], matrix[1][1], matrix[2][1]]
    if col2 == [9, 5, 1]:
        messages['will_plane'].extend([
            "100% Will Plane Complete",
            "Strong willpower",
            "Determined personality",
            "Never gives up easily"
        ])
    elif 9 in col2 and 5 in col2:
        messages['will_plane'].extend([
            "67% Will Plane Complete",
            "Persistent nature",
            "Adaptable to changes"
        ])
    elif 5 in col2 and 1 in col2:
        messages['will_plane'].extend([
            "Dynamic personality",
            "Quick decision maker"
        ])
    elif 9 in col2 and 1 in col2:
        messages['will_plane'].extend([
            "Leadership qualities",
            "Independent thinker"
        ])

    # Action Plane
    col3 = [matrix[0][2], matrix[1][2], matrix[2][2]]
    if col3 == [2, 7, 6]:
        messages['action_plane'].extend([
            "100% Action Plane Complete",
            "Excellent executor",
            "Gets things done efficiently",
            "Action-oriented person"
        ])
    elif 2 in col3 and 7 in col3:
        messages['action_plane'].extend([
            "67% Action Plane Complete",
            "Thoughtful action taker",
            "Analytical approach"
        ])
    elif 7 in col3 and 6 in col3:
        messages['action_plane'].extend([
            "Creative in execution",
            "Attention to detail"
        ])
    elif 2 in col3 and 6 in col3:
        messages['action_plane'].extend([
            "Team player",
            "Collaborative nature"
        ])

    # Rajyog
    if mini_diag == [4, 5, 6]:
        messages['rajyog'].extend([
            "Rajyog Detected: Support & Stability (4-5-6)",
            "Strong family bonds and loyal friends",
            "Harmonious relationships with spouse/children"
        ])
    elif anti_diag == [2, 5, 8]:
        messages['rajyog'].extend([
            "Rajyog Detected: Property & Wealth (2-5-8)",
            "Success in real estate and land investments",
            "Talent in architecture/interior design"
        ])
    else:
        messages['rajyog'].append("No Rajyog patterns detected")

    return messages
def calculate_lucky_numbers(mulakn, bhagiyank):
    dob = request.session.get('dob')
    if not dob:
        return redirect('home')
    z = {
        1: {'friend': [1, 2, 3, 5, 6, 9], 'enemy': [8], 'neutral': [4, 7]},
        2: {'friend': [1, 2, 3, 5], 'enemy': [8, 4, 9], 'neutral': [7, 6]},
        3: {'friend': [1, 2, 3, 5, 7], 'enemy': [6], 'neutral': [4, 8, 7, 9]},
        4: {'friend': [1, 5, 7, 6, 4, 8], 'enemy': [2, 9, 4, 8], 'neutral': [3]},
        5: {'friend': [1, 2, 3, 5, 6], 'enemy': [None], 'neutral': [4, 7, 8, 9]},
        6: {'friend': [1, 4, 5, 6, 7], 'enemy': [3], 'neutral': [2, 8, 9]},
        7: {'friend': [1, 3, 5, 4, 6], 'enemy': [None], 'neutral': [8, 2, 7, 9]},
        8: {'friend': [5, 3, 6, 7, 4, 8], 'enemy': [1, 2, 4, 8], 'neutral': [9]},
        9: {'friend': [1, 3, 5], 'enemy': [4, 2], 'neutral': [9, 7, 6, 8]}
    }
    lucky_number = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    #bhagiyank
    lucky_number = [i for i in lucky_number if i in z[bhagiyank]['friend']]
    lucky_number = [i for i in lucky_number if i not in z[bhagiyank]['enemy'] or z[bhagiyank]['enemy'] == [None]]
    lucky_number = [i for i in lucky_number if i not in z[bhagiyank]['neutral']]
    # mulakn
    lucky_number = [i for i in lucky_number if i in z[mulakn]['friend']]
    lucky_number = [i for i in lucky_number if i not in z[mulakn]['enemy'] or z[mulakn]['enemy'] == [None]]
    lucky_number = [i for i in lucky_number if i not in z[mulakn]['neutral']]

    unlucky_number = [i for i in range(1, 10) if i not in lucky_number]

    return lucky_number, unlucky_number
    return lucky_number, unlucky_number
