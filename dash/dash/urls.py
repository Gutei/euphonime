"""dash URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls import url, include
from euphonime import views

admin.site.site_header = 'EUPHONIME - GOD MODE'

urlpatterns = [
                  url(r'^jet', include('jet.urls', 'jet')),
                  url(r'^ckeditor/', include('ckeditor_uploader.urls')),
                  url(r'^teh-olong/', admin.site.urls),
                  url(r'^login/$', views.login, name='login'),
                  url(r'^register/$', views.register, name='register'),
                  url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
                  url(r'^accounts/', include('allauth.urls')),
                  url(r'^$', views.home, name='home'),
                  url(r'^finish-signup/', views.finish_signup, name='finish_signup'),

                  # Profil
                  url(r'^profile/', views.profile, name='profile'),
                  url(r'^edit-profile/(?P<id>[^/]+)/$', views.edit_profile, name='edit_profile'),
                  url(r'^mordred/(?P<id>[^/]+)/$', views.contact_modred, name='mordred'),
                  url(r'^user/(?P<username>[^/]+)/$', views.public_profile, name='public_profile'),
                  url(r'^user/page/(?P<id>[^/]+)/$', views.read_story, name='read_story'),
                  # url(r'^(?P<username>[^/]+)/(?P<id>[^/]+)/$', views.read_story, name='read_story'),
                  url(r'^create-story/(?P<id>[^/]+)/$', views.create_story, name='create_story'),
                  url(r'^delete-story/(?P<id>[^/]+)/$', views.delete_story, name='delete_story'),
                  url(r'^update-story/(?P<id>[^/]+)/$', views.update_story, name='update_story'),

                  # Anime
                  url(r'^anime/(?P<pk>[^/]+)/(?P<slug>[^/]+)/$', views.get_anime, name='anime'),
                  url(r'^rate-anime/(?P<anime_id>[^/]+)/(?P<rate>[^/]+)/$', views.save_rate, name='rate_anime'),
                  url(r'^watch-anime/(?P<anime_id>[^/]+)/$', views.save_watching, name='watch_anime'),
                  url(r'^anime/$', views.list_anime, name='list_anime'),

                  # Article
                  url(r'^artikel/(?P<pk>[^/]+)/(?P<slug>[^/]+)/$', views.get_article, name='article'),
                  url(r'^artikel/$', views.list_article, name='list_article'),

                  # Quote
                  url(r'^quotes/$', views.list_quote, name='list_quote'),

                  # Character
                  url(r'^karakter/(?P<pk>[^/]+)/(?P<slug>[^/]+)/$', views.get_character, name='character'),
                  url(r'^karakter/$', views.list_character, name='list_character'),

                  # Footer Conrtent
                  url(r'^disclaimer/$', views.get_disclaimer, name='disclaimer'),
                  url(r'^privacy-policy/$', views.get_privacy_policy, name='privacy_policy'),

                  # Contact
                  url(r'^contact-&-media-partner/$', views.get_contact, name='contact'),

                  url(r'^sitemap.xml', views.get_sitemaps, name='sitemaps'),
                  url(r'^robots.txt', views.robots_txt, name='robots'),

                  url(r'^auth-login/', views.auth_login, name='auth_login'),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                                           document_root=settings.MEDIA_ROOT)
