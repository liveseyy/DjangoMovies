from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views import View
import os

from .models import Movie

# Create your views here.


class MoviesView(ListView):
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    template_name = "movies/movie_list.html"


class MovieDetailView(DetailView):
    model = Movie
    slug_field = "url"
    template_name = "movies/movie_detail.html"
