from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Manga, Anime

class MangaListView(ListView):
    model = Manga
    template_name = 'manga/manga_list.html'
    context_object_name = 'mangas'

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

from django.shortcuts import render, get_object_or_404
from .models import Manga

def manga_detail(request, pk):
    manga = get_object_or_404(Manga, pk=pk)
    # manga.chapters.all() ашиглан холбоотой бүх ангиудыг авна
    chapters = manga.chapters.all()
    return render(request, 'manga/manga_detail.html', {
        'manga': manga,
        'chapters': chapters
    })