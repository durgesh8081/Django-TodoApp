from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from todoapp_main.models import Task
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
from django.utils import timezone


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")


class ProfileView(generic.DetailView):
    template_name = "todoapp_main/profile.html"


def index(request):
    context = {"now": timezone.now()}

    user = request.user
    if user.is_authenticated:
        tasks = Task.objects.filter(user=user)

        priority = request.GET.get("priority")
        if priority:
            tasks = tasks.filter(priority=priority)

        status = request.GET.get("status")
        if status:
            tasks = tasks.filter(status=status)
        context["tasks"] = tasks

    return render(request, "todoapp_main/index.html", context=context)


@login_required
def create_task(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        priority = request.POST.get("priority")
        deadline_str = request.POST.get("deadline")  # String from form

        # Basic validation
        if not title or not description or not priority:
            messages.error(request, "All fields are required!")
        else:
            Task.objects.create(
                title=title,
                description=description,
                priority=priority,
                status="pending",
                user=request.user,
                deadline=datetime.strptime(deadline_str, "%Y-%m-%d"),
            )
            messages.success(request, "Task created successfully!")
            return redirect("index")

    return render(request, "create_task.html")


@login_required
def update_task_status(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status in ["done", "cancelled"]:
            task.status = new_status
            task.save()
            messages.success(request, f"Task marked as {new_status}.")
        else:
            messages.error(request, "Invalid status update.")

    return redirect("index")
