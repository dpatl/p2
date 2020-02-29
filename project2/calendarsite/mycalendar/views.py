from django.shortcuts import render, get_object_or_404
from django.db.models.functions import TruncDay

from django.http import HttpResponse, HttpResponseRedirect
from mycalendar.models import User, Calendar, Event, BelongsTo
from django.urls import reverse
import datetime
from django.utils import timezone


# Create your views here.

def mainindex(request):
       context = { 'user_list': User.objects.all() }
       return render(request, 'mycalendar/index.html', context)

def userindex(request, user_id):
    context = {'calendar_list': User.objects.get(pk=user_id).calendar_set.all()}
    return render(request, 'mycalendar/userindex.html', context)

def eventindex(request, event_id):
       event = Event.objects.get(pk=event_id)
       statuses = [(c.title, BelongsTo.Status(BelongsTo.objects.get(event=event, calendar=c).status)) for c in event.calendars.all()]
       context = {'event': event, 'statuses': statuses}
       return render(request, 'mycalendar/eventindex.html', context)

def calendarindex(request, calendar_id):
   e_days = Calendar.objects.get(pk=calendar_id).event_set.all().annotate(day=TruncDay('start_time')).values('day','title','start_time','end_time','id').order_by('-start_time')
   d = {}
   for e in e_days:
       if str(e['day'].month) + ' ' + str(e['day'].day) in d.keys():
           d[str(e['day'].month) + ' ' + str(e['day'].day)].append(e)
       else:
           d[str(e['day'].month)  + ' ' + str(e['day'].day)] = [e]
   print(d.values())
   context = {'calendar_id': calendar_id,
              'event_list': Calendar.objects.get(pk=calendar_id).event_set.order_by('-start_time'),
              'eventz': d}
   return render(request, 'mycalendar/calendarindex.html', context)

def createevent(request, user_id):
       context = { 'user': User.objects.get(pk=user_id), 'calendar_list': Calendar.objects.all() }
       return render(request, 'mycalendar/createevent.html', context)

def submitcreateevent(request, user_id):
       chosen_calendars = [c for c in Calendar.objects.all() if request.POST["answer{}".format(c.id)] == "true"]
       e = Event(title=request.POST["title"], start_time=request.POST["start_time"], end_time=request.POST["end_time"], created_by = User.objects.get(pk=user_id))
       e.save()
       for c in chosen_calendars:
           bt = BelongsTo(event=e, calendar=c, status=BelongsTo.Status.WAITING_RESPONSE)
           bt.save()
       return HttpResponseRedirect(reverse('createdevent', args=(user_id,e.id,)))

def createdevent(request, user_id, event_id):
   return eventindex(request, event_id)


def modifyevent(request, event_id):
    events = Event.objects.get(pk=event_id)
    calendars = Calendar.objects.all()
    invites = BelongsTo.objects.filter(event=event_id).values_list('calendar','status')
    inv = dict(invites)

    for k,v in inv.items():
        if inv[k] == 'AC':
            inv[k] = 'Accepted'
        elif inv[k] == 'DE':
            inv[k] = 'Declined'
        elif inv[k] == 'TE':
            inv[k] = 'Tentative'
        else:
            inv[k] = 'Waiting Response'
    context = {'e': events,
               'c': calendars,
               'i': inv}

    return render(request, 'mycalendar/modifyevent.html', context)

def modifiedevent(request, event_id):
    return eventindex(request, event_id)

def submitmodifyevent(request, event_id):
    invites = []
    cals = Calendar.objects.all()
    for c in cals:
        if request.POST["answer{}".format(c.id)] == "true":
            invites.append(c)
    event = Event.objects.get(pk=event_id)
    event.title,event.start_time,event.end_time = request.POST["title"], request.POST["start_time"],request.POST["end_time"]
    event.save()
    print(BelongsTo.objects.filter(event=event_id))
    bt = BelongsTo.objects.filter(event=event_id).delete()
    print(BelongsTo.objects.filter(event=event_id))

    for i in invites:
        bt = BelongsTo(event=event, calendar=i, status=BelongsTo.Status.WAITING_RESPONSE)
        bt.save()
    return HttpResponseRedirect(reverse('modifiedevent', args=(event.id,)))


def waiting(request, user_id, calendar_id):
    events = BelongsTo.objects.filter(calendar=calendar_id, status="WR")
    cal = Calendar.objects.get(pk=calendar_id)
    u = User.objects.get(pk=user_id)
    context = {'ev': events,
               'us': u,
               'ca': cal}
    return render(request, 'mycalendar/waiting.html', context)
    
def submitmodifystatus(request, user_id, calendar_id):
    changes = []
    w = BelongsTo.objects.filter(calendar=calendar_id, status="WR")
    print("BEFORE:  " + str(BelongsTo.objects.filter(calendar=calendar_id, status="WR")))
    for e in w:
        id = "answer{}".format(e.event.id)
        if request.POST[id] != "WR":
            changes.append(e)
    for c in changes:
        c.status = request.POST["answer{}".format(c.event.id)]
        c.save()

    return HttpResponseRedirect(reverse('modifiedstatus', args=(user_id, calendar_id,)))

def modifiedstatus(request, user_id, calendar_id):
    return calendarindex(request, calendar_id)


# Here we will compute some statistics about the data in the database
# Specifically: for each calendar, we will compute the number of events in different status, and a total as a 6-tuple
# The tuple fields are: (calendar title, number of waiting response events, number of accepted events, number of declined events, number of tentative events, total)
# ('John\'s Work Calendar, 1, 4, 3, 4, 10)
def summary(request):
   tuples = []

   wait = 0
   accept = 0
   decline = 0
   total = 0
   tent = 0

   cals = Calendar.objects.all()[:5]
   for c in cals:
       bt = BelongsTo.objects.filter(calendar = c)
       for b in bt:
           if b.status == 'AC':
               accept = accept + 1
           elif b.status == 'WR':
               wait = wait + 1
           elif b.status == 'DE':
               decline = decline + 1
           elif b.status == 'TE':
               tent = tent + 1
       tuples.append((c.title,wait,accept,decline,tent,wait+accept+decline+tent))

   summary_tuples = [('Sample Calendar', 1, 4, 3, 4, 10)]
   context = {'summary_tuples': tuples}
   return render(request, 'mycalendar/summary.html', context)

