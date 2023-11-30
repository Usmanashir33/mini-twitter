""" users app urls file"""
from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("register/",views.register,name="register"),
    path("profile/",views.fill_profile,name="fill-profile"),
    path("profile/<int:pk>",views.UserDetailView.as_view(),name="user-detail"),
    path("profile/update/<int:pk>",views.user_profile_update,name="profile-update"),
    #path("viewprofile/<int:pk>",views.view_user_profile,name="view-user-profile"),
    path("following/<int:pk>",views.following_friend,name="follow-friend"),
    path("followers/<int:pk>",views.followers,name="followers"),
    path("followings/<int:pk>",views.followings,name="followings"),
    path("searching/friend",views.search_any_friend,name="search-any-friend"),
    
    path("settings",views.settings,name="settings"),
    path("auth/logout",views.user_logout,name="log-out"),
    path("auth/login",views.user_login,name="log-in"),
    path("authe/",include("django.contrib.auth.urls")),
    #path("auth/change/password",auth_views.PasswordChangeView.as_view(template_name="registration/change_password.html"),name="change_password"),
    path("auth/change/password",views.PasswordsChangingView.as_view(),name="change_password"),
    
    
]
