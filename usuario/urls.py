from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.usuario_login, name='usuario_login'),
    path('logout/', views.usuario_logout, name='usuario_logout'),
    path('cadastrar/', views.usuario_cadastrar, name='usuario_cadastrar'),
    path('atualizar/<int:id>', views.usuario_atualizar, name='usuario_atualizar'),
    path('exibir/', views.usuario_exibir, name='usuario_exibir_logado'),
    path('exibir/<int:id>/', views.usuario_exibir, name='usuario_exibir'),
    path('listar/', views.usuario_listar, name='usuario_listar'),
    path('excluir/<int:id>/', views.usuario_excluir, name='usuario_excluir'),
    path('turma/cadastrar/', views.turma_cadastrar, name='turma_cadastrar'),
    path('turma/editar/<int:id>/', views.turma_editar, name='turma_editar'),
    path('turma/excluir/<int:id>/', views.turma_excluir, name='turma_excluir'),
    path('turma/listar/', views.turma_listar, name='turma_listar'),
]