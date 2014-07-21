# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.template import defaultfilters as df

class Evento(models.Model):
    nombre = models.CharField(max_length=50)
    asistentes = models.ManyToManyField(User, through='Asistente_Evento')
    lugar = models.CharField(max_length=50)
    fecha = models.DateTimeField()
    duracion_horas = models.IntegerField('horas aproximadas de duración')
    max_asistentes = models.IntegerField('número máximo de asistentes')
    
    def __unicode__(self):
        return unicode(self.nombre) + ' | ' + df.date(self.fecha, "F d, Y")

class Asistente_Evento(models.Model):
    evento = models.ForeignKey(Evento)
    asistente = models.ForeignKey(User)
    
    class Meta:
        unique_together = ('evento', 'asistente')
        verbose_name = 'asistente'
        
    def __unicode__(self):
        return unicode(self.evento) + ' | ' + unicode(self.asistente)