from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.index),
    path('registration', views.create_user, name="create_user"),
    path('login',views.login, name="login"),
    path('add/jobb',views.add_job, name="add_job"),
    path('logout',views.logout, name="logout"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('views/<int:job_id>', views.show_job, name="show_job"),
    path('edit/<int:job_id>', views.edit_job, name="edit_job"),
    path('join/<int:job_id>', views.join, name="join"),
    path('delete/<int:job_id>', views.delete, name="delete"),   
]