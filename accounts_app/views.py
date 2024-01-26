from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth 
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


# Create your views here.
def register(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST) #request.post will contain all the field values
        if form.is_valid():
            # geting all the fields values
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            # from models.py taking create_user and passing all its arguments
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()

            # USER ACTIVATION sending mail
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_verification_email.html',{
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),#encoding user id
                'token': default_token_generator.make_token(user),
            })
            to_email = email 
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            # messages.success(request, 'Thank you for registering with us.we have sent you a verification email to your email address. Please verify it.')
            
            # redirect to this path it will be in google url search bar
            return redirect('/accounts/login/?command=verification&email='+email)

    else:
        form = RegistrationForm()
    context = {
        'form' : form,
    }
    return render(request, 'accounts/register.html', context)


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)
        print(user)

        if user is not None:
            auth.login(request, user)

            return redirect('home')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
        
    return render(request, 'accounts/login.html')



@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('login')

# after clicking on mail link then is_active = true 
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! your account is activated.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')
    


# http://127.0.0.1:8000/accounts/activate/MjI/c1emp8-6dfac89ee241202d22f2a69d5e33f395/