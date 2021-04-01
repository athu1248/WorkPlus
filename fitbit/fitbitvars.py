from .models import FitBitUser
import base64
import requests
from datetime import date

# get encoded string values from fitbit's web api developer website
def getEncodedStr():
    client_id = "22C5N8"        # ADD YOUR OWN CLIENT ID USING FITBIT API !
    client_secret = "dbd26beefb6532a2f5875700bd6f2830"    # ADD YOUR OWN CLIENT SECRET KEY USING FITBIT API !
    #ADD YOUR OWN CLIENT ID in navbar->nav-item->Connect to Fitbit->a in BASE1.html
    authorizationStr = client_id+":"+client_secret

    encodedBytes = base64.b64encode(authorizationStr.encode("utf-8"))
    encodedStr = str(encodedBytes, "utf-8")

    return encodedStr


# get number of daily steps from authenticated user's fitbit
def getSteps(user):
    url = f"https://api.fitbit.com/1/user/{user.fitbituser.fitbit_user_id}/activities/steps/date/today/today.json"
    activity_request = requests.get(url, headers={
        "Authorization": f"{user.fitbituser.token_type} " + f"{user.fitbituser.access_token}"
    })
    activity_request = activity_request.json()

    if "errors" in activity_request:
        refreshToken(user)
        # Trying to get data again
        url = f"https://api.fitbit.com/1/user/{user.fitbituser.fitbit_user_id}/activities/steps/date/today/today.json"
        activity_request = requests.get(url, headers={
            "Authorization": f"{user.fitbituser.token_type} " + f"{user.fitbituser.access_token}"
        })
        activity_request = activity_request.json()
        if "errors" in activity_request:
            return "not available"

    print(activity_request)
    steps = activity_request["activities-steps"][0]["value"]
    print("Steps=", steps)
    return steps


# get number of daily calories from authenticated user's fitbit
def getCalories(user):
    url = f"https://api.fitbit.com/1/user/{user.fitbituser.fitbit_user_id}/activities/calories/date/today/today.json"
    activity_request = requests.get(url, headers={
        "Authorization": f"{user.fitbituser.token_type} " + f"{user.fitbituser.access_token}"
    })
    activity_request = activity_request.json()

    if "errors" in activity_request:
        refreshToken(user)
        # Trying to get data again
        url = f"https://api.fitbit.com/1/user/{user.fitbituser.fitbit_user_id}/activities/calories/date/today/today.json"
        activity_request = requests.get(url, headers={
            "Authorization": f"{user.fitbituser.token_type} " + f"{user.fitbituser.access_token}"
        })
        activity_request = activity_request.json()
        if "errors" in activity_request:
            return "not available"

    calories = activity_request["activities-calories"][0]["value"]
    print("Calories=", calories)
    return calories


# get current body weight from authenticated user's fitbit
def getWeight(user):
    url = f"https://api.fitbit.com/1/user/{user.fitbituser.fitbit_user_id}/body/weight/date/today/today.json"
    activity_request = requests.get(url, headers={
        "Authorization": f"{user.fitbituser.token_type} " + f"{user.fitbituser.access_token}"
    })
    activity_request = activity_request.json()

    if "errors" in activity_request:
        refreshToken(user)
        # Trying to get data again
        url = f"https://api.fitbit.com/1/user/{user.fitbituser.fitbit_user_id}/body/weight/date/today/today.json"
        activity_request = requests.get(url, headers={
            "Authorization": f"{user.fitbituser.token_type} " + f"{user.fitbituser.access_token}"
        })
        activity_request = activity_request.json()
        if "errors" in activity_request:
            return "not available"

    weight = activity_request["body-weight"][0]["value"]
    print("Weight =", weight)
    return weight


# get daily distance covered from authenticated user's fitbit
def getDistance(user):
    url = f"https://api.fitbit.com/1/user/{user.fitbituser.fitbit_user_id}/activities/distance/date/today/today.json"
    activity_request = requests.get(url, headers={
        "Authorization": f"{user.fitbituser.token_type} " + f"{user.fitbituser.access_token}"
    })
    activity_request = activity_request.json()

    if "errors" in activity_request:
        refreshToken(user)
        # Trying to get data again
        url = f"https://api.fitbit.com/1/user/{user.fitbituser.fitbit_user_id}/activities/distance/date/today/today.json"
        activity_request = requests.get(url, headers={
            "Authorization": f"{user.fitbituser.token_type} " + f"{user.fitbituser.access_token}"
        })
        activity_request = activity_request.json()
        if "errors" in activity_request:
            return "not available"

    distance = round(float(activity_request["activities-distance"][0]["value"]), 2)
    print("Distance =", distance)
    return distance


