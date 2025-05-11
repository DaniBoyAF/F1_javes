from django.contrib import admin
from .models import Telemetria, SessionData, CarStatus ,LapData, Penaty,Usuario,Amizade
# botar as views aqui
#depois ligar nas tem templates

admin.site.register(Telemetria)
admin.site.register(SessionData)
admin.site.register(CarStatus)
admin.site.register(LapData)
admin.site.register(Penaty)
admin.site.register(Usuario)
admin.site.register(Amizade)    

