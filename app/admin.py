from django.contrib import admin
from . import models
from import_export import resources, fields
from import_export.admin import ExportMixin


#Create a model resource class in order to export Daily Update information
class DailyUpdateResource(resources.ModelResource):
    #Format -> ObservationID, Date, SpeciesID, geo-location, checklist values, bird checklist values
    #choices = fields.Field()
    #birds = fields.Field()

    class Meta:
        model = models.DailyUpdate
        widgets = {
                    'date_of_observation': {'format': '%Y.%m.%d'},
                }
        fields = ('id', 'date_of_observation', 'tree__id', 'tree__species__name', 'tree__lat', 'tree__long', 'choices', 'birds',)
        exclude = ('changed_by', 'image',)
        export_order = ('id', 'date_of_observation', 'tree__id', 'tree__species__name', 'tree__lat', 'tree__long', 'choices', 'birds',)

    def dehydrate_choices(self, update):
        return update.choices.all()

    def dehydrate_birds(self, update):
        return update.birds.all()

class DailyUpdateAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = DailyUpdateResource


# Add models so that they can be used in Djangoadmin
admin.site.register(models.SpeciesType)
admin.site.register(models.Tree)
admin.site.register(models.Question)
admin.site.register(models.DailyUpdate, DailyUpdateAdmin)
admin.site.register(models.Choice)
admin.site.register(models.Bird)
admin.site.register(models.TreeSpecies)
admin.site.register(models.Season)
admin.site.register(models.Semester)
admin.site.register(models.SemesterClass)
admin.site.register(models.UserProfile)