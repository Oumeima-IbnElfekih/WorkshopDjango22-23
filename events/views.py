from django.shortcuts import render ,redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from .models import Event
from .forms import EventForm ,EventModelForm
from django.views.generic import ListView ,DetailView ,CreateView ,UpdateView
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

def EventList(request):
    list =Event.objects.filter(state=True)
    print(list)
    return render(request,'events/EventList.html',{'events' : list})

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
        
        






####################################################

# Class Based Views

####################################################
class EventListClass(ListView):
    model=Event
    template_name ='events/EventListView.html'
    context_object_name ='events'
    # queryset = Event.objects.filter(state=True)
    def get_queryset(self):
        return Event.objects.filter(state=True)
    

class EventDetail(DetailView):
    model=Event
    template_name ='events/EventDetails.html'
    context_object_name ='event'
    
    
class CreateEvent(CreateView):
    model =Event
    template_name="events/event_form.html"
    form_class =EventModelForm
    success_url = reverse_lazy('event_list_view')
    
class UpdateEvent(UpdateView):
    model=Event
    template_name ="events/event_form.html"
    form_class =EventModelForm
    success_url = reverse_lazy('event_list_view')
    