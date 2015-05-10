from tutor.models import *
from django.contrib import admin
'''
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3
'''	
class UniversidadAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    '''
    fieldsets = [
        (None,               {'fields': ['question']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question', 'pub_date', 'was_published_recently')
    #list_filter = ['pub_date']
    search_fields = ['question']
    #date_hierarchy = 'pub_date'
    '''
	
class EventoAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo')

class NoticiaAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'fechapub')
    list_filter = ['fechapub']
    date_hierarchy = 'fechapub'
	
admin.site.register(Universidad, UniversidadAdmin)
admin.site.register(Noticia, NoticiaAdmin)
admin.site.register(Evento, EventoAdmin)