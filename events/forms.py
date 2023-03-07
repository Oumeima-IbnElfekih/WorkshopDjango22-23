from django import forms
from .models import Event
from users.models import Person
class EventForm(forms.Form):
    title=forms.CharField(label='Title',max_length=9,
        widget=forms.TextInput(attrs={
            'class' :'form-control'
        }     ))                                          
    description=forms.CharField(label='Event Description',
                                widget=forms.Textarea(attrs={
                                    'class': 'form-control'
                                }))
    image=forms.ImageField(label='Event Image')
    category=forms.ChoiceField(choices=Event.CHOIX, 
                               widget=forms.RadioSelect(
                                   
                               ))
    nbe_participant=forms.IntegerField(min_value=0,step_size=1)
    evt_date=forms.DateField(
        label="Event Date",
        widget=forms.DateInput(
            attrs={
                'type' : 'date',
                'class' :'form-control date-input'
            }
        ))
    organizer=forms.ModelChoiceField(label="Event Organizer",
                                     queryset=Person.objects.all())
    
    
class EventModelForm(forms.ModelForm):
    class Meta:
        model =Event
        # fields ='__all__'
        fields =['title', 'description',
                 'category',
                 'evt_date','nbe_participant',
                 'image']
        exclude=['state']
    evt_date=forms.DateField(
        label="Event Date",
        widget=forms.DateInput(
            attrs={
                'type' : 'date',
                'class' :'form-control date-input'
            }
        ))
    # organizer=forms.ModelChoiceField(label="Event Organizer",
    #                                  queryset=Person.objects.all())