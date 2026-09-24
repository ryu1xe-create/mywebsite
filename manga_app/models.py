from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png', blank=True)
    is_premium = models.BooleanField(default=False)

class Manga(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField()
    cover_image = models.ImageField(upload_to='manga_covers/')
    author = models.CharField(max_length=100)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='mangas')
    created_at = models.DateTimeField(auto_now_add=True)

class Chapter(models.Model):
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE, related_name='chapters')
    chapter_number = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    content_images_folder = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class Anime(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    poster = models.ImageField(upload_to='anime_posters/')
    episodes_count = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class Episode(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='episodes')
    episode_number = models.PositiveIntegerField()
    video_url = models.URLField()
    title = models.CharField(max_length=200, blank=True)

class Review(models.Model):
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

from django.db import models

# Таны одоо байгаа Manga модел...

class Chapter(models.Model):
    manga = models.ForeignKey('Manga', on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=200, verbose_name="Бүлгийн нэр / Дугаар") # Ж: Chapter 1: Romance Dawn
    chapter_number = models.IntegerField(default=1, verbose_name="Ангийн дугаар")
    content = models.TextField(blank=True, null=True, verbose_name="Бичвэр эсвэл Агуулга")
    video_url = models.URLField(blank=True, null=True, verbose_name="Аниме бичлэгийн линк (YouTube/Drive)")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['chapter_number']

    def __str__(self):
        return f"{self.manga.title} - Ch.{self.chapter_number}: {self.title}"