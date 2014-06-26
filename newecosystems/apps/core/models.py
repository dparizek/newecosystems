import os
import random
import datetime
from django.db import models
from django.contrib.auth.models import User, Group
from django.forms import ModelForm, Textarea, TextInput
from django.forms.extras.widgets import SelectDateWidget
from .settings import *

from django.db import transaction
from itertools import chain
from taggit.managers import TaggableManager



def get_file_path(instance, filename):
    dateString = datetime.datetime.now().strftime("%Y/%m/%d")
    return os.path.join('uploads', dateString, filename)


class Organization(models.Model):
    organization_name = models.CharField(max_length=200)
    organization_type = models.CharField(max_length=8, choices=ORGANIZATION_TYPES)
    organization_contact_info = models.TextField(max_length=3000, help_text='Addresses, phone numbers, email addresses, contact names...', blank=True)


class Plant(models.Model):
    compiled_by = models.CharField(max_length=20, blank=True, null=True)
    family = models.CharField(max_length=60)
    genus = models.CharField(max_length=50)
    species = models.CharField(max_length=50)
    slug = models.SlugField(max_length=80)
    common_name = models.CharField(max_length=100, blank=True, null=True)
    is_native = models.IntegerField(choices=YES_NO_CHOICES, null=True)
    annual_perennial = models.CharField(max_length=16, choices=ANN_PER_CHOICES, blank=True, null=True)
    annualness_index = models.FloatField(null=True)  # annual=0, perennial=1, annual/perennial=0.5
    habit = models.CharField(max_length=60, blank=True, null=True)
    forb_to_tree_index = models.FloatField(blank=True, null=True)  # forb/herb/grass=0, subshrub=1, vine=1.5, herb/vine=?, shrub=2, tree=3
    aspect = models.CharField(max_length=60, blank=True, null=True)
    shade_open = models.CharField(max_length=20, blank=True, null=True)
    shade_open_index = models.FloatField(choices=SHADE_CHOICES, blank=True, null=True)
    substrate = models.CharField(max_length=60, blank=True, null=True)
    water_low_medium_high = models.CharField(max_length=20, choices=WATER_CHOICES, blank=True, null=True)
    water_needs_index = models.FloatField(choices=WATER_INDEX_CHOICES, blank=True, null=True)
    water_slope = models.CharField(max_length=100, blank=True, null=True)
    common_scarce = models.CharField(max_length=25, blank=True, null=True)
    common_scarce_index = models.FloatField(choices=YES_NO_CHOICES, blank=True, null=True)
    commonality_index = models.IntegerField(choices=COMMONALITY_CHOICES, blank=True, null=True)
    elevation = models.CharField(max_length=20, blank=True, null=True)
    loweboundary = models.CharField(max_length=20, blank=True, null=True)
    highebound = models.CharField(max_length=20, blank=True, null=True)
    flowering_time = models.CharField(max_length=50, blank=True, null=True)
    flower_spring = models.IntegerField(choices=YES_NO_CHOICES, blank=True, null=True)
    flower_summer = models.IntegerField(choices=YES_NO_CHOICES, blank=True, null=True)
    flower_fall = models.IntegerField(choices=YES_NO_CHOICES, blank=True, null=True)
    flower_winter = models.IntegerField(choices=YES_NO_CHOICES, blank=True, null=True)
    benign_or_not = models.IntegerField(choices=YES_NO_CHOICES, blank=True, null=True)
    cryptically_malignant = models.CharField(max_length=200, blank=True, null=True)
    obviously_malignant = models.CharField(max_length=200, blank=True, null=True)
    habitat_requirement = models.CharField(max_length=200, blank=True, null=True)
    plant_range = models.CharField(max_length=200, blank=True, null=True)
    species_association = models.CharField(max_length=200, blank=True, null=True)
    jonathan_comments = models.CharField(max_length=240, blank=True, null=True)
    source_url = models.TextField(blank=True, null=True)
    photo_url = models.TextField(blank=True, null=True)
    availability = models.CharField(max_length=100, blank=True, null=True)
    firefly_url = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ('genus', 'species')

    def __unicode__(self):
        return self.common_name