# get daily sleep hours from authenticated user's fitbit
def getSleep(user):
    dateToday = date.today().strftime("%Y-%m-%d")
    url = f"https://api.fitbit.com/1.2/user/{user.fitbituser.fitbit_user_id}/sleep/date/{dateToday}.json"
    activity_request = requests.get(url, headers={
        "Authorization": f"{user.fitbituser.token_type} " + f"{user.fitbituser.access_token}"
    })
    activity_request = activity_request.json()

    if "errors" in activity_request:
        refreshToken(user)
        # Trying to get data again
        url = f"https://api.fitbit.com/1.2/user/{user.fitbituser.fitbit_user_id}/sleep/date/{dateToday}.json"
        activity_request = requests.get(url, headers={
            "Authorization": f"{user.fitbituser.token_type} " + f"{user.fitbituser.access_token}"
        })
        activity_request = activity_request.json()
        if "errors" in activity_request:
            return "not available"

    sleep = activity_request["summary"]["totalMinutesAsleep"]
    print("Sleep =", sleep)
    return sleep


# get body fat data from authenticated user's fitbit
def getBodyFat(user):
    dateToday = date.today().strftime("%Y-%m-%d")
    url = f"https://api.fitbit.com/1/user/{user.fitbituser.fitbit_user_id}/body/log/fat/date/{dateToday}.json"
    activity_request = requests.get(url, headers={
        "Authorization": f"{user.fitbituser.token_type} " + f"{user.fitbituser.access_token}"
    })
    activity_request = activity_request.json()

    if "errors" in activity_request:
        refreshToken(user)
        # Trying to get data again
        url = f"https://api.fitbit.com/1/user/{user.fitbituser.fitbit_user_id}/body/log/fat/date/{dateToday}.json"
        activity_request = requests.get(url, headers={
            "Authorization": f"{user.fitbituser.token_type} " + f"{user.fitbituser.access_token}"
        })
        activity_request = activity_request.json()
        if "errors" in activity_request:
            return "not available"

    bodyFat = activity_request["fat"]
    print("BodyFat =", bodyFat)
    return bodyFat


# get steps, calories & distance goals from authenticated user's fitbit
def getActivityGoals(user):
    url = f"https://api.fitbit.com/1/user/{user.fitbituser.fitbit_user_id}/activities/goals/daily.json"
    activity_request = requests.get(url, headers={
        "Authorization": f"{user.fitbituser.token_type} " + f"{user.fitbituser.access_token}"
    })
    activity_request = activity_request.json()

    if "errors" in activity_request:
        refreshToken(user)
        # Trying to get data again
        url = f"https://api.fitbit.com/1/user/{user.fitbituser.fitbit_user_id}/activities/goals/daily.json"
        activity_request = requests.get(url, headers={
            "Authorization": f"{user.fitbituser.token_type} " + f"{user.fitbituser.access_token}"
        })
        activity_request = activity_request.json()
        if "errors" in activity_request:
            return "not available", "not available", "not available"

    stepsGoals = activity_request["goals"]["steps"]
    caloriesGoals = activity_request["goals"]["caloriesOut"]
    distanceGoals = activity_request["goals"]["distance"]

    print("Steps Goals =", stepsGoals)
    print("Calories Goals =", caloriesGoals)
    print("Distance Goals =", distanceGoals)

    return stepsGoals, caloriesGoals, distanceGoals


# get weight goals from authenticated user's fitbit
def getWeightGoals(user):
    url = f"https://api.fitbit.com/1/user/{user.fitbituser.fitbit_user_id}/body/log/weight/goal.json"
    activity_request = requests.get(url, headers={
        "Authorization": f"{user.fitbituser.token_type} " + f"{user.fitbituser.access_token}"
    })
    activity_request = activity_request.json()

    if "errors" in activity_request:
        refreshToken(user)
        # Trying to get data again
        url = f"https://api.fitbit.com/1/user/{user.fitbituser.fitbit_user_id}/body/log/weight/goal.json"
        activity_request = requests.get(url, headers={
            "Authorization": f"{user.fitbituser.token_type} " + f"{user.fitbituser.access_token}"
        })
        activity_request = activity_request.json()
        if "errors" in activity_request:
            return "not available"

    weightGoals = "not defined"
    if "weight" in activity_request["goal"]:
        weightGoals = activity_request["goal"]["weight"]
        print("Weight Goals =", weightGoals)

    return weightGoals


