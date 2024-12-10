from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='app/login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('inicio/', views.inicio, name='inicio'),
    #path('login_redirect/', views.login_redirect, name='login_redirect'),
    path('main/',views.main, name='main'),
    path('main/start/',views.start_simulation,name='start'),
    path('restart/',views.restart_machines,name='restart'),
    path('main/confirmar/',views.confirmar,name='confirmar'),
    path('main/listar/',views.vista,name='listar'),
    path('main/revision', views.make_revision,name='revision'),
    path('main/work', views.work,name='work'),
    path('main/s_e', views.sup_engineer,name='s_e'),
    path('main/s_t', views.sup_tecnician,name='s_t'),
]