class PlantsForm(ModelForm):

    class Meta:
        model = Plant
        fields = ('family', 'genus', 'species', 'common_name', 'is_native', 'annual_perennial', 'habit', 'aspect', 'shade_open', 'substrate', 'water_low_medium_high', 'water_slope', 'common_scarce', 'habit', 'flower_spring', 'flower_summer', 'flower_fall', 'flower_winter', 'benign_or_not', 'obviously_malignant')


class Firefly(models.Model):
    firefly_plant = models.ForeignKey(Plant, verbose_name='Plant')  #related_name='firefly_plant_related',
    firefly_html = models.TextField(blank=True, null=True)
    firefly_duration = models.CharField(max_length=254, blank=True, null=True)
    firefly_growth_habit = models.CharField(max_length=254, blank=True, null=True)
    firefly_native_status = models.CharField(max_length=254, blank=True, null=True)
    firefly_habitat = models.CharField(max_length=254, blank=True, null=True)
    firefly_flower_color = models.CharField(max_length=254, blank=True, null=True)
    firefly_flower_season = models.CharField(max_length=254, blank=True, null=True)
    firefly_height = models.CharField(max_length=254, blank=True, null=True)
    firefly_special = models.TextField(blank=True, null=True)
    firefly_description = models.TextField(blank=True, null=True)
    firefly_class = models.CharField(max_length=100, blank=True, null=True)
    firefly_subclass = models.CharField(max_length=100, blank=True, null=True)
    firefly_order = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ('firefly_plant', )
        verbose_name_plural = 'Firefly Pages'

    def __unicode__(self):
        return self.firefly_plant.common_name


class Project(models.Model):
    project_name = models.CharField(max_length=20, verbose_name='Project Name')
    project_summary = models.CharField(max_length=254, verbose_name='Summary')
    project_creator = models.ForeignKey(User, related_name='project_creator', verbose_name='Creator')
    project_creation_date = models.DateTimeField(auto_now_add=True)
    greenhouse_plants = models.ManyToManyField(Plant, related_name="greenhouse_plants", blank=True, null=True)  #a shopping cart of plant spp that they will eventually kick to the wizard to generate a complementary spp list
    belle_ball_plants = models.ManyToManyField(Plant, related_name="belle_ball_plants", blank=True, null=True)  #list of plants they want to favorite - include for sure
    exclude_plants = models.ManyToManyField(Plant, related_name="exclude_plants", blank=True, null=True)  #list of plants they want to exclude

    class Meta:
        ordering = ('project_name', )

    def __unicode__(self):
        return self.project_name
        

class Photo(models.Model):
    photo_plant = models.ForeignKey(Plant, related_name='photo_plant_related', verbose_name='Plant')
    file = models.FileField(upload_to='uploaded-photos')
    photo_caption = models.CharField(max_length=254, verbose_name='Caption')
    photo_name = models.CharField(max_length=100)
    uploaded_by_who = models.ForeignKey(User, related_name='uploaded_by', blank=True, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('photo_plant', )

    def __unicode__(self):
        return self.file.name


class UploadedFile(models.Model):
    projectfk = models.ForeignKey(Project, verbose_name='Project ID', related_name="%(app_label)s_%(class)s_related")
    file_description = models.CharField(max_length=500, help_text='A brief description of the file.', blank=True, null=True)
    the_file = models.FileField(upload_to=get_file_path)
    uploaded_by_who = models.ForeignKey(User, related_name='file_uploaded_by')
    upload_date = models.DateTimeField(auto_now_add=True)

    @property
    def filename(self):
        return os.path.basename(self.the_file.name)

    @property
    def filesize(self):
        return self.the_file.size

    def __unicode__(self):
        return self.filename