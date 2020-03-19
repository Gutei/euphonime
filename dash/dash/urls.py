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
                  url(r'^admin/', admin.site.urls),
                  url(r'^login/$', views.login, name='login'),
                  url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
                  url(r'^oauth/', include('social_django.urls', namespace='social')),
                  url(r'^$', views.home, name='home'),
                  url(r'^profile/', views.profile, name='profile'),
                  url(r'^finish-signup/', views.finish_signup, name='finish_signup'),

                  # Anime
                  url(r'^anime/(?P<pk>[^/]+)/$', views.get_anime, name='anime'),
                  url(r'^animes/$', views.list_anime, name='list_anime'),

                  # Article
                  url(r'^article/(?P<pk>[^/]+)/$', views.get_article, name='article'),
                  url(r'^articles/$', views.list_article, name='list_article'),

                  # Quote
                  url(r'^quotes/$', views.list_quote, name='list_quote'),

                  # Character
                  url(r'^character/(?P<pk>[^/]+)/$', views.get_character, name='character'),
                  url(r'^characters/$', views.list_character, name='list_character'),

                  url(r'^auth-login/', views.auth_login, name='auth_login'),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                                           document_root=settings.MEDIA_ROOT)
