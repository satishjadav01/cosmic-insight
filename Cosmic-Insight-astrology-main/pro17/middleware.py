"""
Navigation Guard Middleware

Prevents users from navigating by manually typing URLs in the browser address bar.
Navigation is only allowed when initiated by the application itself (clicking links,
submitting forms, or server-side redirects).

How it works:
1. Every request is intercepted by this middleware.
2. The middleware checks whether the navigation was initiated by the application:
   - Referer header present and from our domain → in-app click/form → ALLOW
   - Following a server-issued redirect (302/301) → ALLOW
   - POST request → form submission → ALLOW
   - Same page as current (refresh) → ALLOW
   - First visit (no current_page in session) → ALLOW
3. If none of the above → manual URL entry → REDIRECT back to current page.
"""

from django.shortcuts import redirect
from urllib.parse import urlparse


class NavigationGuardMiddleware:
    """Blocks manual URL entry; only allows in-app navigation."""

    # Paths that should never be blocked (static files, admin, etc.)
    EXEMPT_PREFIXES = ['/static/', '/admin/', '/favicon.ico']

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        # 1. Skip non-page requests (static files, admin, etc.)
        if any(path.startswith(prefix) for prefix in self.EXEMPT_PREFIXES):
            return self.get_response(request)

        # 2. If following a server-initiated redirect → allow and update current_page
        if request.session.pop('_nav_redirect', False):
            request.session['current_page'] = path
            request.session.modified = True
            response = self.get_response(request)
            self._track_redirects(request, response)
            return response

        current_page = request.session.get('current_page')

        # 3. First visit ever (no page stored yet) → allow entry
        if not current_page:
            request.session['current_page'] = path
            request.session.modified = True
            response = self.get_response(request)
            self._track_redirects(request, response)
            return response

        # 4. Same page (browser refresh / F5) → allow
        if path.rstrip('/') == current_page.rstrip('/'):
            response = self.get_response(request)
            self._track_redirects(request, response)
            return response

        # 5. POST request (form submission from the app) → allow
        if request.method == 'POST':
            request.session['current_page'] = path
            request.session.modified = True
            response = self.get_response(request)
            self._track_redirects(request, response)
            return response

        # 6. Check Referer header — present and from our domain means in-app link click
        referer = request.META.get('HTTP_REFERER', '')
        if referer and self._is_same_origin(request, referer):
            request.session['current_page'] = path
            request.session.modified = True
            response = self.get_response(request)
            self._track_redirects(request, response)
            return response

        # 7. None of the above → manual URL entry → block and redirect to current page
        return redirect(current_page)

    def _is_same_origin(self, request, referer):
        """Check if the Referer header is from the same domain as this application."""
        try:
            parsed = urlparse(referer)
            host = request.get_host()
            # Match hostname (with or without port)
            return parsed.netloc == host
        except Exception:
            return False

    def _track_redirects(self, request, response):
        """
        If the view returned a redirect (301/302), mark the session so the
        next incoming request (from the browser following the redirect) is allowed.
        """
        if response.status_code in (301, 302):
            request.session['_nav_redirect'] = True
            request.session.modified = True
