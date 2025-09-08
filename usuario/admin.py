from django.contrib import admin
from .models import Usuario, Turma

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'ra', 'turma', 'telefone')
    search_fields = ('user__username', 'user__email', 'ra')
    list_filter = ('turma',)
    raw_id_fields = ('user',)

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Turma)
