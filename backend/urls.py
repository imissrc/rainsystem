from django.urls import path
from . import views
urlpatterns = [
    path('login', views.login),
    path('register', views.register),
    path('logout', views.logout),
    path('findPassword', views.findPassword),
    path('changePassword', views.changePassword),
    path('getUserInfo', views.getUserInfo),
    path('uploadImage', views.uploadImage),
    path('queryImageTaskResult',views.queryImageTaskResult),
    path('uploadVideo', views.uploadVideo),
    path('runVideo', views.runVideo),
    path('queryVideoTaskResult',views.queryVideoTaskResult),
]

