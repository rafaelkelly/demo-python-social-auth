from django.contrib import admin
from models import Evento, Asistente_Evento

class AsistenteInLine(admin.TabularInline):
    model = Asistente_Evento;
    extra = 1;
    
class EventoAdmin(admin.ModelAdmin):
    inlines = [AsistenteInLine]

admin.site.register(Evento, EventoAdmin)
