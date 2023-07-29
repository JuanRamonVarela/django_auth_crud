from django.urls import path
from . import views

urlpatterns=[
    path('', views.home, name="home"),
    path('signup/', views.signup, name="signup"),
    path('tasks/', views.tareas, name="tasks"),
    path('tasks/completed/', views.tareas_completas, name="tasks_completed"),
    path('tasks/create/', views.create_task, name="create_task"),
    path('tasks/<int:task_id>/', views.task_detail, name="task_detail"),
    path('tasks/<int:task_id>/completed/', views.task_completed, name="task_completed"),
    path('tasks/<int:task_id>/delete/', views.task_delete, name="task_delete"),
    path('logout/', views.signout, name="logout"),
    path('signin/', views.signin, name="signin")

]