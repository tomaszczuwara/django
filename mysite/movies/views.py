from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, ListView
from movies.models import Actor, Country, Movie, Oscar
from django.shortcuts import render

def countries(request):
        return render(
            request,
            template_name='countries.html',
            context={'countries': Country.objects.all()}
    )

class ActorsView(View):
   def get(self, request):
       return render(
           request, template_name="actors.html",
           context={'actors': Actor.objects.all()}
       )

def actors(request):
    return render(
        request,
        template_name='actors.html',
        context={'answers': Actor.objects.all()}
    )

class MoviesTemplateView(TemplateView):
    template_name = "movies.html"
    extra_context = {'movies': Movie.objects.all()}

class OscarsListView(ListView):
    template_name = "oscars.html"
    model = Oscar

def index(request):
    return render(
        request,
        template_name="index_movies.html"
    )
