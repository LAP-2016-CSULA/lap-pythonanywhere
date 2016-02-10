from django.contrib import admin
from . import models

admin.site.register(models.SpeciesType)
admin.site.register(models.Species)
admin.site.register(models.SpecificSpecies)
admin.site.register(models.Question)
admin.site.register(models.Checklist)
admin.site.register(models.DailyUpdate)
admin.site.register(models.Choice)