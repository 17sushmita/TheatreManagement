from django.shortcuts import render, redirect
from .models import Movie, Ticket, Slot
from users.models import User
from django.db import IntegrityError
from django.contrib import messages

# Create your views here.
def dashboard(request):
    if request.method == "POST" and request.POST['type'] == 'search':
        search_term = request.POST['search']
        movies = Movie.objects.filter(name__icontains=search_term)
        return render(request, 'dashboard/dashboard.html', {'movies': movies})
    movies = Movie.objects.all()
    return render(request, 'dashboard/dashboard.html', {'movies': movies})

def add_movie(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            title = request.POST['title']
            description = request.POST['description']
            release_date = request.POST['release_date']
            director = request.POST['director']
            movie = Movie.objects.create(name=title, description=description, release_date=release_date, director=director)
            return redirect('dashboard')
        return render(request, 'dashboard/add_movie.html')
    if request.method == 'POST':
        movies = Movie.objects.all()
        return redirect('dashboard', {'movies': movies})

def movie(request, id):
    slots = Slot.objects.filter(movie_id=id)
    movie_id = id
    movie = Movie.objects.get(id=movie_id)
    if request.method == 'POST':
        if request.POST['type'] == 'slot' and request.user.is_authenticated and request.user.is_staff:
            movie_id = id
            date = request.POST['date']
            start_time = request.POST['start_time']
            end_time = request.POST['end_time']
            try:
                slot = Slot.objects.create(movie=Movie.objects.get(id=movie_id), date=date, starttime=start_time, endtime=end_time)
            except IntegrityError as e:
                messages.error(request, 'Add a different time slot. This slot is already filled')

            return redirect('dashboard')
        elif request.POST['type'] == 'ticket' and request.user.is_authenticated:
            movie_id = id
            movie = Movie.objects.get(id=movie_id)
            if request.method == 'POST':
                slot = request.POST['slot']
                number_of_tickets = request.POST['number_of_tickets']
                ticket = Ticket.objects.create(slot=Slot.objects.get(id=slot), user=request.user, quantity=number_of_tickets)
                return redirect('ticket')
        slots = Slot.objects.filter(movie_id=movie_id)

    return render(request, 'dashboard/movie.html', {'slots': slots, 'movie': movie})

def ticket(request):
    if request.user.is_authenticated:
        tickets = Ticket.objects.filter(user=User.objects.get(email=request.user))
        return render(request, 'dashboard/ticket.html', {'tickets': tickets})