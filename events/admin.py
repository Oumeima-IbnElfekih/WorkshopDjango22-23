from django.contrib import admin ,messages
from .models import Event ,Participation
from datetime import datetime

# Register your models here.

class ParticipationInline(admin.StackedInline):
    model =Participation
    extra=1
    readonly_fields=('date_participation',)
    can_delete=True


class ParticipantFilter(admin.SimpleListFilter):
    title='NBR Participant'
    parameter_name ='nbe_participant'
    def lookups(self,request,model_admin):
        return (('0',("No Participants")),('more',("More participants")))
    def queryset(self,request,queryset):
        if self.value() =='0':
            return queryset.filter(nbe_participant__exact=0)
        if self.value() =='more':
            return queryset.filter(nbe_participant__gt=0)
class DateFilter(admin.SimpleListFilter):
    title ='Event Date'
    parameter_name ='evt_date'
    def lookups(self,request,model_admin):
        return (('Past events',("Past events")),
                ('Upcomming Event',("Upcomming Event")),
                ('Today Event',("Today Event")))
    def queryset(self, request,queryset):
        if self.value() =='Past events':
            return queryset.filter(evt_date__lt=datetime.today())
        if self.value() =='Upcomming Event':
            return queryset.filter(evt_date__gt=datetime.today())
        if self.value() =='Today Event':
            return queryset.filter(evt_date__exact=datetime.today())

def accept_events(model_admin,request,queryset):
        rows_updated=queryset.update(state=True)
        if rows_updated ==1:
            msg="1 event"
        else:
            msg=f"{rows_updated} events"
        messages.success(request,message= "%s successfully accepted " %msg)
accept_events.short_description='Accept'
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    def set_to_Refuse(self, request, queryset):
        rows_NoValid = queryset.filter(state=False)
        if rows_NoValid.count() > 0:
            messages.error(
                request, f"{rows_NoValid.count()} events are already marked as Not Accepted")
        else:
            rows_updated = queryset.update(state=False)
            if rows_updated == 1:
                message = "1 event was"
            else:
                message = f"{rows_updated} events were"
            self.message_user(request, level='success',
                              message="%s successfully marked as Not Accepted" % message)

    set_to_Refuse.short_description = "Refuse"
    def event_participants(self,obj):
        count =obj.participations.count()
        return count
    actions=[accept_events,'set_to_Refuse']
    list_display=('title','category','state','event_participants','evt_date')
    list_filter=('state','category',ParticipantFilter,DateFilter)
    list_per_page =5
    ordering =('-title','category')
    search_fields=('title','category')
    readonly_fields=('created_at','updated_at')
    autocomplete_fields=('organizer',)
    fieldsets=(('State', { 'fields': ('state',)}),
                ('Event', { 
                           
                           'classes' :('collapse',),
                           'fields': ('title', 'description','category' ,'nbe_participant' ,'image',
                                       'organizer')}),
                     ('Dates', { 'fields': ('evt_date','created_at','updated_at')})
               )
    inlines=[ParticipationInline]
class ParticipationsAdmin(admin.ModelAdmin):
    pass

admin.site.register(Participation,ParticipationsAdmin)