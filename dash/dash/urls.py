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
                  url(r'^anime/(?P<pk>[^/]+)/$', views.get_anime, name='anime'),
                  url(r'^article/(?P<pk>[^/]+)/$', views.get_article, name='article'),
                  url(r'^auth-login/', views.auth_login, name='auth_login'),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                document_root=settings.MEDIA_ROOT)
