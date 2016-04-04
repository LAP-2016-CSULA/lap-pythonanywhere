from django.contrib import admin
from . import models

# Add models so that they can be used in Djangoadmin
admin.site.register(models.SpeciesType)
admin.site.register(models.Tree)
admin.site.register(models.Question)
admin.site.register(models.DailyUpdate)
admin.site.register(models.Choice)
admin.site.register(models.Bird)
admin.site.register(models.TreeSpecies)