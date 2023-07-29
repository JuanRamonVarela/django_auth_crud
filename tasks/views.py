from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import TaskForm
from .models import tasks
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method=="GET":
        return render(request, 'signup.html',{
            'form':UserCreationForm
        })
    else:
        if request.POST['password1']==request.POST["password2"]:
            #register user
            try:
                user=User.objects.create_user(username=request.POST["username"], 
                                              password=request.POST["password1"])
                user.save()
                #return  HttpResponse("Usuario Creado")
                #return render(request, 'tasks.html')
                login(request, user)
                return redirect("tasks")
            except InterruptedError:
                return render(request, 'signup.html',{
                            'form':UserCreationForm,
                            'error':"Usario Registrado"
                        })
                #return HttpResponse("Usuario existe")
        #return HttpResponse("No coinciden las passwords")
        return render(request, 'signup.html',{
            'form':UserCreationForm,
            'error':"Las contraseñas no coinciden"
        })

@login_required
#No declarar modelos con el mismo nombre de las funciones
def tareas(request):
    #task=tasks.objects.all()
    task=tasks.objects.filter(user=request.user, datecompleted__isnull=True)
    #task=tasks.objects.filter(user=request.user)
    return render(request, "tasks.html", {'tasks':task})

@login_required
def tareas_completas(request):
    #task=tasks.objects.all()
    task=tasks.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    #task=tasks.objects.filter(user=request.user)
    return render(request, "tasks.html", {'tasks':task})

@login_required
def create_task(request):
    if request.method=="GET":
        return render(request, "create_task.html",{
            'form':TaskForm
        })
    else:
        #print(request.POST)
        try:
            forms=TaskForm(request.POST)
            new_task=forms.save(commit=False)
            new_task.user=request.user
            new_task.save()
            #print(new_task)
            return redirect('tasks')
        except ValueError:
            return render(request, "create_task.html",{
                'form':TaskForm,
                'error':"Inserta datos validos",
            })

@login_required
def task_detail(request, task_id):
    if request.method=="GET":
        #task=tasks.objects.get(pk=task_id)
        task=get_object_or_404(tasks, pk=task_id, user=request.user)
        form=TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task':task, 'form':form})
    else:
        try:
            task=get_object_or_404(tasks,pk=task_id, user=request.user)
            form=TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'task':task, 
            'form':form, 'error':'Error al actualizar task'})

@login_required     
def task_completed(request, task_id):
    task=get_object_or_404(tasks, pk=task_id, user=request.user)
    if request.method=="POST":
        task.datecompleted=timezone.now()
        task.save()
        return redirect('tasks')
    task=get_object_or_404(tasks, pk=task_id, user=request.user)
    if request.method=="POST":
        task.datecompleted=timezone.now()
        task.save()
        return redirect('tasks')
    
@login_required
def task_delete(request, task_id):
    task=get_object_or_404(tasks, pk=task_id, user=request.user)
    if request.method=="POST":
        task.delete()
        return redirect('tasks')

@login_required 
#no declarar el logout con ese nombre, puede haber problema
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method=="GET":
        return render(request, 'signin.html',{
            'form':AuthenticationForm
        })
    else:
        #print(request.POST)
        user=authenticate(request, username=request.POST['username'],
                     password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html',{
            'form':AuthenticationForm,
            'error':'Usuario o contrasena incorrecto'
            })
        else:
            login(request, user)
            return redirect('tasks')
