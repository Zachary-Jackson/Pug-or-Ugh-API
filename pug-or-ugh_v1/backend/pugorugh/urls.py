from django.conf.urls import url
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token

from pugorugh.views import (
    RetrieveDogView, RetrieveUpdateUserPrefView, UserRegisterView,
    UpdateUserDogView)

# API endpoints
urlpatterns = format_suffix_patterns([
    url(r'^api/user/login/$', obtain_auth_token, name='login-user'),
    url(r'^api/user/$', UserRegisterView.as_view(), name='register-user'),
    url(r'^favicon\.ico$',
        RedirectView.as_view(
            url='/static/icons/favicon.ico',
            permanent=True
        )),
    url(r'^$', TemplateView.as_view(template_name='index.html')),

    url(r'^api/user/preferences/$',
        RetrieveUpdateUserPrefView.as_view(),
        name='user_pref_detail'),

    url(r'^api/dog/(?P<dog_pk>(-)?\d+)/(?P<status_pk>\w+)/next/',
        RetrieveDogView.as_view(),
        name='dog_detail'
        ),

    url(r'^api/dog/(?P<dog_pk>(-)?\d+)/(?P<status_pk>\w+)/',
        UpdateUserDogView.as_view(),
        name='UserDog_update'
        )
])
