"""
LAP Models.
Each models should have a history field of type HistoricalRecords to store the history.

"""

"""
Information needed:
    id, date, species, geo-location, checklist, birdlist

@TODO:
1. bird list
2. observation list
3. accept image
4. connect all species to the user who added information about them
"""

from django.db import models
from simple_history.models import HistoricalRecords


class SpeciesType(models.Model):
    """ species type. E.g plant, animal"""
    classification = models.CharField(max_length=50)
    history = HistoricalRecords()

    def __str__(self):
        """ display the category name of the species e.g. bird. """
        return self.classification


class Species(models.Model):
    """ species model. E.g. tree, bird """
    classification = models.ForeignKey(SpeciesType)
    type = models.CharField(max_length=255)
    history = HistoricalRecords()

    def __str__(self):
        """ display name. """
        return self.type

class SpecificSpecies(models.Model):
    """
    A model for a specific species e.g. the california sycamore
    """
    classification = models.ForeignKey(Species)
    common_name = models.CharField(max_length=255)
    scientific_name = models.CharField(max_length=255)
    general_info = models.CharField(max_length=4096)
    history = HistoricalRecords()
    image = models.ImageField(max_length=None, null=True, blank=True)

    def __str__(self):
        """
        display the species' name
        """
        return self.common_name + ", CATEGORY(" + str(self.classification) + ")"

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value

class Location(models.Model):
    """
    Location of each species instance
    """
    species = models.ForeignKey(SpecificSpecies)
    species_latitude = models.FloatField()
    species_longitude = models.FloatField()
    history = HistoricalRecords()

"""
def create_choices_on_question_creation(instance, created, raw, **kwargs):
     Create 2 choices for each question. 
    if created:
        c1 = Choice(question=instance, value=True)
        c2 = Choice(question=instance, value=False)
        c1.save()
        c2.save()

# Auto create 2 choices in the db coresponse to each question on its creation
models.signals.post_save.connect(create_choices_on_question_creation, sender=Question, dispatch_uid='create_choices_on_question_creation')      
""" 
"""
class Tree(models.Model):
     a tree instance. it contains location (longitude and latitude). 
    species = models.ForeignKey(Species)
    long = models.FloatField()
    lat = models.FloatField()
    changed_by = models.ForeignKey('auth.User')
    history = HistoricalRecords()

    def __str__(self):
         display species name and tree id.
        return self.species.name + ' [' + str(self.id) + '] found at lat, ' + str(self.long) + ' long' 

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value


class Bird(models.Model):
    
    A bird instance. It should contain the the tree instance it was interacting with.
    
    species = models.ForeignKey(Species)
    history = HistoricalRecords()

    def __str__(self):
        
        Shows bird information in a human-readable format
        
        return self.species.name

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value
"""

class Choice(models.Model):
    """ Boolean choices. We don't want text answers"""
    options = models.CharField(max_length=5)
    history = HistoricalRecords()

    def __str__(self):
        """ display choice text. """
        return str(self.options)

class Question(models.Model):
    """ species' category. """
    text = models.CharField(max_length=255)
    choices = models.ManyToManyField(Choice)
    history = HistoricalRecords()

    def __str__(self):
        """ display name. """
        return self.text

class Checklist(models.Model):
    """
    A checklist used to find out information about a species.
    Has questions and choices
    """
    species = models.ForeignKey(Species)
    questions = models.ManyToManyField(Question)
    history = HistoricalRecords()

    def __str__(self):
        """
        Tell's what species the checklist is for
        """
        return str(self.species.type) + "'s Checklist"

class DailyUpdate(models.Model):
    """
    
    """
    species = models.ForeignKey(SpecificSpecies)
    checklist = models.ForeignKey(Checklist)
    history = HistoricalRecords()

    def __str__(self):
         """
         display string. 
         """
         return str(self.species.common_name) + "'s Observation"

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value
"""
class DailyUpdate(models.Model):
    a tree daily update. each instance is bound to a specified tree.
    tree = models.ForeignKey(Tree)
    # added_by = models.ForeignKey('auth.User', related_name='creator')
    changed_by = models.ForeignKey('auth.User', related_name='modifier')
    choices = models.ManyToManyField(Choice)
    image = models.ImageField(max_length=None, null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self):
         display string. 
        return 'Daily Update # ' + str(self.id) + ' of ' + str(self.tree)

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value
"""
