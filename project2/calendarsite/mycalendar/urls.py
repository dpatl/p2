from django.conf.urls import url

from . import views
        
urlpatterns = [
        url(r'^$', views.mainindex, name='mainindex'),

        url(r'^user/(?P<user_id>[0-9]+)/$', views.userindex, name='userindex'),

        url(r'^event/(?P<event_id>[0-9]+)/$', views.eventindex, name='eventindex'),

        url(r'^calendar/(?P<calendar_id>[0-9]+)/$', views.calendarindex, name='calendarindex'),

        url(r'^user/(?P<user_id>[0-9]+)/createevent$', views.createevent, name='createevent'),
        url(r'^modifyevent/(?P<event_id>[0-9]+)/$', views.modifyevent, name='modifyevent'),
        url(r'^modifyevent/(?P<event_id>[0-9]+)/submitmodifyevent/$', views.submitmodifyevent, name='submitmodifyevent'),
        url(r'^modifyevent/(?P<event_id>[0-9]+)/modifiedevent/$', views.modifiedevent, name='modifiedevent'),
        url(r'^user/(?P<user_id>[0-9]+)/submitcreateevent/$', views.submitcreateevent, name='submitcreateevent'),
        url(r'^waiting/user/(?P<user_id>[0-9]+)/calendar/(?P<calendar_id>[0-9]+)/submitmodifystatus$',
            views.submitmodifystatus, name='submitmodifystatus'),

        url(r'^waiting/user/(?P<user_id>[0-9]+)/calendar/(?P<calendar_id>[0-9]+)/modifiedstatus$', views.modifiedstatus,
            name='modifiedstatus'),

        url(r'^user/(?P<user_id>[0-9]+)/createdevent/(?P<event_id>[0-9]+)/$', views.createdevent, name='createdevent'),

        url(r'^waiting/user/(?P<user_id>[0-9]+)/calendar/(?P<calendar_id>[0-9]+)/$', views.waiting, name='waiting'),

        url(r'^summary$', views.summary, name='summary')
] 
