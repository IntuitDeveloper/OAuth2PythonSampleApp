from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^/?$', views.index, name='index'),
    url(r'^(?i)/connectToQuickbooks/?$', views.connectToQuickbooks, name='connectToQuickbooks'),
    url(r'^(?i)/signInWithIntuit/?$', views.signInWithIntuit, name='signInWithIntuit'),
    url(r'^(?i)/getAppNow/?$', views.getAppNow, name='getAppNow'),
    url(r'^(?i)/authCodeHandler/?$', views.authCodeHandler, name='authCodeHandler'),
    url(r'^(?i)/disconnect/?$', views.disconnect, name='disconnect'),
    url(r'^(?i)/apiCall/?$', views.apiCall, name='apiCall'),
    url(r'^(?i)/connected/?$', views.connected, name='connected'),
    url(r'^(?i)/refreshTokenCall/?$', views.refreshTokenCall, name='refreshTokenCall')
]
