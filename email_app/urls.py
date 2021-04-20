from django.urls import path
from . import views

#each path is bound to a specific view in the views file
urlpatterns = [
    path('',                    views.index,         name="index"),
    path('signin/',             views.signin,        name="signin"),
    path('inbox/',              views.inbox,         name="inbox"),
    path('<id>/message_view/',  views.message_view,  name="message_view"),
    path('<id>/message_view2/', views.message_view2, name="message_view2"),
    path('sent/',               views.sent,          name="sent"),
    path('compose/',            views.compose,       name="compose"),
    path('logout/',             views.logout,        name="logout"),

]