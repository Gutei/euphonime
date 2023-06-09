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
from django.utils.text import Truncator
from django.utils.safestring import mark_safe
from django.urls import reverse

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

    usr_story = UserPost.objects.filter(user=profile).order_by('-updated')[:100]
    us_st = []
    for s in usr_story:
        release_content = s.content
        truncated_text = Truncator(release_content).words(150)

        us_st.append({
            'id': s.id,
            'story': release_content,
            'created': s.created,
            'updated': s.updated,
        })

    paginator = Paginator(us_st, 1)  # Show 25 contacts per page
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
    if biod:
        escape_biod = re.sub(r'<script.+?</script>', '', biod, flags=re.DOTALL)
    else:
        escape_biod = ""

    context['biodata'] = escape_biod

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

    if request.GET.get('fail') and request.GET.get('fail') == '4':
        context['message_fail'] = "Gagal mengubah username. Username sudah digunakan."

    if request.GET.get('fail') and request.GET.get('fail') == '5':
        context['message_fail'] = "Gagal mengubah username. Simbol mordred telah habis. Username haya dapat diubah maksimal 3x."

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
        username = request.POST.get('username')
        photo = request.FILES.get('photo', False)
        if biodata:
            photo = None
            usr_prof.biodata = biodata
        if birth_date:
            usr_prof.birth_date = ps.parse(birth_date)
        if gender:
            usr_prof.gender = gender
        if username:
            if usr_prof.symbol < 1:
                return redirect("{}?{}".format(reverse('profile'), 'fail=5'))
            usrnm = User.objects.filter(username=username).first()
            if usrnm:
                return redirect("{}?{}".format(reverse('profile'), 'fail=4'))
            usr_prof.symbol -= 1
            usr_prof.save()

            usrnm = request.user
            usrnm.username = username
            usrnm.save()

        if photo:
            usr_prof.photo_profile = request.FILES['photo']
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
    usr_story = UserPost.objects.filter(user=profile).order_by('-updated')[:100]
    claimed_watch = UserWatching.objects.filter(user=profile).count()

    ust_parse = []

    for u_p in usr_story:
        img = re.search('<img src="([^"]+)"'[4:], u_p.content)
        display_img = None
        img_thread_url = None
        no_prefix = None
        if img:
            display_img = img.group().strip('"')
            if display_img.split('"')[0] == " src=":
                no_prefix = display_img.split('"')[1]
                if no_prefix.split(':')[0] == 'https' or no_prefix.split(':')[0] == 'http':
                    img_thread_url = no_prefix
                else:
                    img_thread_url = None

        ust_parse.append({
            'id': u_p.id,
            'created': u_p.created,
            'content': u_p.content,
            'updated': u_p.updated,
            'img': None if not img_thread_url else img_thread_url,
        })

    paginator = Paginator(ust_parse, 3)  # Show 25 contacts per page
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
        status__in=[UserWatching.WATCHING, UserWatching.HOLDING, UserWatching.FINISHED_WATCHING],
        user=profile).order_by('-updated')[
                               :10]

    context['claimed_watch'] = claimed_watch if claimed_watch > 0 else None

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

    img = re.search('<img src="([^"]+)"'[4:], usr_story.content)
    display_img = None
    img_thread_url = None
    no_prefix = None
    if img:
        display_img = img.group().strip('"')
        if display_img.split('"')[0] == " src=":
            no_prefix = display_img.split('"')[1]
            if no_prefix.split(':')[0] == 'https' or no_prefix.split(':')[0] == 'http':
                img_thread_url = no_prefix
            else:
                img_thread_url = None

    logger.debug('AUTHENTICATION FROM SOCIAL MEDIA {}'.format(allauth))

    context = {
        # 'author': username,
        'profile': profile,
        'story': usr_story,
        'img_thread_url': img_thread_url,
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


@login_required
@transaction.atomic
def update_story(request, id):
    old_story = get_object_or_404(UserPost, id=id)

    if request.method == 'POST':
        content = request.POST.get('content')
        old_story.content = content
        if content:
            try:
                old_story.save()
            except Exception as e:
                return redirect('profile')
    return redirect('profile')
