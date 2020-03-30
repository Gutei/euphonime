from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.db import transaction
from euphonime.models import ProfileUser


@transaction.atomic
def register(request):
    template_name = 'euphonime/register.html'

    if request.method == "POST":
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        context = {
            'failed': "True'"
        }

        if User.objects.filter(username=username).exists():
            context['message'] = 'You have tried to Register and Failed. Username already exist .'
            return render(request, template_name, context)
        if User.objects.filter(email=email).exists():
            context['message'] = 'You have tried to Register and Failed. Email already exist .'
            return render(request, template_name, context)

        user = User(
            username=username,
            email=email,
            password=make_password(password),
            is_active=True,
            is_staff=False,
        )

        try:
            user.save()
        except Exception as e:
            return render(request, template_name)

        profile_user = ProfileUser(user=user,)

        try:
            profile_user.save()
        except Exception as e:
            return render(request, template_name)

        return redirect('profile')
    return render(request, template_name)
