import uuid
from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from euphonime.tasks import send_email_to_user


class ProfileUser(models.Model):

    MALE = 1
    FEMALE = 2

    GENDER = (
        (MALE, 'Laki-laki'),
        (FEMALE, 'Perempuan'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo_profile = models.ImageField(upload_to='user/profile', null=True, blank=True)
    biodata = models.TextField(null=True, blank=True)
    gender = models.PositiveIntegerField(choices=GENDER, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    website = models.CharField(max_length=512, null=True, blank=True)
    symbol = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        db_table = 'user_profiles'

    def __str__(self):
        return '{}'.format(self.user.email)

    def save(self, *args, **kwargs):
        exist = ProfileUser.objects.filter(user=self.user).first()
        if not exist:  # object is being created, thus no primary key field yet
            self.symbol = 3
            username = self.user.username
            sender = 'projecteupho@gmail.com'
            email = []
            email.append(self.user.email)
            recipients = email
            subject = "Terimakasih telah begabung bersama kami"
            reply = "Selamat datang {},<br>Jangan takut, kami benci spam!<br>" \
                    "Euphonime adalah media, database anime, dan situs komunitas untuk penggemar anime yang dapat saling berinteraksi di Indonesia.<br><br>" \
                    "Euphonime mendukung segala upaya untuk memajukan kreatif industri anime sebagai media jurnalisme, komunitas, dan database anime di Indonesia.<br><br>" \
                    "Kirimkan siaran pers, aktivitas usaha, event anime dan karya kreatif yang nantinya akan dimuat di Euphonime melalui email:projecteupho@gmail.com<br><br>" \
                    "<a href='https://euphonime.com/'>Bersenang-senanglah!!</a>".format(self.user.username)
            content = "<div style='max-width:400px;'>{}</div><hr><img src='https://euphonime.com/static/euphonime/img/contact-media-partner.jpg' style='max-width:400px;'><br>".format(
                reply)
            send_email_to_user.apply_async((username, sender, recipients, subject, content), )

        super(ProfileUser, self).save(*args, **kwargs)


class UserWatching(models.Model):
    WATCHING = 1
    FINISHED_WATCHING = 2
    HOLDING = 3
    STOP_WATCHING = 4

    STATE = (
        (WATCHING, 'Sedang ditonton'),
        (FINISHED_WATCHING, 'Selesai ditonton'),
        (HOLDING, 'Menunda'),
        (STOP_WATCHING, 'Tidak melanjutkan'),
    )

    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('ProfileUser', null=True, blank=True, on_delete=models.CASCADE)
    anime = models.ForeignKey('Anime', null=True, blank=True, on_delete=models.CASCADE)
    status = models.PositiveIntegerField(choices=STATE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_watching'


class UserAnimeScore(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('ProfileUser', null=True, blank=True, on_delete=models.CASCADE)
    anime = models.ForeignKey('Anime', null=True, blank=True, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_anime_scores'


class UserPolls(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('ProfileUser', null=True, blank=True, on_delete=models.CASCADE)
    anime = models.ForeignKey('Anime', null=True, blank=True, on_delete=models.CASCADE)
    poll = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_polls'
        verbose_name = 'Polling'


class UserAnimeReview(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('ProfileUser', null=True, blank=True, on_delete=models.CASCADE)
    anime = models.ForeignKey('Anime', null=True, blank=True, on_delete=models.CASCADE)
    review = RichTextUploadingField(blank=True, null=True,)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_reviews'
        verbose_name = 'Anime Review From User'


class UserMessage(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('ProfileUser', null=True, blank=True, on_delete=models.CASCADE)
    message = models.TextField(blank=True, null=True,)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_messages'
        verbose_name = 'Pesan Untuk Developer'


class UserPost(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('ProfileUser', null=True, blank=True, on_delete=models.CASCADE)
    content = RichTextUploadingField(blank=True, null=True,)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_posts'