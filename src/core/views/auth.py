from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib import auth
from django.views.decorators.http import require_POST
from django.db.models import Q

from django.conf import settings

from utils.redirect_check import redirect_after_login


def login(request):
    """ login the user """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect_after_login(request)

        # wrong credentials
        redirect_to = request.path
        if request.GET.get("next"):
            redirect_to += f"?next={request.GET.get('next')}"
        return redirect(redirect_to)

    else:
        if request.user.is_authenticated:
            # user already login
            return redirect("index")
        return render(request, "core/login.html", {"next": request.GET.get("next")})


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        user_exists = (
            get_user_model()
            .objects.filter(Q(username=username) | Q(email=email))
            .exists()
        )
        if user_exists:
            print("can't use the username or password")
            return redirect("register")

        user = get_user_model().objects.create_user(
            username=username, email=email, password=password
        )
        auth.login(request, user)
        return redirect(settings.LOGIN_REDIRECT_URL)

    else:
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return render(request, "core/register.html")


@require_POST
def logout(request):
    auth.logout(request)
    print("Log user out")
    return redirect("index")