# get body fat goals from authenticated user's fitbit
def getFatGoals(user):
    url = f"https://api.fitbit.com/1/user/{user.fitbituser.fitbit_user_id}/body/log/fat/goal.json"
    activity_request = requests.get(url, headers={
        "Authorization": f"{user.fitbituser.token_type} " + f"{user.fitbituser.access_token}"
    })
    activity_request = activity_request.json()

    if "errors" in activity_request:
        refreshToken(user)
        # Trying to get data again
        url = f"https://api.fitbit.com/1/user/{user.fitbituser.fitbit_user_id}/body/log/fat/goal.json"
        activity_request = requests.get(url, headers={
            "Authorization": f"{user.fitbituser.token_type} " + f"{user.fitbituser.access_token}"
        })
        activity_request = activity_request.json()
        if "errors" in activity_request:
            return "not available"

    print(activity_request)
    fatGoals = " not defined"
    if "fat" in activity_request["goal"]:
        fatGoals = activity_request["goal"]["fat"]
        print("Weight Goals =", fatGoals)

    return fatGoals


# get sleep goals from authenticated user's fitbit
def getSleepGoals(user):
    url = f"https://api.fitbit.com/1/user/{user.fitbituser.fitbit_user_id}/sleep/goal.json"
    activity_request = requests.get(url, headers={
        "Authorization": f"{user.fitbituser.token_type} " + f"{user.fitbituser.access_token}"
    })
    activity_request = activity_request.json()

    if "errors" in activity_request:
        refreshToken(user)
        # Trying to get data again
        url = f"https://api.fitbit.com/1/user/{user.fitbituser.fitbit_user_id}/sleep/goal.json"
        activity_request = requests.get(url, headers={
            "Authorization": f"{user.fitbituser.token_type} " + f"{user.fitbituser.access_token}"
        })
        activity_request = activity_request.json()
        if "errors" in activity_request:
            return "not available"

    sleepGoals = activity_request["goal"]["minDuration"]
    print("Weight Goals =", sleepGoals)

    return sleepGoals


# get user's fitbit API refresh token  
def refreshToken(user):
    encodedStr = getEncodedStr()
    refresh = requests.post(
        f"https://api.fitbit.com/oauth2/token?grant_type=refresh_token&refresh_token={user.fitbituser.refresh_token}",
        headers={
            "Authorization": f"Basic {encodedStr}",
            "Content-Type": "application/x-www-form-urlencoded"
        })
    data = refresh.json()
    fbu = FitBitUser(user_id=user,
                     access_token=data["access_token"],
                     expires_in=data["expires_in"],
                     refresh_token=data["refresh_token"],
                     scope=data["scope"],
                     token_type=data["token_type"],
                     fitbit_user_id=data["user_id"],
                     )
    fbu.save(update_fields=["access_token", "expires_in",
                            "refresh_token", "scope", "token_type", "fitbit_user_id"])

# add user's extracted fitbit data to variables
def getFitbitData(user):
    if (FitBitUser.objects.filter(user_id=user)):
        # Trying to obtain activity
        steps = getSteps(user)
        calories = getCalories(user)
        weight = getWeight(user)
        distance = getDistance(user)
        sleep = getSleep(user)
        bodyFat = getBodyFat(user)
        stepsGoals, caloriesGoals, distanceGoals = getActivityGoals(user)
        weightGoals = getWeightGoals(user)
        fatGoals = getFatGoals(user)
        sleepGoals = getSleepGoals(user)

    return {
        "steps": steps,
        "calories": calories,
        "weight": weight,
        "distance": distance,
        "sleep": sleep,
        "bodyFat": bodyFat,
        "stepsGoals": stepsGoals,
        "caloriesGoals": caloriesGoals,
        "weightGoals": weightGoals,
        "distanceGoals": distanceGoals,
        "sleepGoals": sleepGoals,
        "fatGoals": fatGoals
    }
