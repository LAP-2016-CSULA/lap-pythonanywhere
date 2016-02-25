"""
LAP Models.
Each models should have a history field of type HistoricalRecords to store the history.
 
"""

from django.db import models
from simple_history.models import HistoricalRecords
from PIL import Image, ImageFile
import io
from io import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from lap_django.settings import MEDIA_ROOT
from datetime import datetime

class SpeciesType(models.Model):
    """ species type. """
    name = models.CharField(max_length=50)
    history = HistoricalRecords()

    def __str__(self):
        """ display the category name of the species e.g. bird. """
        return self.name


class Species(models.Model):
    """ species model. """
    type = models.ForeignKey(SpeciesType)
    scientific_name = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=2048)
    image = models.ImageField(max_length=None, null=True, blank=True, upload_to='species')
    history = HistoricalRecords()

    def __str__(self):
        """ display name. """
        return self.name

def create_choices_on_question_creation(instance, created, raw, **kwargs):
    """ Create 2 choices for each question.
    Check post_save in the django documentation for the parameter
    """
    if created:
        c1 = Choice(question=instance, value=True)
        c2 = Choice(question=instance, value=False)
        c1.save()
        c2.save()


class Question(models.Model):
    """ species' category. """
    text = models.CharField(max_length=255)
    history = HistoricalRecords()

    def __str__(self):
        """ display name. """
        return self.text

# Auto create 2 choices in the db coresponse to each question on its creation
models.signals.post_save.connect(create_choices_on_question_creation, sender=Question, dispatch_uid='create_choices_on_question_creation')       

class TreeSpecies(models.Model):
    species = models.ForeignKey(Species)
    history = HistoricalRecords()

    def __str__(self):
        """
        Shows bird information in a human-readable format
        """
        return self.species.name

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value 

class Tree(models.Model):
    """ a tree instance. it contains location (longitude and latitude). """
    species = models.ForeignKey(TreeSpecies)
    long = models.FloatField()
    lat = models.FloatField()
    changed_by = models.ForeignKey('auth.User')
    image = models.ImageField(max_length=None, null=True, blank=True)
    date_modified = models.DateTimeField(default=datetime.now(), blank=True)
    history = HistoricalRecords()

    def __str__(self):
        """ display species name and tree id. """
        return self.species.species.name + ' [' + str(self.id) + '] found at lat ' + str(self.lat)  + ', ' + str(self.long) + ' long' 

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value


class Bird(models.Model):
    """
    A bird instance. It should contain the the tree instance it was interacting with.
    """
    species = models.ForeignKey(Species)
    history = HistoricalRecords()

    def __str__(self):
        """
        Shows bird information in a human-readable format
        """
        return self.species.name

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
    history = HistoricalRecords()

    def __str__(self):
        """ display choice text. """
        return str(self.question) + '|' + str(self.value)

class BirdChoice(models.Model):
    choice = models.ForeignKey(Choice)

    def __str__(self):
        """ display choice text. """
        return str(self.choice)

class TreeChoice(models.Model):
    choice = models.ForeignKey(Choice)

    def __str__(self):
        return str(self.choice)

class BirdObservation(models.Model):
    """

    """
    bird = models.ForeignKey(Bird)
    tree_observed_on = models.ForeignKey(Tree, blank=False)
    choices = models.ManyToManyField(BirdChoice)
    date_of_observation = models.DateTimeField(default=datetime.now, blank=True)
    image = models.ImageField(max_length=None, null=True, blank=True)

    def __str__(self):
        """

        """
        return "Observation " + str(self.id) + " of " + str(self.bird)

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
    choices = models.ManyToManyField(TreeChoice)
    image = models.ImageField(max_length=None, null=True, blank=True)
    history = HistoricalRecords()

    #http://stackoverflow.com/questions/24373341/django-image-resizing-and-convert-before-upload
    #def save(self, *args, **kwargs):
    #    """ Override save. Resize the image ratio """
    #    if self.image:
    #        image = Image.open(StringIO(self.image.read()))
    #        #image = Image.open(io.BytesIO(self.image.read()))
    #        #image = Image.open(self.image.path)
    #        h = image.height
    #        w = int(h * 2 / 3)
    #        image.resize((w, h))
    #        output = StringIO()
    #        image.save(output, 'JPEG')
    #        output.seek(0)
    #        self.image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" %self.image.name, 'image/jpeg', output.len, None)
    #    super(DailyUpdate, self).save(*args, **kwargs)

    def __str__(self):
        """ display string. """
        return 'Daily Update # ' + str(self.id) + ' of ' + str(self.tree)

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value

def link_image_to_tree(instance, created, raw, **kwargs):
    """ Link the image from daily update to the tree if it exists. """
    if instance:
        tree = Tree.objects.get(pk=instance.tree.pk)
        if tree and instance.image:
            tree.image = instance.image
            tree.save()

# link image to tree image
models.signals.post_save.connect(link_image_to_tree, sender=DailyUpdate, dispatch_uid='link_image_to_tree')

    