from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls

mypatterns = [
    path('admin/', admin.site.urls),
    path('docs/', include_docs_urls(title='Jacob Rest API')),
    path('auth/', include('project.apps.authentication.urls')),
    path('search/', include('project.apps.search.urls')),
    path('file/', include('project.apps.upload.urls')),
    path('tags/', include('project.apps.tags.urls')),
    path('user/', include('project.apps.registrations.urls')),
    path('annotate/', include('project.apps.annotations.urls'))

]

urlpatterns = [
    path('backend/', include(mypatterns)),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
