
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gymapp.urls')),
    path("api/", include("apis.urls")), 
    path('api-auth/', include('rest_framework.urls')),
    path('accounts/', include('allauth.urls')),
    path("api/dj-rest-auth/", include("dj_rest_auth.urls")),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
