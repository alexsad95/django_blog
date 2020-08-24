from django.contrib import admin
from django.urls import path
from django.urls import include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from .views import redirect_blog


urlpatterns = [
    path('', redirect_blog),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)