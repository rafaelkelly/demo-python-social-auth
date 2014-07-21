from django.shortcuts import render
from django.views import generic
from django.utils import timezone
from models import Evento, Asistente_Evento
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.template import defaultfilters as df
import facebook


class HomeView(generic.TemplateView):
    template_name = "eventos/home.html"

class EventosView(generic.ListView):
    template_name = 'eventos/eventos.html'
    context_object_name = 'eventos'

    def get_queryset(self):
        return Evento.objects.order_by('-fecha')

class DetallesView(generic.DetailView):
    model = Evento
    template_name = 'eventos/evento.html'
    
    def get_context_data(self, **kwargs):
        context = super(DetallesView, self).get_context_data(**kwargs)
        context['disponible'] = True
        if self.get_object().asistentes.filter(
            pk=self.request.user.pk) or self.get_object().fecha < timezone.now():
            context['disponible'] = False
        return context

@login_required
def registrar(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    mensaje = "Voy a asistir al evento " + evento.nombre + " cuya fecha es: " + df.date(evento.fecha, "F d, Y")
    user = request.user
    social_user = user.social_auth.first()
    asistente_evento = Asistente_Evento(asistente=user, evento=evento)
    try:
        asistente_evento.save()
        graph = facebook.GraphAPI(social_user.extra_data['access_token'])
        graph.put_object('me', 'feed', message=mensaje, link="http://www.test1.com",
            picture='http://www.thefamilyfocus.ca/images/Inserts/Calendar.png')
    except:
        messages.add_message(request, messages.ERROR, "Se ha producido un error!")
    else:
        messages.add_message(request, messages.INFO,
            "Gracias por registrar tu asistencia. Esta accion ha sido publicada en tu muro de fb.")
        return HttpResponseRedirect(reverse('eventos:evento', args=[evento.pk]))