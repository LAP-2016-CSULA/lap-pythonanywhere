from django.contrib import admin
from django.http import HttpRequest
import csv
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from . import models

#Copied from http://stackoverflow.com/questions/18685223/how-to-export-django-model-data-into-csv-file
#Clients want the information in this format:
#ObservationID, Date, [tree] SpeciesID, geo-location, [tree] checklist values, bird checklist values
def download_csv(modeladmin, request, queryset):
        """
        Downloads model information into a csv file
        """
        if not request.user.is_staff:
            raise PermissionDenied
        opts = queryset.model._meta
        model = queryset.model
        response = HttpResponse(content_type='text/csv')
        # force download.
        response['Content-Disposition'] = 'attachment;filename=LAP.csv'
        # the csv writer
        writer = csv.writer(response)
        field_names = [field.name for field in opts.fields]
        # Write a first row with header information
        writer.writerow(field_names)
        # Write data rows
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])
        return response
download_csv.short_description = "Download selected as csv"

class BirdObservationAdmin(admin.ModelAdmin):
    """
    Admin for the csv data of the bird observation
    """
    pass

class TreeObservationAdmin(admin.ModelAdmin):
    """
    Admin for the csv data of the tree observation
    """
    list_display = ['id', 'species', 'lat', 'long', 'date_modified']
    ordering = ['id']
    actions = [download_csv]

admin.site.register(models.SpeciesType)
#admin.site.register(models.Species)
admin.site.register(models.Tree, TreeObservationAdmin)
admin.site.register(models.Question)
admin.site.register(models.DailyUpdate)
admin.site.register(models.Choice)
admin.site.register(models.Bird)
admin.site.register(models.BirdObservation)
admin.site.register(models.TreeSpecies)
admin.site.register(models.BirdChoice)
admin.site.register(models.TreeChoice)


