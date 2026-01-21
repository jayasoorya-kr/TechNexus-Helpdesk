from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from tickets import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('ticket/new/', views.create_ticket, name='create_ticket'),
    
    # NEW: Chat/Detail View
    path('ticket/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),

    path('ticket/<int:ticket_id>/assign/', views.assign_ticket, name='assign_ticket'),
    path('ticket/<int:ticket_id>/status/', views.update_status, name='update_status'),
    path('user/<int:profile_id>/approve/', views.approve_user, name='approve_user'),
]