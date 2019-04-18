from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from core.views import profile_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('account/profile/', profile_view, name='profile'),
    path('cart/', include('shopping_cart.urls', namespace='cart')),
    path('', include('books.urls', namespace='books'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
