from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from euphonime.models import ProfileUser, UserWatching, UserAnimeScore, Season, Anime, AnimeSeason
from django.shortcuts import redirect
from social_django.models import UserSocialAuth
from django.db import transaction
from django.db.models import Count
from dateutil import parser as ps
from django.db.models import Q
from allauth.socialaccount.models import SocialAccount


@login_required
def profile(request):
    user = request.user
    profile = ProfileUser.objects.filter(user=user).first()
    social = UserSocialAuth.objects.filter(user=user).first()

    this_season = Season.objects.filter(is_season=True).first()
    anime = AnimeSeason.objects.filter(season=this_season)


    context = {'profile': profile}

    if social:
        image = social.extra_data['picture']['data']['url']
        context = {
            'profile_pic': image,
        }

    if not profile:
        return redirect('finish_signup')

    if profile.photo_profile:
        context['profile_pic'] = profile.photo_profile.url

    watch_anime = UserWatching.objects.filter(user=profile)

    context['watch_data'] = [
        watch_anime.filter(status=2).count(),
        watch_anime.filter(status=1).count(),
        watch_anime.filter(status=3).count(),
        watch_anime.filter(status=4).count(),
    ]

    score_anime = UserAnimeScore.objects.filter(user=profile)

    context['score_data'] = [
        score_anime.filter(score=10).count(),
        score_anime.filter(score=9).count(),
        score_anime.filter(score=8).count(),
        score_anime.filter(score=7).count(),
        score_anime.filter(score=6).count(),
        score_anime.filter(score=5).count(),
        score_anime.filter(score=4).count(),
        score_anime.filter(score=3).count(),
        score_anime.filter(score=2).count(),
        score_anime.filter(score=1).count(),
    ]

    context['user_watching'] = watch_anime

    return render(request, 'euphonime/profile.html', context)


@login_required
@transaction.atomic
def edit_profile(request, id):
    usr_prof = ProfileUser.objects.filter(id=id).first()
    if not usr_prof:
        return redirect('finish_signup')

    if request.method == 'POST':
        biodata = request.POST.get('biodata')
        birth_date = request.POST.get('birth_date')
        if biodata:
            usr_prof.biodata = biodata
        if birth_date:
            usr_prof.birth_date = ps.parse(birth_date)
        try:
            usr_prof.save()
        except Exception as e:
            print(e)
            return redirect('profile')
    return redirect('profile')
