from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views import View
import os

from .models import Movie, Category

from .forms import ReviewForm
# Create your views here.


class MoviesView(ListView):
    model = Movie
    queryset = Movie.objects.filter(draft=False)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['categories'] = Category.objects.all()
        return context


class MovieDetailView(DetailView):
    model = Movie
    slug_field = "url"
    template_name = "movies/movie_detail.html"


class AddReview(View):
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                print(request.POST)
                form.parent_id = int(request.POST.get("parent"))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())
