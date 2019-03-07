from django.urls import path
from django.conf.urls import url,include
from . import views

app_name = 'tasks'
urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name = 'detail'),
    path('create', views.CreateTask.as_view(), name = 'add_task'),
    path('', views.IndexView.as_view(), name='homepage'),
    path('task/<int:pk>/', views.UpdateTask.as_view(), name = 'update_task'),
    path('task/<int:pk>/delete/', views.DeleteTask.as_view(), name = 'delete_task'),
    path('login', views.LoginView.as_view(), name='login'),
    path('register', views.RegisterView.as_view(), name='register'),
    path('logout', views.logout_view, name='logout'),
    path('login' , views.ClientLoginView.as_view(),name = 'allauth_login'),
    path('signup' , views.ClientSignupView.as_view(),name = 'allauth_signup'),
    path('social' , views.SocialLogin.as_view(),name = 'allauth_social'),
    path('about_me', views.about_me, name = 'about'),
    ]
