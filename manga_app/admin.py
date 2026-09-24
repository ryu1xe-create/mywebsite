from django.contrib import admin
from .models import Manga, Chapter

class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 1

@admin.register(Manga)
class MangaAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    inlines = [ChapterInline]  # Манга засах үед дотор нь шууд Chapter нэмэх хэсэг гарч ирнэ

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('manga', 'chapter_number', 'title', 'created_at')
    list_filter = ('manga',)