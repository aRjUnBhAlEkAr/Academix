'''
*** This File contains all the url patterns for the authentication, administrator, students, teachers and academics.
'''

from django.urls import path, include;

urlpatterns = [
    # authentication
    path('auth/', include('apps.authentication.urls')),
    
    # administration
    path('admin/', include('apps.administration.urls')),
]