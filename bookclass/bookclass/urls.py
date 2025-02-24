from django.contrib import admin
from django.urls import include, path
from classes.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('classes.urls')),  # Makes endpoints like /api/book/ accessible
    path('', index, name='index'),
]
