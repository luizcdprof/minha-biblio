from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UsuarioForm, TurmaForm, LoginForm
from .models import Turma, Usuario
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt # REMOVER DA PRODUÇÃO - USAR EM DEBUG APENAS

# Create your views here.
def home_view(request):
    return render(request, 'home.html')

def is_bibliotecario(user):
    return hasattr(user, 'usuario_user_set') and user.usuario_user_set.perfil == 'bibliotecario'

@csrf_exempt  # REMOVER DA PRODUÇÃO - USAR EM DEBUG APENAS
def usuario_login(request):
    form = LoginForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                login(request, user)

                # Resposta para requisição AJAX (JSON)
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': True, 'message': 'Login realizado com sucesso!'})

                # Resposta para navegador (HTML)
                messages.success(request, 'Login realizado com sucesso!')
                return redirect('usuario_exibir_logado')
            else:
                # Resposta para requisição AJAX (JSON)
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'message': 'E-mail ou senha inválidos.'})

                # Resposta para navegador (HTML)
                messages.error(request, 'E-mail ou senha inválidos.')
    return render(request, 'usuario_login.html', {'form': form})

@login_required
def usuario_logout(request):
    logout(request)
    messages.success(request, 'Logout realizado com sucesso!')
    return redirect('home')

def usuario_cadastrar(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario.user)  # loga o usuário automaticamente
            messages.success(request, 'Usuário cadastrado com sucesso!')
            return render(request, 'usuario_exibir.html', {'usuario': usuario})
        else:
            messages.error(request, 'Erro ao cadastrar usuário. Verifique os dados e tente novamente.')
    else:
        form = UsuarioForm()
    return render(request, 'usuario_cadastrar.html', {'form': form})

@login_required
@csrf_exempt  # REMOVER DA PRODUÇÃO - USAR EM DEBUG APENAS
def usuario_exibir(request, id=None):
    usuario = request.user.usuario_user_set  # usuário logado

    if id:
        if not is_bibliotecario(request.user) and usuario.id != id:
            # Resposta para requisição AJAX (JSON)
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse(
                    {'success': False, 'message': 'Você não tem permissão para ver este perfil.'},
                    status=403 # Retorna status HTTP 403 Forbidden
                )
            
            # Resposta para navegador (HTML)
            messages.error(request, 'Você não tem permissão para ver este perfil.')
            return redirect('home')
        else:
            usuario = get_object_or_404(Usuario, id=id)

    # Resposta para requisição AJAX (JSON)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Converte o objeto de usuário em um dicionário para serializar
        usuario_data = {
            'id': usuario.id,
            'username': usuario.user.username,
            'email': usuario.user.email,
            'perfil': usuario.perfil,
            'ra': usuario.ra,
            'telefone': usuario.telefone,
            'turma_nome': usuario.turma.nome if usuario.turma else None,
            'turma_periodo': usuario.turma.periodo if usuario.turma else None,
        }
        return JsonResponse({'success': True, 'usuario': usuario_data})

    # Resposta para navegador (HTML)
    return render(request, 'usuario_exibir.html', {'usuario': usuario})

@user_passes_test(is_bibliotecario)
@csrf_exempt  # REMOVER DA PRODUÇÃO - USAR EM DEBUG APENAS
def usuario_listar(request):
    usuarios = Usuario.objects.all()

    # Resposta para requisição AJAX (JSON)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        usuarios_data = []
        for usuario in usuarios:
            usuarios_data.append({
                'id': usuario.id,
                'username': usuario.user.username,
                'email': usuario.user.email,
                'perfil': usuario.perfil,
                'ra': usuario.ra,
                'telefone': usuario.telefone,
                'turma_nome': usuario.turma.nome if usuario.turma else None,
                'turma_periodo': usuario.turma.periodo if usuario.turma else None,
            })
        return JsonResponse({'success': True, 'usuarios': usuarios_data})
    
    # Resposta para navegador (HTML)
    return render(request, 'usuario_listar.html', {'usuarios': usuarios})

@login_required
def usuario_atualizar(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados do usuário atualizados com sucesso!')
            return redirect('usuario_listar')
        else:
            messages.error(request, 'Erro ao atualizar dados. Verifique os campos e tente novamente.')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'usuario_cadastrar.html', {'form': form, 'usuario': usuario, 'editar': True})

@login_required
def usuario_excluir(request):
    usuario = request.user.usuario_user_set
    if request.method == 'POST':
        usuario.user.delete()
        messages.success(request, 'Seu perfil foi excluído com sucesso.')
        return redirect('home')
    return render(request, 'usuario_confirmar_exclusao.html', {'usuario': usuario})

@login_required
def turma_cadastrar(request):
    if request.method == 'POST':
        form = TurmaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Turma cadastrada com sucesso!')
            turmas = Turma.objects.all()
            return render(request, 'turma_listar.html', {'turmas': turmas})
        else:
            messages.error(request, 'Erro ao cadastrar turma. Verifique os dados e tente novamente.')
    else:
        form = TurmaForm()
    return render(request, 'turma_cadastrar.html', {'form': form})

@user_passes_test(is_bibliotecario)
def turma_editar(request, id):
    turma = get_object_or_404(Turma, id=id)
    if request.method == 'POST':
        form = TurmaForm(request.POST, instance=turma)
        if form.is_valid():
            form.save()
            messages.success(request, 'Turma editada com sucesso!')
            turmas = Turma.objects.all()
            return render(request, 'turma_listar.html', {'turmas': turmas})
        else:
            messages.error(request, 'Erro ao editar turma. Verifique os dados e tente novamente.')
    else:
        form = TurmaForm(instance=turma)
    return render(request, 'turma_cadastrar.html', {'form': form, 'editar': True})

@login_required
def turma_excluir(request, id):
    turma = get_object_or_404(Turma, id=id)
    if request.method == 'POST':
        turma.delete()
        messages.success(request, 'Turma excluída com sucesso!')
        turmas = Turma.objects.all()
        return render(request, 'turma_listar.html', {'turmas': turmas})
    return render(request, 'turma_confirmar_exclusao.html', {'turma': turma})

@login_required
def turma_listar(request):
    turmas = Turma.objects.all()
    return render(request, 'turma_listar.html', {'turmas': turmas})