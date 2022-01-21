"""awesomesite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap
from django.conf.urls.static import static
from django.conf import settings
from awesomesite.settings import MEDIA_ROOT
from ..account import account_views
from django.urls.resolvers import URLPattern
from django.contrib.auth import views as auth_views

sitemaps = {
 'posts': PostSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/',include('blog.urls',namespace='blog')),
    path('account/',include('account.urls',namespace='account')),
    path('',include('portfolio.urls',namespace='portfolio')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},name='django.contrib.sitemaps.views.sitemap'),
    # social authentication
    path('social-auth/',include('social_django.urls', namespace='social')),

        #post views
    path('login/',auth_views.user_login,name='login'),

    #authentication views
    # path('login/',auth_views.LoginView.as_view(), name='login'), i am not using this
    path('logout/',auth_views.LogoutView.as_view(), name='logout'),

    #change password urls
    path('password_change/',auth_views.PasswordChangeView.as_view(),name='password_change'),
    path('password_change/done/',auth_views.PasswordChangeDoneView.as_view(),name='password_change_done'),

    #reset password urls
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_complete'),

    #Instead of all that i wrote at the top I can just use this 
    # path('', include('django.contrib.auth.urls')),

    #home page
    path('dashboard/',account_views.dashboard,name='dashboard'),
    #others
    path('register/', account_views.register, name='register'),
    path('edit/', account_views.edit, name='edit'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=MEDIA_ROOT)
