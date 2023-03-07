from django.shortcuts import render ,redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from .models import Event,Participation
from .forms import EventForm ,EventModelForm
from datetime import date
from django.views.generic import ListView ,DetailView ,CreateView ,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from users.models import Person
# Create your views here.
####################################################

# Function Based Views

####################################################
def HomePage(request,id):
    response ='hello from %s'
    return HttpResponse(response % id)
def eventStatic(req):
    list =[
        {
            'title' :'title1',
            'description' :'description 1'
        },
         {
            'title' :'title2',
            'description' :'description 2'
        }
    ]
    return render(req,'events/staticList.html',{'events':list})
@login_required(login_url="login")
def EventList(request):
    list =Event.objects.filter(state=True)
    print(list)
    return render(request,'events/EventList.html',{'events' : list})

@login_required(login_url="login")
def create_event(request):
    form=EventForm()
    if request.method == "POST":
        form=EventForm(request.POST,request.FILES)
        if form.is_valid():
            Event.objects.create(**form.cleaned_data)
            return redirect('event_list_view')
        else :
            print(form.errors)
    return render(request,"events/event_form.html",{'form' :form})
        
@login_required(login_url="login")
def add_event(req):
    if req.method =="GET":
        form =EventModelForm()
        return render(req,"events/event_form.html",{'form' :form})
    if req.method =="POST":
        form= EventModelForm(req.POST,req.FILES)
        if form.is_valid():
            Event= form.save(commit=False)
            Event.save()
            return redirect('event_list_view')
        else :
            return render(req,"events/event_form.html",{'form' :form})
        
        
@login_required(login_url="login")
def participate(req,event_id):
    user=req.user
    event=Event.objects.get(id=event_id)
    if Participation.objects.filter(Person=user,event=event).count() ==0:
        part=Participation.objects.create(Person=user,event=event,date_participation=date.today)
        part.save()
        event.nbe_participant+=1
        event.save()
        return redirect('event_list_view')
    
    #continuer la logique métier
    
def cancel(request, event_id):
    user = request.user
    event = Event.objects.filter(id=event_id).first()
    participant = Participation.objects.filter(Person=user, event=event).first()
    participant.delete()
    event.nbe_participant -= 1
    event.save()
    return redirect('event_list_view')


####################################################

# Class Based Views

####################################################
class EventListClass(LoginRequiredMixin,ListView):
    login_url="/users/login"
    model=Event
    template_name ='events/EventListView.html'
    context_object_name ='events'
    # queryset = Event.objects.filter(state=True)
    def get_queryset(self):
        return Event.objects.filter(state=True)
    

class EventDetail(LoginRequiredMixin,DetailView):
    login_url="/users/login"
    model=Event
    template_name ='events/EventDetails.html'
    context_object_name ='event'
    
    
class CreateEvent(LoginRequiredMixin,CreateView):
    login_url="/users/login"
    model =Event
    template_name="events/event_form.html"
    form_class =EventModelForm
    success_url = reverse_lazy('event_list_view')
    def form_valid(self, form) -> HttpResponse:
        form.instance.organizer = Person.objects.get(cin=self.request.user.cin)
        return super().form_valid(form)
    
class UpdateEvent(LoginRequiredMixin,UpdateView):
    login_url="/users/login"
    model=Event
    template_name ="events/event_form.html"
    form_class =EventModelForm
    success_url = reverse_lazy('event_list_view')
    
class EventDeleteView(LoginRequiredMixin,DeleteView):
    login_url="/users/login"
    model = Event
    success_url = reverse_lazy('event_list_view')
    