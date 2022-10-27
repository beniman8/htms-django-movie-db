from django.http.response import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic import FormView, TemplateView
from django.contrib.auth import get_user_model
from .models import Film,UserFilms
from django.views.generic.list import ListView
from django.shortcuts import render,get_object_or_404


from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_http_methods
from django.contrib import messages

from films.forms import RegisterForm
from films.utils import get_max_order , reorder


class IndexView(TemplateView):
    template_name = 'index.html'
    
class Login(LoginView):
    template_name = 'registration/login.html'

class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()  # save the user
        return super().form_valid(form)

class FilmListView(LoginRequiredMixin,ListView):
    model = UserFilms
    template_name = "films.html"
    context_object_name ='films'
    paginate_by = 20


    def get_template_names(self):

        if self.request.htmx:
            return "partials/film-list-elements.html"
        else:
            return "films.html"


    #filter to get the users film only and not all the available films
    def get_queryset(self):
        # user = self.request.user
        # return user.films.all()

        return UserFilms.objects.filter(user=self.request.user)
    




def check_username(request):
    username = request.POST.get('username')
    if get_user_model().objects.filter(username=username).exists():
        return HttpResponse("<div id='username-error' class='error'>This username already exists</div>")
    else:
        return HttpResponse("<div id='username-error' class='success'>This username is available</div>")

@login_required
def add_film(request):
    name = request.POST.get('filmname')

    film = Film.objects.get_or_create(name=name)[0]

    # add film to user's 
    # request.user.films.add(film)
    if not UserFilms.objects.filter(film=film,user = request.user).exists():

        UserFilms.objects.create(film=film,user = request.user,order=get_max_order(request.user))

    #return template with all of the users films
    films = UserFilms.objects.filter(user=request.user)
    messages.success(request,f"Added {name} to list of films")
    return render(request,'partials/film-list.html',{'films':films})


@login_required
@require_http_methods('DELETE')
def delete_film(request,pk):

    #remove the film from user's list
    # request.user.films.remove(pk)
    UserFilms.objects.get(pk=pk).delete()
    reorder(request.user)
    #retuern templat fragment
    # films = request.user.films.all()
    films =UserFilms.objects.filter(user = request.user)
    return render(request,'partials/film-list.html',{'films':films})


def search_film(request):
    search_text = request.POST.get('search')

    userfilms= UserFilms.objects.filter(user = request.user)
    results = Film.objects.filter(name__icontains=search_text).exclude(
        name__in=userfilms.values_list('film__name',flat=True)
    )

    return render(request,'partials/search-results.html',{'results':results})



def clear(request):
    return HttpResponse("")



def sort(request):
    film_pks_order = request.POST.getlist('film_order')
    films = []
    for idx,film_pk in enumerate(film_pks_order,start=1):
        userfilm = UserFilms.objects.get(pk=film_pk)
        userfilm.order = idx
        userfilm.save()
        films.append(userfilm)

    return render(request,'partials/film-list.html',{'films':films})

@login_required
def detail(request,pk):
    userfilm = get_object_or_404(UserFilms,pk=pk)
    context  = {'userfilm':userfilm}

    return render(request,'partials/film-detail.html',context)


def films_partials(request):

    films= UserFilms.objects.filter(user = request.user)
    
    return render(request,'partials/film-list.html',{'films':films})


@login_required
def upload_photo(request,pk):
    userfilm = get_object_or_404(UserFilms,pk=pk)
    photo = request.FILES.get('photo')

    userfilm.film.photo.save(photo.name,photo)

    context  = {'userfilm':userfilm}
    
    return render(request,'partials/film-detail.html',context)