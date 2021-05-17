from django.contrib import admin
from . import models

# Register your models here.

class AdsAdmin(admin.ModelAdmin):
    
    list_display = ('id','orgname','weburl','adsdec','adimg','pubtime','is_active')
    list_filter = ('is_active','tags')
    search_fields = ('orgname','adsdec','tags')
    ordering = ('pubtime',)

    

admin.site.register(models.Ads,AdsAdmin)
admin.site.register(models.Tag)
admin.site.register(models.AdsDomains)