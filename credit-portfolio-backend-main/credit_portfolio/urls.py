from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView


urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html"), name="app"),
    path("admin/", admin.site.urls),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/credit/', include('credit.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
]

urlpatterns += [
    re_path('^.*$', TemplateView.as_view(template_name="index.html")),
]
