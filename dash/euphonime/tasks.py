from __future__ import absolute_import, unicode_literals
import logging
import re
import requests
# Create your tasks here

from celery import shared_task

# from euphonime.models import Anime, Character, VoiceAct

logger = logging.getLogger(__name__)

from euphonime.services.sync_services import get_anime


@shared_task
def sync_anime(mal_id, task_id):

    get_anime(mal_id, task_id)

    return None