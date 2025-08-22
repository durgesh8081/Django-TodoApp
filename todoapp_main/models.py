from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    priority = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField()
    user = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, related_name="tasks"
    )

    def __str__(self):
        return self.title
