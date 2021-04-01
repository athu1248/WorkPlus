import datetime
from workgroups.models import WorkGroupUser
from django.db import models
from users.models import Account

# Create your models here.

# stores user's points gained from challenges
class fitnessPoints(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} FitnessPoints'

# stores data of user's daily nike run challenge upload
class runImage(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='run_images')
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.image.name

# stores data of user's trivia of the day attempt
class quizUser(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField(choices=(
        ("A", "A"), 
        ("B", "B"),
        ("C", "C"),
        ("D", "D"),
        ),
        null=True,
        blank=True,
    )
    correct = models.TextField()
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.user.username) + " " + str(self.date_added)
