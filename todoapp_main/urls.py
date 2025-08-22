from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("task/", views.create_task, name="create_task"),
    path(
        "tasks/<int:task_id>/update/",
        views.update_task_status,
        name="update_task_status",
    ),
]
