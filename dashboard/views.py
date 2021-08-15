from django.shortcuts import render, redirect
from .models import Movie, Ticket, Slot
# Create your views here.
def dashboard(request):
    if request.user.is_authenticated:
        movies = Movie.objects.all()
        return render(request, 'dashboard/dashboard.html', {'movies': movies})
    return redirect('login')

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
            slot = Slot.objects.create(movie=Movie.objects.get(id=movie_id), date=date, starttime=start_time, endtime=end_time)
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
        tickets = Ticket.objects.filter(user=request.user)
        print(tickets)
        return render(request, 'dashboard/ticket.html', {'tickets': tickets})