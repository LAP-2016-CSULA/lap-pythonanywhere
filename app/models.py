"""
LAP Models.
Each models should have a history field of type HistoricalRecords to store the history.

"""

from django.db import models
from simple_history.models import HistoricalRecords


class SpeciesType(models.Model):
    """ species type. """
    name = models.CharField(max_length=50)
    history = HistoricalRecords()

    def __str__(self):
        """ display name. """
        return self.name


class Species(models.Model):
    """ species model. """
    type = models.ForeignKey(SpeciesType)
    scientific_name = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=2048)
    history = HistoricalRecords()

    def __str__(self):
        """ display name. """
        return self.name


class Question(models.Model):
    """ species' category. """
    text = models.CharField(max_length=50)
    history = HistoricalRecords()

    def __str__(self):
        """ display name. """
        return self.text


class Tree(models.Model):
    """ a tree instance. it contains location (longitude and latitude). """
    species = models.ForeignKey(Species)
    long = models.FloatField()
    lat = models.FloatField()
    changed_by = models.ForeignKey('auth.User')
    history = HistoricalRecords()

    def __str__(self):
        """ display species name and tree id. """
        return self.species.name + ' [' + str(self.id) + ']'

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value


class DailyUpdate(models.Model):
    """ a tree daily update. each instance is bound to a specified tree. """
    tree = models.ForeignKey(Tree)
    # added_by = models.ForeignKey('auth.User', related_name='creator')
    changed_by = models.ForeignKey('auth.User', related_name='modifier')
    image = models.ImageField(max_length=None, null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        """ display string. """
        return 'dailyupdate [' + str(self.id) + '] of ' + str(self.tree)

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value


class Choice(models.Model):
    """ choices. """
    question = models.ForeignKey(Question)
    value = models.BooleanField(default=False)
    daily_update = models.ManyToManyField(DailyUpdate)
    history = HistoricalRecords()

    def __str__(self):
        """ display choice text. """
        return self.text

