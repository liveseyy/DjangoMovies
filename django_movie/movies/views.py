from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.views import View

from .models import Movie, Actor, Genre, Rating

from .forms import ReviewForm, RatingForm


class GenreYear:
    """Жанры и года выхода фильмов"""
    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values_list("year", flat=True).distinct()


class MoviesView(GenreYear, ListView):
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    paginate_by = 4


class MovieDetailView(GenreYear, DetailView):
    """Полное описание фильма"""
    model = Movie
    slug_field = "url"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["star_form"] = RatingForm()
        return context


class AddReview(View):
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())


class ActorView(GenreYear, DetailView):
    model = Actor
    template_name = 'movies/actor.html'
    slug_field = 'name'


class FilterMoviesView(GenreYear, ListView):
    """Фильтр фильмов"""
    paginate_by = 4

    def get_queryset(self):
        if self.request.GET.getlist("genre") and not self.request.GET.getlist("year"):
            queryset = Movie.objects.filter(genres__in=self.request.GET.getlist("genre")).distinct()
            return queryset

        elif self.request.GET.getlist("year") and not self.request.GET.getlist("genre"):
            queryset = Movie.objects.filter(year__in=self.request.GET.getlist("year")).distinct()
            return queryset

        elif self.request.GET.getlist("year") and self.request.GET.getlist("genre"):
            queryset = Movie.objects.filter(
                                            year__in=self.request.GET.getlist("year"),
                                            genres__in=self.request.GET.getlist("genre")
                                            ).distinct()
            return queryset

        queryset = Movie.objects.all()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["year"] = ''.join([f"year={x}&" for x in self.request.GET.getlist("year")])
        context["genre"] = ''.join([f"genre={x}&" for x in self.request.GET.getlist("genre")])
        return context


class AddStarRating(View):
    """Добавление рейтинга к фильму"""
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
            print(x_forwarded_for)
        else:
            ip = request.META.get('REMOTE_ADDR')
            print(request.META.get('REMOTE_ADDR'))
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get("movie")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)
