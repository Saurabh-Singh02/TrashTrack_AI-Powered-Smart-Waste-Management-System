from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),  
    path('login/', views.login_view, name='login'), 
    path('logout/', views.logout_view, name='logout'), 
    path('company-portal/signup/', views.company_signup, name='company_signup'), 
    path('dashboard/', views.dashboard, name='dashboard'), 
    path('map/', views.map_view, name='map_view'),  
    path('smart-bins/', views.smart_bins, name='smart_bins'),  
    path('smart-bins/update/<int:bin_id>/', views.update_bin_fill_level, name='update_bin_fill_level'),  
    path('tracking/', views.tracking, name='tracking'),  
    path('dumping-area/', views.dumping_area, name='dumping_area'), 
    path('company-portal/', views.company_portal, name='company_portal'),  
]
