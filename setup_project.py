import os

# Үүсгэх файлууд ба тэдгээрийн кодууд
files = {
    "manga_app/models.py": '''from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True, verbose_name="Товч танилцуулга")
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png', blank=True)
    is_premium = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Manga(models.Model):
    title = models.CharField(max_length=200, verbose_name="Манганы нэр")
    summary = models.TextField(verbose_name="Товч утга")
    cover_image = models.ImageField(upload_to='manga_covers/')
    author = models.CharField(max_length=100)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='mangas')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Chapter(models.Model):
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE, related_name='chapters')
    chapter_number = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    content_images_folder = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['chapter_number']

    def __str__(self):
        return f"{self.manga.title} - Chapter {self.chapter_number}"

class Anime(models.Model):
    title = models.CharField(max_length=200, verbose_name="Аниме нэр")
    description = models.TextField()
    poster = models.ImageField(upload_to='anime_posters/')
    episodes_count = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Episode(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='episodes')
    episode_number = models.PositiveIntegerField()
    video_url = models.URLField(help_text="YouTube/Embed видео линк")
    title = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.anime.title} - Ep {self.episode_number}"

class Review(models.Model):
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
''',

    "manga_app/admin.py": '''from django.contrib import admin
from .models import CustomUser, Manga, Chapter, Anime, Episode, Review

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_premium')
    list_filter = ('is_staff', 'is_superuser', 'is_premium')
    search_fields = ('username', 'email')

@admin.register(Manga)
class MangaAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_by', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('title', 'summary')
    ordering = ('-created_at',)
    fieldsets = (
        ('Үндсэн мэдээлэл', {'fields': ('title', 'author', 'summary', 'cover_image')}),
        ('Үүсгэсэн хэрэглэгч', {'fields': ('created_by',)}),
    )

admin.site.register(Chapter)
admin.site.register(Anime)
admin.site.register(Episode)
admin.site.register(Review)
''',

    "manga_app/views.py": '''from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Manga, Anime

class MangaListView(ListView):
    model = Manga
    template_name = 'manga/manga_list.html'
    context_object_name = 'mangas'
    paginate_by = 12

class MangaDetailView(DetailView):
    model = Manga
    template_name = 'manga/manga_detail.html'

class MangaCreateView(LoginRequiredMixin, CreateView):
    model = Manga
    fields = ['title', 'summary', 'cover_image', 'author']
    template_name = 'manga/manga_form.html'
    success_url = reverse_lazy('manga_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class AnimeListView(ListView):
    model = Anime
    template_name = 'anime/anime_list.html'
    context_object_name = 'animes'

class AnimeDetailView(DetailView):
    model = Anime
    template_name = 'anime/anime_detail.html'
''',

    "templates/base.html": '''<!DOCTYPE html>
<html lang="mn" data-bs-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}AniManga World{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { background-color: #0f172a; color: #e2e8f0; }
        .navbar { background-color: #1e293b !important; }
        .card { background-color: #1e293b; border: 1px solid #334155; }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark mb-4">
        <div class="container">
            <a class="navbar-brand text-danger fw-bold" href="#">AniManga</a>
        </div>
    </nav>
    <div class="container">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
'''
}

# Файлуудыг автомат үүсгэж бичих
for filepath, content in files.items():
    folder = os.path.dirname(filepath)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Амжилттай үүссэн: {filepath}")

print("\n🎉 Бүх кодууд холбогдох файлууддаа шууд хуулагдлаа!")