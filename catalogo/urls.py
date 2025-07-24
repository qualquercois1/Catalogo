from django.contrib import admin
from django.urls import path, include  
from catalog import views as catalog_views

urlpatterns = [
    path('', catalog_views.home_view, name='home'),

    path('admin/', admin.site.urls),

    path('app/', include('catalog.urls')),

]