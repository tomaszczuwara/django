from django.urls import path
from movies.views import ActorsView, MoviesTemplateView, OscarsListView
from movies.views import countries, index

urlpatterns = [
    path('actors/', ActorsView.as_view(), name='actor'),
    path('countries/', countries, name='country'),
    path('movies', MoviesTemplateView.as_view(), name='movie'),
    path('oscars', OscarsListView.as_view(), name='oscar'),
    path('', index)
]