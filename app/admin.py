from django.contrib import admin
from . import models

admin.site.register(models.SpeciesType)
#admin.site.register(models.Species)
admin.site.register(models.Tree)
admin.site.register(models.Question)
admin.site.register(models.DailyUpdate)
admin.site.register(models.Choice)
admin.site.register(models.Bird)
admin.site.register(models.BirdObservation)
admin.site.register(models.TreeSpecies)
admin.site.register(models.BirdChoice)
admin.site.register(models.TreeChoice)