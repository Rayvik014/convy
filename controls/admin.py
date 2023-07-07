from django.contrib import admin
from .models import Sector, Word, Progress
# Register your models here.
class SectorAdmin(admin.ModelAdmin):
    list_display = ('id', 'sectors')
    list_display_links = ('sectors', )
    search_fields = ('sectors', )

class WordAdmin(admin.ModelAdmin):
    list_display = ('id', 'lang1', 'lang2', 'sector')
    list_display_links = ('lang1', )
    search_fields = ('lang1', )

class ProgressAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'word_id', 'chance')
    list_display_links = ('user_id', 'word_id')
    search_fields = ('user_id', 'word_id')

admin.site.register(Sector, SectorAdmin)
admin.site.register(Word, WordAdmin)
admin.site.register(Progress, ProgressAdmin)