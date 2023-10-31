from django.urls import path
from .import views

urlpatterns = [
    path('sign-up/',views.register_views,name="sign-up"),
    path('sign-in/',views.login,name="sign-in"),
    path('sign-out/',views.logout,name="sign-out"),
    #edit profile
    path('profile/update/',views.profile_update,name="profile-update"),
]
