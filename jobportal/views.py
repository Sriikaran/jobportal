from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import logging

# Set up logging
logger = logging.getLogger(__name__)

@never_cache
@csrf_protect
def login_view(request):
    """
    Handle user login with different user types and redirect accordingly
    """
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        usertype = request.POST.get('usertype', '')
        
        # Input validation
        if not all([username, password, usertype]):
            messages.error(request, 'All fields are required. Please fill in all details.')
            return render(request, 'login.html')
        
        # Validate usertype
        valid_usertypes = ['jobseeker', 'employer', 'administrator']
        if usertype not in valid_usertypes:
            messages.error(request, 'Invalid user type selected.')
            return render(request, 'login.html')
        
        try:
            # Authenticate user
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                if user.is_active:
                    # Check if user has the required profile for the selected usertype
                    if validate_user_type(user, usertype):
                        # Login the user
                        login(request, user)
                        
                        # Store user type in session for future reference
                        request.session['usertype'] = usertype
                        request.session['user_id'] = user.id
                        
                        # Log successful login
                        logger.info(f"User {user.username} logged in as {usertype}")
                        
                        # Redirect based on user type
                        return redirect_by_usertype(usertype)
                    else:
                        messages.error(request, f'Your account is not registered as a {usertype.title()}. Please select the correct user type.')
                else:
                    messages.error(request, 'Your account has been deactivated. Please contact support.')
            else:
                messages.error(request, 'Invalid email or password. Please try again.')
                
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            messages.error(request, 'An error occurred during login. Please try again.')
    
    return render(request, 'login.html')


def validate_user_type(user, usertype):
    """
    Validate if user has the correct profile for the selected user type
    """
    try:
        if usertype == 'jobseeker':
            # Check if user has JobSeeker profile
            from jsapp.models import JobSeeker  # Adjust import based on your model location
            return hasattr(user, 'jobseeker') or JobSeeker.objects.filter(user=user).exists()
            
        elif usertype == 'employer':
            # Check if user has Employer profile
            from employer.models import Employer  # Adjust import based on your model location
            return hasattr(user, 'employer') or Employer.objects.filter(user=user).exists()
            
        elif usertype == 'administrator':
            # Check if user is admin/staff
            return user.is_staff or user.is_superuser
            
    except Exception as e:
        logger.error(f"Error validating user type: {str(e)}")
        return False
    
    return False


def redirect_by_usertype(usertype):
    """
    Redirect user based on their type
    """
    redirect_urls = {
        'jobseeker': 'jsapp:dashboard',  # Redirect to job seeker dashboard
        'employer': 'employer:dashboard',  # Redirect to employer dashboard  
        'administrator': 'adminapp:dashboard'  # Redirect to admin dashboard
    }
    
    # Fallback URLs in case named URLs don't exist
    fallback_urls = {
        'jobseeker': '/jsapp/',
        'employer': '/employer/', 
        'administrator': '/adminapp/'
    }
    
    try:
        return redirect(redirect_urls.get(usertype, '/'))
    except:
        # Use fallback URL if named URL fails
        return redirect(fallback_urls.get(usertype, '/'))


@login_required
def logout_view(request):
    """
    Handle user logout
    """
    usertype = request.session.get('usertype', '')
    username = request.user.username
    
    # Clear session data
    request.session.flush()
    
    # Logout user
    from django.contrib.auth import logout
    logout(request)
    
    logger.info(f"User {username} ({usertype}) logged out")
    
    messages.success(request, 'You have been successfully logged out.')
    return redirect('jobapp:login')


# Additional utility view for AJAX login (optional)
@csrf_protect
def ajax_login(request):
    """
    Handle AJAX login requests
    """
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        usertype = request.POST.get('usertype', '')
        
        if not all([username, password, usertype]):
            return JsonResponse({
                'success': False,
                'message': 'All fields are required.'
            })
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_active:
            if validate_user_type(user, usertype):
                login(request, user)
                request.session['usertype'] = usertype
                
                # Return success with redirect URL
                redirect_urls = {
                    'jobseeker': '/jsapp/',
                    'employer': '/employer/',
                    'administrator': '/adminapp/'
                }
                
                return JsonResponse({
                    'success': True,
                    'message': 'Login successful!',
                    'redirect_url': redirect_urls.get(usertype, '/')
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': f'Your account is not registered as a {usertype.title()}.'
                })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Invalid credentials.'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


# Middleware function to check user type on protected views (optional)
def check_user_type_middleware(get_response):
    """
    Middleware to ensure users can only access their designated areas
    """
    def middleware(request):
        # Skip middleware for certain paths
        skip_paths = ['/admin/', '/login/', '/logout/', '/register/', '/static/', '/media/']
        
        if any(request.path.startswith(path) for path in skip_paths):
            return get_response(request)
        
        # Check if user is authenticated and has correct access
        if request.user.is_authenticated:
            usertype = request.session.get('usertype')
            current_path = request.path
            
            # Define path restrictions
            restrictions = {
                'jobseeker': ['/employer/', '/adminapp/'],
                'employer': ['/jsapp/', '/adminapp/'],
                'administrator': []  # Admin can access all areas
            }
            
            if usertype in restrictions:
                restricted_paths = restrictions[usertype]
                if any(current_path.startswith(path) for path in restricted_paths):
                    messages.error(request, 'You do not have permission to access this area.')
                    return redirect_by_usertype(usertype)
        
        response = get_response(request)
        return response
    
    return middleware