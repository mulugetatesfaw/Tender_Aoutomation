"""Tender_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from E_Tender.views import UserRegistrationView,AuthenticationView


from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



# Define the URL patterns for the views
from django.urls import path, include
from django.views.generic import RedirectView


urlpatterns = [
    path('', RedirectView.as_view(url='/admin/')),

    path('admin/', admin.site.urls),
    path('api/register/', UserRegistrationView.as_view(), name='user-registration'),
    path('api/auth/', include('rest_framework.urls')),
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('api/auth/user/', AuthenticationView.as_view(), name='user-authentication'),

    path('api/', include('E_Tender.urls')),
    
]
urlpatterns.extend(static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))