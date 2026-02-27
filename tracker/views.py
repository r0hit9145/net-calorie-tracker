from django.shortcuts import get_object_or_404, redirect, render
from .models import UserProfile
from .forms import UserProfileForm



def user_list(request):
    users = UserProfile.objects.all().order_by("id")
    return render(request, "users/user_list.html", {"users": users})

def user_create(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect("user_detail", user_id=user.id)
    else:
        form = UserProfileForm()

    return render(request, "users/user_form.html", {"form": form})


def user_detail(request, user_id):
    user = get_object_or_404(UserProfile, id=user_id)
    return render(request, "users/user_detail.html", {"user": user})


def user_delete(request, user_id):
    user = get_object_or_404(UserProfile, id=user_id)

    if request.method == "POST":
        user.delete()
        return redirect("user_list")

    return render(request, "users/user_confirm_delete.html", {"user": user})


