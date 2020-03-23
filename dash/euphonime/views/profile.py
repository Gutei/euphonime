import logging
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from euphonime.models import ProfileUser, UserWatching, UserAnimeScore, Season, Anime, AnimeSeason, UserMessage
from django.shortcuts import redirect
from social_django.models import UserSocialAuth
from django.db import transaction
from django.db.models import Count
from dateutil import parser as ps
from django.db.models import Q
from allauth.socialaccount.models import SocialAccount

from euphonime.tasks import send_email_to_user

logger = logging.getLogger(__name__)

@login_required
def profile(request):
    user = request.user
    profile = ProfileUser.objects.filter(user=user).first()
    social = UserSocialAuth.objects.filter(user=user).first()

    this_season = Season.objects.filter(is_season=True).first()
    anime = AnimeSeason.objects.filter(season=this_season)

    allauth = SocialAccount.objects.filter(user=user).first()
    logger.debug('AUTHENTICATION FROM SOCIAL MEDIA {}'.format(allauth))

    context = {'profile': profile}

    if social:
        image = social.extra_data['picture']['data']['url']
        context = {
            'profile_pic': image,
        }

    if allauth:
        if "picture" in allauth.extra_data:
            image_url = allauth.extra_data['picture']
            logger.debug('GET PROFILE PIC {}'.format(image_url))

            context['sosmed_pic'] = image_url

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

    l = [
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
    context['score_data'] = l[::-1]

    context['user_watching'] = watch_anime.filter(status__in=[UserWatching.WATCHING, UserWatching.HOLDING, UserWatching.FINISHED_WATCHING]).order_by('-updated')[:10]

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
        gender = request.POST.get('gender')
        if biodata:
            usr_prof.biodata = biodata
        if birth_date:
            usr_prof.birth_date = ps.parse(birth_date)
        if gender:
            print(gender)
            usr_prof.gender = gender
        try:
            usr_prof.save()
        except Exception as e:
            print(e)
            return redirect('profile')
    return redirect('profile')

@login_required
def contact_modred(request, id):
    user = request.user
    username= user.username
    sender = 'projecteupho@gmail.com'
    email = []
    email.append(user.email)
    recipients = email
    subject = "{}, Kamu dapat pesan dari Mordred".format(username)

    if request.POST.get('mordred'):
        reply = "Pesan anda telah kami terima. Kami akan mendengarkan setiap kritik dan masukan dari kalian. Setelah semuanya diproses, kami akan membalas kembali pesanmu tanpa robot otomatis. Tenang saja, kami sangat membenci spam!<br><br><a href='https://euphonime.com/'>Kembalilah bersenang-senang!!</a>"
        content = "<img src='https://euphonime.com/static/euphonime/servant/modred-chibi.png' width='100'><br>Mastaa!! Pesan anda kepada developer telah saya sampaikan.<br>Begini kata mereka:<br><div style='padding:10px; border:1px solid #467f8a; border-radius:10px; background-color: #d1ebf0; max-width:400px;'><b>{}</b></div><br>".format(reply)
        send_email_to_user.apply_async((username, sender, recipients, subject, content),)
        user_profile = ProfileUser.objects.filter(user=user).first()
        user_profile.symbol -= 1
        user_profile.save()
        user_message = UserMessage(user=user_profile, message=request.POST.get('mordred'))
        user_message.save()

        return redirect('profile')

    return redirect('profile')