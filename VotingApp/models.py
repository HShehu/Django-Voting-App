from django.db import models
from django.conf import settings
from django.utils import timezone
# Create your models here.


class Poll(models.Model):
    poll_text = models.CharField(max_length=200)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()

    @property
    def is_past_due(self):
        return timezone.now() > self.end_date

    def __str__(self):
        return self.poll_text


class Contestant(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)


    def __str__(self):
        return self.user.full_name + ": "+ self.user.student_number



class Choice(models.Model):
    contestant = models.ForeignKey(Contestant, on_delete=models.CASCADE, limit_choices_to={"approved": True})
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    votes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.contestant.user.full_name + ": " + self.poll.poll_text



class Voter(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
