# middleware.py

from django.shortcuts import redirect
from django.urls import reverse

class SessionCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check session existence
        session_exists = request.session.get('fullname') is not None
        usertype = request.session.get('usertype')

        # Reverse URLs
        login_url = reverse('login')
        register_url = reverse('register')
        index_url = reverse('index')
        category_url = reverse('all-categories')
        process_login_url = reverse('process_login')
        process_register_url = reverse('process_registration')
        forget_url = reverse('email_verfication')
        otp_verfiy_url=reverse('otp_verfiy')
        otp_email_url=reverse('otp_email')
        dashboard_url = reverse('dashboard')
        manage_order_url = reverse('manage_order')
        productD_url = reverse('productD')
        viewuser_url = reverse('viewuser')

        # Allow access to media and static files without session check
        media_url = request.path.startswith('/media/')
        static_url = request.path.startswith('/static/')

        # Paths that can be accessed without a session
        allowed_paths_without_session = [
            login_url, 
            register_url, 
            index_url, 
            process_login_url,
            process_register_url,
            forget_url, 
            category_url,
            otp_verfiy_url,
            otp_email_url
        ]

        # Check for dynamic category product paths
        if request.path.startswith('/category_products/'):
            # If accessing a category product page, allow access without a session
            response = self.get_response(request)
            return response
        if request.path.startswith('/detail/'):
            # If accessing a category product page, allow access without a session
            response = self.get_response(request)
            return response

        # Paths that can be accessed with a session
        allowed_paths_with_session = [
            login_url, 
            register_url, 
            process_login_url
        ]

        # User allowed paths
        user_paths = [
            dashboard_url,
            manage_order_url,
            productD_url,
            viewuser_url
        ]

        # Allow access to media and static files without session check
        if media_url or static_url:
            response = self.get_response(request)
            return response

        # If session exists, handle redirection based on usertype
        if session_exists:
            if request.path in allowed_paths_with_session:
                if usertype == 0:
                    return redirect('index')
                else:
                    return redirect('dashboard')
            if request.path in user_paths and usertype == 0:
                return redirect('index')

        # If no session and trying to access a protected page, redirect to login
        if not session_exists and request.path not in allowed_paths_without_session:
            return redirect('login')

        response = self.get_response(request)
        return response
