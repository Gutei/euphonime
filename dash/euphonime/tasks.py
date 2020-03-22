from __future__ import absolute_import, unicode_literals
import logging
import re
import requests
# Create your tasks here

from celery import shared_task

# from euphonime.models import Anime, Character, VoiceAct

logger = logging.getLogger(__name__)

from euphonime.services.sync_services import get_anime, get_chara

from euphonime.services.send_mail import send_html_email


@shared_task
def sync_anime(mal_id, task_id):

    get_anime(mal_id, task_id)

    return None

@shared_task
def sync_chara(mal_id, anime):

    get_chara(mal_id, anime)

    return None

@shared_task
def send_email_to_user(username, sender, recipients, subject, content):

    send_html_email(username, sender, recipients, subject, content)

    return "Send email to {}".format(recipients[0])