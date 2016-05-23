"""
LAP Models.
Each models should have a history field of type HistoricalRecords to store the history.
 
"""

from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords
from PIL import Image, ImageFile
import io
from io import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from lap_django.settings import MEDIA_ROOT
import datetime
class DBLastChangeTime(models.Model):
    """ Save last change time of the database. """
    type = models.CharField(max_length=30)
    time = models.DateTimeField(auto_now=True)


def get_db_last_change_time(type):
    """ Get the time of last change of the database. """
    try:
        o = DBLastChangeTime.objects.get(type=type)
        return o
    except:
        return None

def set_db_last_change_time(instance, created, raw, **kwargs):
    t = get_db_last_change_time(instance.__class__.__name__)
    if not t:
        t = DBLastChangeTime()
        t.type = instance.__class__.__name__
    t.save()

def set_db_last_change_time_deletion(instance, **kwargs):
    t = get_db_last_change_time(instance.__class__.__name__)
    if not t:
        t = DBLastChangeTime()
        t.type = instance.__class__.__name__
    t.save()

class Season(models.Model):
    """Seasons for available semesters"""
    name = models.CharField(max_length=50)
    history = HistoricalRecords()

    def __str__(self):
        """ display the category name of the semester e.g. Fall """
        return self.name

#Gives choices in the format of year - year e.g 2015 - 2016
#Found here: https://groups.google.com/forum/#!msg/django-users/al95x1TXFV4/7mCCWQE3jtAJ
YEAR_CHOICES = []
for year in range(2015, (datetime.datetime.now().year + 1)):
    YEAR_CHOICES.append((year, year))

class Semester(models.Model):
    """School semester information"""
    season = models.ForeignKey(Season)
    year = models.IntegerField(('year'), max_length=4, choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    history = HistoricalRecords()

    def __str__(self):
        """ display the category name of the semester e.g. Fall """
        return str(season) + " " + str(year)

class SemesterClass(models.Model):
    """Information for a specific semester"""
    category_id = models.IntegerField(help_text="Enter the id of this class from the school catelog");
    name = models.CharField(max_length=255)
    semester = models.ForeignKey(Semester);

    def __str__(self):
        """ display the category name of the class e.g. Biology 101 - Fall 2015, 2016"""
        return self.name + " - " + str(self.semester)

class UserProfile(models.Model):
    """Profile for the user. Contains class information"""
    user = models.ForeignKey(User)
    current_class = models.ForeignKey(SemesterClass)

    def __str__(self):
        """ display info of the User"""
        return str(self.user.username) + " in " + str(self.current_class)

class SpeciesType(models.Model):
    """ species type. """
    name = models.CharField(max_length=50)
    history = HistoricalRecords()

    def __str__(self):
        """ display the category name of the species e.g. bird. """
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
    type = models.ForeignKey(SpeciesType)
    scientific_name = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=2048)
    image = models.ImageField(max_length=None, null=True, blank=True, upload_to='species')
    history = HistoricalRecords()

    def __str__(self):
        """ display name. """
        return "[" + str(self.id) + "]" + self.name

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value 


class DeletedTree(models.Model):
    """ Store the deleted trees' ids.
    NOTE: Should use push notification if have more time """
    tree_id = models.IntegerField()
    time = models.DateTimeField(auto_now=True)


class Tree(models.Model):
    """ a tree instance. it contains location (longitude and latitude). """
    species = models.ForeignKey(TreeSpecies)
    long = models.FloatField()
    lat = models.FloatField()
    changed_by = models.ForeignKey('auth.User')
    image = models.ImageField(max_length=None, null=True, blank=True)
    date_modified = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        """ display species name and tree id. """
        return str(self.species) + ' observation # [' + str(self.id) + '] found at lat ' + str(self.lat)  + ', ' + str(self.long) + ' long' 

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value


def add_to_deleted_list(instance, **kwargs):
    """ Add tree id to deleted_list after delete it from the database """
    d = DeletedTree(tree_id=instance.id)
    d.save()


class Bird(models.Model):
    """
    
    """
    type = models.ForeignKey(SpeciesType)
    scientific_name = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=2048)
    image = models.ImageField(max_length=None, null=True, blank=True, upload_to='species')
    history = HistoricalRecords()

    def __str__(self):
        """ display name. """
        return "[" + str(self.id) + "] " + self.name

    #@property
    #def _history_user(self):
    #    return self.changed_by

    #@_history_user.setter
    #def _history_user(self,value):
    #    self.changed_by = value

class Choice(models.Model):
    """ choices. """
    question = models.ForeignKey(Question)
    value = models.BooleanField(default=False)
    history = HistoricalRecords()

    def __str__(self):
        """ display choice text. """
        return str(self.question) + '|' + str(self.value)


class DailyUpdate(models.Model):
    """ a tree daily update. each instance is bound to a specified tree. """
    tree = models.ForeignKey(Tree)
    changed_by = models.ForeignKey('auth.User')
    choices = models.ManyToManyField(Choice)
    image = models.ImageField(max_length=None, null=True, blank=True)
    date_of_observation = models.DateTimeField(auto_now=True)    
    birds = models.ManyToManyField(Bird, blank=True)
    history = HistoricalRecords()

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


# update db_last_change_time after every model's save
models.signals.post_save.connect(set_db_last_change_time, sender=Tree, dispatch_uid='set_db_last_change_time')
models.signals.post_save.connect(set_db_last_change_time, sender=Question, dispatch_uid='set_db_last_change_time')
models.signals.post_save.connect(set_db_last_change_time, sender=Bird, dispatch_uid='set_db_last_change_time')
models.signals.post_save.connect(set_db_last_change_time, sender=DailyUpdate, dispatch_uid='set_db_last_change_time')
models.signals.post_save.connect(set_db_last_change_time, sender=TreeSpecies, dispatch_uid='set_db_last_change_time')
models.signals.post_delete.connect(set_db_last_change_time_deletion, sender=Tree, dispatch_uid='set_db_last_change_time_deletion')
models.signals.post_delete.connect(set_db_last_change_time_deletion, sender=Question, dispatch_uid='set_db_last_change_time_deletion')
models.signals.post_delete.connect(set_db_last_change_time_deletion, sender=Bird, dispatch_uid='set_db_last_change_time_deletion')
models.signals.post_delete.connect(set_db_last_change_time_deletion, sender=DailyUpdate, dispatch_uid='set_db_last_change_time_deletion')
models.signals.post_delete.connect(set_db_last_change_time_deletion, sender=TreeSpecies, dispatch_uid='set_db_last_change_time_deletion')
models.signals.post_delete.connect(add_to_deleted_list, sender=Tree, dispatch_uid='add_to_deleted_list')
