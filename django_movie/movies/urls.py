from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.MoviesView.as_view(), name="movie_list_url"),
    path("<slug:slug>/", views.MovieDetailView.as_view(), name='movie_detail_url'),
    path("review/<int:pk>/", views.AddReview.as_view(), name="add_review_url"),
    path("actor/<str:slug>/", views.ActorView.as_view(), name="actor_detail_url")
]
