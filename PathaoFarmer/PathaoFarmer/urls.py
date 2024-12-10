from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('auth_app.urls')),
    path('api/farmers/', include('farmers.urls')),
    path('api/farms/', include('farms.urls')),
    path('api/livestock/', include('livestock.urls')),
    path('api/transactions/', include('transactions.urls')),
]
