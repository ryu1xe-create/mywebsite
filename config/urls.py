from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from manga_app.views import MangaListView, MangaDetailView, MangaCreateView, AnimeListView, AnimeDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MangaListView.as_view(), name='manga_list'),
    path('manga/<int:pk>/', MangaDetailView.as_view(), name='manga_detail'),
    path('manga/new/', MangaCreateView.as_view(), name='manga_create'),
    path('anime/', AnimeListView.as_view(), name='anime_list'),
    path('anime/<int:pk>/', AnimeDetailView.as_view(), name='anime_detail'),
]

# Зураг (Media files) зөв харагдах тохиргоо
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)