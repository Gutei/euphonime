import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from euphonime.models import ProfileUser, UserWatching
from django.shortcuts import redirect
from django.urls import reverse
from social_django.models import UserSocialAuth
from django.contrib.auth import authenticate, login as do_login, logout

# Create your views here.
def login(request):
  message = ''
  failed = False
  if request.GET.get('failed') == '1':
    message = "We're so sory to say your account now is inactive. Please contact our admin to solve this."
    failed = True
  if request.GET.get('failed') == '2':
    message = 'You have tried to login and failed. Please type your username and password correctly.'
    failed = True
  if request.GET.get('failed') == '3':
    message = 'You are tried to login and failed. Please type your username and password correctly.'
    failed = True

  user = request.user
  image = None
  if not user.is_anonymous:
    profile = ProfileUser.objects.filter(user=user).first()
    social = UserSocialAuth.objects.filter(user=user).first()
    if social:
      image = social.extra_data['picture']['data']['url']
    if profile.photo_profile:
      image = profile.photo_profile.url

  context = {
    'message': message,
    'failed': failed,
    'profile_pic': image,
  }

  return render(request, 'euphonime/login.html', context)

def auth_login(request):
  if request.POST:
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user:
      if user.is_active:
        do_login(request, user)
        return redirect(reverse('profile'))
      else:
        return redirect('{}?{}'.format(reverse('login'), 'failed=1'))
    else:
      # print("Someone tried to login and failed.")
      # print("They used username: {} and password: {}".format(username, password))
      return redirect('{}?{}'.format(reverse('login'), 'failed=2'))

  return redirect('{}?{}'.format(reverse('login'), 'failed=3'))

@login_required
def profile(request):
  user = request.user
  profile = ProfileUser.objects.filter(user=user).first()
  social = UserSocialAuth.objects.filter(user=user).first()
  image = None
  if social:
    image = social.extra_data['picture']['data']['url']
  context = {
    'profile_pic':image,
  }
  if not profile:
    return render(request, 'euphonime/finish_signup.html', context)

  if profile.photo_profile:
    context['profile_pic'] = profile.photo_profile.url

  user_anime_label = []
  user_anime_data = []
  user_anime = UserWatching.objects.filter(user=profile)
  for ua in user_anime:
    user_anime_label.append(ua.anime.title)

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