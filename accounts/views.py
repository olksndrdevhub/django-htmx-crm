from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.template.response import TemplateResponse

from django_htmx.http import HttpResponseClientRedirect

from accounts.models import CrmUser

# Create your views here.
def auth(request):
    template_name = 'auth_page.html'
    page = 'login'

    context = {
        'page': page,
    }
    return render(request, template_name, context)


def hx_registration(request):
    partial_template_name = 'partials/registration.html'

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password1')

        if CrmUser.objects.filter(email=email).exists():
            messages.add_message(request, messages.ERROR, f'Error! User with email {email} already registered!')
        else:
            new_user = CrmUser.objects.create_user(
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password
            )
            new_user.is_active = True
            new_user.save()

            messages.add_message(request, messages.SUCCESS, f'Registration success! Check your {email} inbox to confirm your email!')
            return TemplateResponse(request, 'partials/login.html')


    if request.htmx:
        return render(request, partial_template_name)



def hx_login(request):
    partial_template_name = 'partials/login.html'

    if request.method == 'POST':
        print(request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(email=email, password=password)
        if user is not None and not user.is_staff:
            messages.add_message(request, messages.ERROR, 'Error! You must log in with staff credentials!')

        elif user is not None:
            login(request, user)
            messages.add_message(request, messages.SUCCESS, 'You successfully log in!')
            return HttpResponseClientRedirect('/')
        else:
            messages.add_message(request, messages.ERROR, 'Error! Wrong email or password...')

    if request.htmx:
        return render(request, partial_template_name)
