from django.urls import path, include
from django.urls.resolvers import URLPattern
from django.contrib.auth import views as auth_views
from . import views

app_name = 'account'

urlpatterns = [
    #post views
    path('login/',views.user_login,name='login'),

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
    path('',views.dashboard,name='dashboard'),
    #others
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
 
    
]