def user_type_context(request):
    """
    Add user type information to all template contexts
    """
    context = {
        'current_usertype': None,
        'is_jobseeker': False,
        'is_employer': False,
        'is_administrator': False,
    }
    
    if request.user.is_authenticated:
        usertype = request.session.get('usertype')
        context['current_usertype'] = usertype
        
        if usertype == 'jobseeker':
            context['is_jobseeker'] = True
        elif usertype == 'employer':
            context['is_employer'] = True
        elif usertype == 'administrator':
            context['is_administrator'] = True
    
    return context