from django.urls import path
from .views import *
urlpatterns = [
    path('homepage/<int:id>' ,HomePage , name='HomePage'),
    path('liststatic/' ,eventStatic , name='event_static'),
    path('list/' ,EventList , name='event_list'),
    path('create_event/',create_event,name="create_event"),
    path('add_event/',add_event,name="add_event"),
    path('participate/<int:event_id>',participate,name="participate"),
    path('listeventsView/' ,
         EventListClass.as_view() ,
         name='event_list_view'),
    path('detailsEvent/<int:pk>' ,
         EventDetail.as_view() ,
         name='event_details_view'),
    path('deleteView/<int:pk>', EventDeleteView.as_view(),
         name="Events_Delete_View"),
    path('create_event_view',CreateEvent.as_view(),name="create_event_view"),
    path('update_event_view/<int:pk>',UpdateEvent.as_view(),name="update_event_view")
]
