import logging
import re
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from euphonime.models import ProfileUser, UserWatching, UserAnimeScore, Season, Anime, AnimeSeason, UserMessage, \
    UserPost
from django.shortcuts import redirect
from social_django.models import UserSocialAuth
from django.db import transaction
from django.db.models import Count
from dateutil import parser as ps
from django.db.models import Q
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User
from django.core.paginator import Paginator
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

    usr_story = UserPost.objects.filter(user=profile).order_by('-created')[:100]
    paginator = Paginator(usr_story, 3)  # Show 25 contacts per page
    page = request.GET.get('page')
    story_page = paginator.get_page(page)

    context = {
        'profile': profile,
        'story_page': story_page,
    }

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

    biod = profile.biodata
    escape_biod = re.sub(r'<script.+?</script>', '', biod, flags=re.DOTALL)

    context['biodata'] = escape_biod

    # exeption user
    if profile.user.email == "hixotow831@upcmaill.com":
        context['biodata'] = biod

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

    context['user_watching'] = watch_anime.filter(
        status__in=[UserWatching.WATCHING, UserWatching.HOLDING, UserWatching.FINISHED_WATCHING]).order_by('-updated')[
                               :10]

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
        photo = request.FILES['photo']
        if biodata:
            usr_prof.biodata = biodata
        if birth_date:
            usr_prof.birth_date = ps.parse(birth_date)
        if gender:
            usr_prof.gender = gender
        if photo:
            usr_prof.photo_profile = photo
        try:
            usr_prof.save()
        except Exception as e:
            return redirect('profile')
    return redirect('profile')


@login_required
def contact_modred(request, id):
    user = request.user
    username = user.username
    sender = 'projecteupho@gmail.com'
    email = []
    email.append(user.email)
    recipients = email
    subject = "{}, Kamu dapat pesan dari Mordred".format(username)

    if request.POST.get('mordred'):
        reply = "Pesan anda telah kami terima. Kami akan mendengarkan setiap kritik dan masukan dari kalian. Setelah semuanya diproses, kami akan membalas kembali pesanmu tanpa robot otomatis. Tenang saja, kami sangat membenci spam!<br><br><a href='https://euphonime.com/'>Kembalilah bersenang-senang!!</a>"
        content = "<img src='https://euphonime.com/static/euphonime/servant/modred-chibi.png' width='100'><br>Mastaa!! Pesan anda kepada developer telah saya sampaikan.<br>Begini kata mereka:<br><div style='padding:10px; border:1px solid #467f8a; border-radius:10px; background-color: #d1ebf0; max-width:400px;'><b>{}</b></div><br>".format(
            reply)
        send_email_to_user.apply_async((username, sender, recipients, subject, content), )
        user_profile = ProfileUser.objects.filter(user=user).first()
        user_profile.symbol -= 1
        user_profile.save()
        user_message = UserMessage(user=user_profile, message=request.POST.get('mordred'))
        user_message.save()

        return redirect('profile')

    return redirect('profile')


def public_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = ProfileUser.objects.filter(user=user).first()
    allauth = SocialAccount.objects.filter(user=user).first()
    usr_story = UserPost.objects.filter(user=profile).order_by('-created')[:100]
    paginator = Paginator(usr_story, 3)  # Show 25 contacts per page
    page = request.GET.get('page')
    story_page = paginator.get_page(page)


    biod = profile.biodata
    if biod:
        escape_biod = re.sub(r'<script.+?</script>', '', biod, flags=re.DOTALL)
    else:
        escape_biod = ""

    context = {
        'profile': profile,
        'user': user,
        'biodata': escape_biod,
        'story_page': story_page,
    }

    if allauth:
        if "picture" in allauth.extra_data:
            image_url = allauth.extra_data['picture']
            logger.debug('GET PROFILE PIC {}'.format(image_url))

            context['sosmed_pic'] = image_url

    if profile.photo_profile:
        context['profile_pic'] = profile.photo_profile.url

    context['user_watching'] = UserWatching.objects.filter(
        status__in=[UserWatching.WATCHING, UserWatching.HOLDING, UserWatching.FINISHED_WATCHING]).order_by('-updated')[
                               :10]

    return render(request, 'euphonime/profile/public_profile.html', context)


@login_required
@transaction.atomic
def create_story(request, id):
    usr_prof = ProfileUser.objects.filter(id=id).first()
    if not usr_prof:
        return redirect('finish_signup')

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            try:
                UserPost.objects.create(
                    user=usr_prof,
                    content=content,
                )
            except Exception as e:
                return redirect('profile')
    return redirect('profile')


@login_required
@transaction.atomic
def delete_story(request, id):
    usr_story = UserPost.objects.filter(id=id).first()
    if not usr_story:
        return redirect('finish_signup')

    if request.method == 'POST':
        try:
            usr_story.delete()
        except Exception as e:
            return redirect('profile')
    return redirect('profile')


def read_story(request, id):
    usr_story = get_object_or_404(UserPost, id=id)

    user = usr_story.user.user
    social = UserSocialAuth.objects.filter(user=user).first()
    allauth = SocialAccount.objects.filter(user=user).first()
    profile = ProfileUser.objects.filter(user=user).first()

    logger.debug('AUTHENTICATION FROM SOCIAL MEDIA {}'.format(allauth))

    context = {
        # 'author': username,
        'profile': profile,
        'story': usr_story,
    }

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

    if usr_story.user.photo_profile:
        context['profile_pic'] = usr_story.user.photo_profile.url

    return render(request, 'euphonime/profile/read_story.html', context)
