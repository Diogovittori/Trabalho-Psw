from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from Pessoas import views as pessoas_views


urlpatterns = [
    path('', include('Plantas.urls')),
    path('admin/', admin.site.urls),
    path("contas/login/", pessoas_views.login_view, name="login"),
    path("contas/logout/", pessoas_views.logout_view, name="logout"),
    path(
        "contas/cadastro/",
        pessoas_views.usuario_cadastrar,
        name="usuario_cadastrar",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
