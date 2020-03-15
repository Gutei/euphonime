import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from euphonime.models import ProfileUser
from django.shortcuts import redirect
from django.urls import reverse
from social_django.models import UserSocialAuth

# Create your views here.
def login(request):
  return render(request, 'euphonime/login.html')

@login_required
def profile(request):
  user = request.user
  profile = ProfileUser.objects.filter(user=user).first()
  social = UserSocialAuth.objects.filter(user=user).first()
  image = social.extra_data['picture']['data']['url']
  context = {
    'profile_pic':image,
  }
  if not profile:
    return render(request, 'euphonime/finish_signup.html', context)

  return render(request, 'euphonime/profile.html', context)


@login_required
def finish_signup(request):
  user = request.user
  profile = ProfileUser.objects.filter(user=user).first()
  if profile:
    return redirect(reverse('profile'))
  else:
    profile = ProfileUser()
    profile.user = user
    profile.save()

  return redirect(reverse('profile'))