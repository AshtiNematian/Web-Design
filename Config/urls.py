from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from Config import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('blog/', include('blogs.urls')),
    path('services/', include('services.urls')),

]