from functools import wraps
from django.shortcuts import redirect

# Auth routes accessible when not logged in
AUTH_ROUTES = {'login', 'otp', 'resend'}

def enforce_step_protection(view_name):
    """
    Strict Backend Route Guard:
    - Completely disables manual URL navigation in the browser address bar.
    - If an unauthenticated user manually types /home, /DateofBirth, /profile, /yourplane, etc.
      into the browser bar, the request is ignored and the server redirects them back to /login/.
    - If a logged-in user who hasn't submitted Date of Birth manually types /yourplane or /numbers_role,
      the request is ignored and the server redirects them back to /DateofBirth/.
    - If a logged-in user attempts to type /login into the URL bar, they are redirected back to their active workspace.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            is_logged_in = bool(request.session.get('user'))
            has_dob = bool(
                request.session.get('user_birth_date_slash') or 
                request.session.get('dob') or 
                request.session.get('birthDate')
            )

            # Rule 1: Unauthenticated users are strictly locked to /login/
            # Any manual URL change to /home, /DateofBirth, /profile, etc. is blocked.
            if not is_logged_in:
                if view_name not in AUTH_ROUTES:
                    return redirect('login')

            # Rule 2: Logged-in users cannot access login/otp forms; redirect to active workspace
            if is_logged_in and view_name in ['login', 'otp']:
                if not has_dob:
                    return redirect('DateofBirth')
                return redirect('home')

            # Rule 3: Logged-in users missing DOB cannot jump to advanced features (/yourplane, /numbers_role, /marriage_score)
            if is_logged_in and not has_dob:
                if view_name not in ['DateofBirth', 'home', 'profile', 'logout_view']:
                    return redirect('DateofBirth')

            # Store current authorized step in session
            request.session['current_step'] = view_name
            request.session.modified = True

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
