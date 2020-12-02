from django.urls import path

from . import views

urlpatterns = [
    path("", views.MoviesView.as_view(), name="movie_list_url"),
    path("filter/", views.FilterMoviesView.as_view(), name="filter_url"),
    path("add-rating/", views.AddStarRating.as_view(), name="add_rating_url"),
    path("<slug:slug>/", views.MovieDetailView.as_view(), name='movie_detail_url'),
    path("review/<int:pk>/", views.AddReview.as_view(), name="add_review_url"),
    path("actor/<str:slug>/", views.ActorView.as_view(), name="actor_detail_url"),
]
