import datetime
from django.shortcuts import render
from django.db.models import F
from fitbit.fitbitvars import getSteps, getSleep, getCalories

from fitbit.models import FitBitUser
from workgroups.models import  WorkGroup, WorkGroupUser

from .models import fitnessPoints, quizUser, runImage
from .forms import runImageForm, quizUserForm
from .randomquestion import Quiz

import cv2 
import pytesseract
import fnmatch
import uuid

# Create your views here.


# checks user's nike run daily challenge & trivia of the day to reward points
def home(request, groupid):
    groupuuid = uuid.UUID(groupid)
    if WorkGroup.objects.filter(groupID=groupuuid).exists():
        workGroup = WorkGroup.objects.get(groupID=groupuuid)
        if(request.user.workgroupuser_set.filter(work_group=workGroup).exists()):

            fileCheckMessage = ""
            quizMessage = ""

            # extract data from user's nike run screenshot using image recognition
            if request.method == "POST":
                if "addRunImageSubmit" in request.POST:
                    addRunImageForm = runImageForm(request.POST, request.FILES)
                    if addRunImageForm.is_valid():
                        dateToday = datetime.date.today()
                        print(runImage.objects.filter(user=request.user).filter(date_added = dateToday).exists())
                        if runImage.objects.filter(user=request.user).filter(date_added=dateToday).exists():
                            fileCheckMessage = "Run added today already. Enough for today."
                        else:
                            addRunImageForm.save()
                            img_obj = cv2.imread("media/run_images/" + f"{request.FILES['image']}")
                            img_obj = cv2.resize(img_obj, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
                            img_obj = cv2.cvtColor(img_obj, cv2.COLOR_BGR2GRAY)
                            cv2.threshold(cv2.bilateralFilter(img_obj, 5, 75, 75), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

                            bool1, fileCheckMessage = checkRun(img_obj)
                            if bool1:
                                newFitnessPoint = fitnessPoints()
                                newFitnessPoint.user = request.user
                                newFitnessPoint.points = 10
                                newFitnessPoint.save()
                            else:
                                runImage.objects.filter(user=request.user).filter(date_added=dateToday).delete()

                if "quizAnswer" in request.POST:
                    dateToday = datetime.date.today()
                    if quizUser.objects.filter(user=request.user).filter(date_added=dateToday).exists():
                        quizMessage = "You have already attempted today's daily trivia"
                    else:
                        quizForm = quizUserForm(request.POST)
                        if "answer" in request.POST:
                            response = request.POST["answer"]
                            option = request.POST["correct"]

                            if response == option:
                                quizMessage = 'Correct! +10 PTS! Come back tomorrow for more:)'
                                newFitnessPoint = fitnessPoints()
                                newFitnessPoint.user = request.user
                                newFitnessPoint.points = 10
                                newFitnessPoint.save()

                            else:
                                quizMessage = f'Incorrect! Correct answer is {option} Come back tomorrow for more:)'



                            quizUserToAdd = quizUser()
                            quizUserToAdd.user = request.user
                            quizUserToAdd.question = request.POST["question"]
                            quizUserToAdd.correct = request.POST["correct"]
                            quizUserToAdd.answer = request.POST["answer"]
                            quizUserToAdd.save()


                        else:
                            quizUserToAdd = quizUser()
                            quizUserToAdd.user = request.user
                            quizUserToAdd.question = request.POST["question"]
                            quizUserToAdd.correct = request.POST["correct"]
                            quizUserToAdd.save()
                            quizMessage = f'Incorrect! Correct answer is {request.POST["correct"]} Come back tomorrow for more:)'



            members, addRunImageForm = getAllWorkGroupFitnessData(workGroup, request.user)
            dateToday = datetime.date.today()
            if quizUser.objects.filter(user=request.user).filter(date_added=dateToday).exists():
                quizForm, quizQuestion, option = "", "", ""
            else:
                quizForm, quizQuestion, option = getQuiz(request.user)
            userPoints = getPoints(request.user)
            totalPoints = getTeamPoints(members)
            userType = getUserType(request.user,workGroup)
            return render(request, "fitness/groupFitness.html", {
                "groupuuid": groupuuid,
                "user": request.user,
                "members":  members,
                "addRunImageForm": addRunImageForm,
                "fileCheckMessage": fileCheckMessage,
                "quizForm": quizForm,
                "quizQuestion": quizQuestion,
                "quizMessage": quizMessage,
                "userPoints": userPoints,
                "teamPoints": totalPoints,
                "userType": userType
            })
    
    return render(request, "users/home.html", {})


# get fitbit data of all team members
def getAllWorkGroupFitnessData(workGroup, user):
    groupUsers = WorkGroupUser.objects.filter(work_group=workGroup)
    members = []
    for groupUser in groupUsers:
        if FitBitUser.objects.filter(user_id=groupUser.user).exists():
            members.append({
                "username": groupUser.user.username, 
                "steps": getSteps(groupUser.user), 
                "calories": getCalories(groupUser.user), 
                "sleep": getSleep(groupUser.user),
                "points": getPoints(groupUser.user),
                })
        else:
            members.append({
                "username": groupUser.user.username,
                "steps": "not available",
                "calories": "not available",
                "sleep": "not available",
                "points": getPoints(groupUser.user),
            })
    """
    msgs = []
    chatObjs = Chat.objects.filter(
        work_group=workGroup).order_by("dateCreated")
    for chatObj in chatObjs:
        msgs.append([chatObj.author.username, chatObj.message])
    """

    addRunImageForm = runImageForm()
    addRunImageForm.initial["work_group_user"] = WorkGroupUser.objects.filter(work_group=workGroup).get(user=user)
    addRunImageForm.initial["user"] = user

    return members, addRunImageForm


# get your personal points
def getPoints(user):
    year = str(datetime.datetime.today().year)
    month =  str(datetime.datetime.today().month)
    pointsObjs = fitnessPoints.objects.filter(user=user).filter(date_added__year=year, date_added__month=month)
    totalPoints = 0
    for pointsObj in pointsObjs:
        totalPoints += pointsObj.points
    return totalPoints


# get your team members' points
def getTeamPoints(members):
    totalPoints = 0
    for member in members:
        totalPoints += member["points"]
    return totalPoints


# check whether user is a leader or a member
def getUserType(user, workgroup):
    workgroupuser = WorkGroupUser.objects.filter(work_group=workgroup).filter(user=user)[0]
    userType = workgroupuser.userType
    return userType


# check whether user has met the running criteria from screenshot using data from image recognition
def checkRun(img):
    print("here")
    text = pytesseract.image_to_string(img)
    run = dict()
    try:
        for i in range(len(text.split())):

            if fnmatch.fnmatch(text.split()[i], "loday"):
                run["Date"] = "Today"
            elif "Kilometers" in text.split()[i]:
                run["Distance"] = float(text.split()[i-1])

        if "Date" not in run.keys():
            run["Date"] = ""

        if run["Date"] == "Today" and run["Distance"] >= 2:
            return (True, 'Good job! +10 PTS')

        elif run["Date"] == "Today" and run["Distance"] < 2:
            return (False, 'You did not run 2km!')

        elif run["Date"] != "Today" and run["Distance"] >= 2:
            return (False, 'The run is not from today!')

        else:
            return (False, 'The run does not meet both the criteria!')
    except:
        return (False, "Image is not valid")

# get trivia answer from the user
def getQuiz(user):
    form = quizUserForm()
    form.initial["user"] = user
    quizOfTheDay = Quiz()

    question = quizOfTheDay.question
    form.initial["question"] = question

    option = quizOfTheDay.answer
    form.initial["correct"] = option

    form.fields["answer"].choices = quizOfTheDay.CHOICES

    return (form, question, option)
