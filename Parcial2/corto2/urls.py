
from django.contrib import admin
from django.urls import path, include
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views import (
    login_view,
    logout_view,
    home_view,
    find_user_view
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('classify/', find_user_view, name='classify'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)