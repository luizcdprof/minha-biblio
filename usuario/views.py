from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UsuarioForm, TurmaForm, LoginForm
from .models import Turma, Usuario
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout, authenticate

# Create your views here.
def home_view(request):
    return render(request, 'home.html')

def is_bibliotecario(user):
    return hasattr(user, 'usuario_user_set') and user.usuario_user_set.perfil == 'bibliotecario'

def usuario_login(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login realizado com sucesso!')
                return redirect('usuario_exibir_logado')
            else:
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
def usuario_exibir(request, id=None):
    #usuario = get_object_or_404(Usuario, id=id)
    if id:
        usuario = get_object_or_404(Usuario, id=id)
    else:
        usuario = request.user.usuario_user_set  # usuário logado
    return render(request, 'usuario_exibir.html', {'usuario': usuario})

@user_passes_test(is_bibliotecario)
def usuario_listar(request):
    usuarios = Usuario.objects.all()
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