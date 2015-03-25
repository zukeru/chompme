from django.conf.urls import patterns, include, url
from django.contrib import admin

from ChompMe.views import *
 
urlpatterns = patterns('',
    url(r'^$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', logout_page),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'), # If user is not login it will redirect to login page
    url(r'^register$', register, name='register'),
    url(r'^home$', home),
    url(r'^home/$', home),
    url(r'^register/success/$', register_success),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^gettoken/$', getToken),
    url(r'^addfriend/$', addFriend),
    url(r'^profilepic/$', upload_profilepic),
    url(r'^updateprofilepic/$', update_profile_pic),
    url(r'^makepost/$', makepost),
    url(r'^getfriends/$', getFriends),
    url(r'^getnot/$', getNot),
    url(r'^deletepost/$', deletePost),
    url(r'^searchfriends/$', searchFriends),
    url(r'^ar/$', ar),
    url(r'^getposts/$', get_posts),
    url(r'^friendcount/$', friendCount),
    url(r'^requestcount/$', requestCount),
    url(r'^editprofile/$', editProfile),
    url(r'^commentpost/$', commentPost),
    url(r'^getcomments/$', getComments),
    url(r'^getrequest/$', getRequest),
    url(r'^addlike/$', addLike),
    url(r'^removelike/$', removeLike),
    url(r'^friendrequest/$', friendRequest),
    url(r'^[A-Za-z0-9_.]+$', friends),
)

