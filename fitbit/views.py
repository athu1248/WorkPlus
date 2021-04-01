from django.contrib.auth.decorators import login_required
from django.db import models
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from datetime import date

from . import fitbitvars
from .models import FitBitUser

from workgroups.models import WorkGroupUser, WorkGroup

import requests
import uuid

# Create your views here.

# using fitbit API to get access to user's fitbit data
def home(request):
    if (request.user.is_authenticated):
        if request.GET.get("code"):
            auth_code = request.GET.get('code')
            url = f"https://api.fitbit.com/oauth2/token?code={auth_code}&grant_type=authorization_code&redirect_uri=http://localhost:8000/fitbit"

            encodedStr = fitbitvars.getEncodedStr()

            raw_data = requests.post(url, headers={
                "Authorization": f"Basic {encodedStr}",
                "Content-Type": "application/x-www-form-urlencoded"
            })
            data = raw_data.json()

            if (FitBitUser.objects.filter(fitbit_user_id=data["user_id"])):
                messages.success(request, "Message: FitBit account has already been used")
                realFitBitUser = FitBitUser.objects.get(fitbit_user_id=data["user_id"])
                fbu = FitBitUser(
                    user_id=realFitBitUser.user_id,
                    access_token=data["access_token"],
                    expires_in=data["expires_in"],
                    refresh_token=data["refresh_token"],
                    scope=data["scope"],
                    token_type=data["token_type"],
                    fitbit_user_id=data["user_id"],
                )
                fbu.save(update_fields=["access_token", "expires_in",
                                        "refresh_token", "scope", "token_type", "fitbit_user_id"])
            else:
                fbu = FitBitUser(
                    user_id=request.user,
                    access_token=data["access_token"],
                    expires_in=data["expires_in"],
                    refresh_token=data["refresh_token"],
                    scope=data["scope"],
                    token_type=data["token_type"],
                    fitbit_user_id=data["user_id"],
                )
                fbu.save()

            return redirect("profile")

    return render(request, "users/home.html", {})


# disconnect from fitbit connection
@login_required
def disconnectConfirmation(request):
    if (FitBitUser.objects.filter(user_id=request.user).exists()):
        token = request.user.fitbituser.access_token
        url = "https://api.fitbit.com/oauth2/revoke?token="+token
        encodedStr = fitbitvars.getEncodedStr()

        response = requests.post(url, headers={
            "Authorization": f"Basic {encodedStr}",
            "Content-Type": "application/x-www-form-urlencoded"
        })

        FitBitUser.objects.filter(user_id=request.user.fitbituser.user_id).delete()

        return redirect("profile")
    
    return render(request, "users/home.html", {})
