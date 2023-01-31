from django.db import models
from datetime import date
from django.core.exceptions import ValidationError

from users.models import Person
# Create your models here.


def is_date_event(value):
    if value <= date.today():
        raise ValidationError('Event date is incorrect!!!')
    return value


class Event(models.Model):
    CATEGORY_CHOICES = (
        ('Music', 'Music'),
        ('Cinema', 'Cinema'),
        ('Sport', 'Sport'),
    )

    title = models.CharField(max_length=255, null=True)
    description = models.TextField()
    eventImage = models.ImageField(upload_to='images/', blank=True)

    category = models.CharField(choices=CATEGORY_CHOICES, max_length=8)
    state = models.BooleanField(default=False)
    nbrParticipants = models.IntegerField(default=0)
    eventDate = models.DateField(validators=[is_date_event])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    organizer = models.ForeignKey(
        Person,
        on_delete=models.CASCADE
    )

    subscription = models.ManyToManyField(
        Person,
        related_name='participations',
        through='Participation'
    )

    


class Participation(models.Model):
    person = models.ForeignKey(
        Person, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    participationDate = models.DateField(auto_now=True)

 
