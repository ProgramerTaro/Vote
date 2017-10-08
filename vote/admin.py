from django.contrib import admin
from .models import voteType, Room, voter, elect, gradeFive

admin.site.register(voteType)
admin.site.register(Room)
admin.site.register(voter)
admin.site.register(elect)
admin.site.register(gradeFive)
