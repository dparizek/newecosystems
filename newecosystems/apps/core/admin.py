from django.contrib import admin
from .models import *
from .settings import *

class PlantAdmin(admin.ModelAdmin):
    list_display = ('common_name', 'family', 'genus', 'species', 'is_native', 'annual_perennial', 'annualness_index', 'shade_open', 'forb_to_tree_index', 'water_low_medium_high', 'water_needs_index', 'commonality_index', 'common_scarce_index', 'flower_spring', 'flower_summer', 'flower_fall', 'flower_winter')
    search_fields = ('family', 'genus', 'species', 'common_name', )
    prepopulated_fields = {"slug": ("genus", 'species',)}


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'project_creator', 'project_summary', )

class FireflyAdmin(admin.ModelAdmin):
    list_display = ('firefly_plant', 'firefly_html', 'firefly_duration', 'firefly_growth_habit', 'firefly_special')


admin.site.register(Plant, PlantAdmin)
admin.site.register(Firefly, FireflyAdmin)
admin.site.register(Project, ProjectAdmin)
