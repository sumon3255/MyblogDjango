"""icoder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from django.contrib.auth import views as auth_views
from blog import views
from icoder import settings
from django.conf.urls.static import static

admin.site.site_header = "Icoder Admin"
admin.site.site_title = "Icoder Admin Panel"
admin.site.index_title = "Welcome to iCoder Admin Panel"


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),#home ere url e chole jabe
    path('blog/', include('blog.urls')),#blog ere url e chole jabe
    path('likes',views.likes_post,name="likes_post"),
    path('edit_profile',views.edit_profile,name="edit_profile"),

    path('^', include('django.contrib.auth.urls')),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)