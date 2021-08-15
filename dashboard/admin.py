from django.contrib import admin
from .models import Movie, Slot, Ticket

admin.site.register(Movie)
admin.site.register(Slot)
admin.site.register(Ticket)
