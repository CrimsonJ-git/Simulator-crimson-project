from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden,JsonResponse
from .simulation import sim
from .models import Registro,Revision
from django.contrib import messages
from django.contrib import sessions
import json
from django.core.paginator import Paginator
from django.db.models import Q
import datetime as dt


def asignar_rol(usuario, rol):
    grupo, created = Group.objects.get_or_create(name=rol)
    usuario.groups.add(grupo)
    usuario.save()


@login_required
def main(request):
    user_groups = request.user.groups.values_list('name', flat=True)
    if 'tecnician' in user_groups:
        return render(request, 'app/main_t.html')
    elif 'engineer' in user_groups:
        return render(request,'app/main.html')
        #return HttpResponse("Hola ingeniero")
    elif 'supervisor' in user_groups:
        #return render(request,'app/chinchilla.html')
        return render(request,"app/main_s.html")
    else:
        return render(request,'app/access_denied.html')

@login_required
def start_simulation(request):
    user_groups = request.user.groups.values_list('name', flat=True)
    
    # Verificar si el usuario pertenece al grupo "engineer"
    if 'engineer' in user_groups:
        if request.method == 'POST':
            # Iniciar la simulación tras la confirmación
            return redirect('confirmar')

    # Si no es ingeniero, acceso denegado
    return render(request, 'app/access_denied.html', status=403)

@login_required
def confirmar(request):
    user_groups = request.user.groups.values_list('name', flat=True)
    
    # Verificar si el usuario pertenece al grupo "engineer"
    if 'engineer' in user_groups:
        if request.method == 'POST':
            # Realizar la simulación en este paso
            sim.switch_all()  # Iniciar la simulación
            sim.analysis()  # Ejecutar el análisis

            # Obtener datos de la simulación si es necesario
            source = sim.source_data()
            machine_01 = sim.machine_data('vo_1','l1')
            machine_02 = sim.machine_data('vo_2','l2')
            machine_03 = sim.machine_data('vo_3','l3')
            machine_04 = sim.machine_data('vo_4','l4')
            # Mostrar mensaje de éxito
            messages.success(request, "Máquinas trabajando")
            registro_s = Registro.objects.create(
                name="Source",  # Aquí puedes definir un nombre para la fuente, o usar otro dato
                type_comp="Source",  # Aquí puedes poner el tipo de la fuente, o usar otro dato del diccionario
                active_power=source['activa'],  # Usando los valores del diccionario
                reactive_power=source['reactiva'],
                factor=source['factor'],
                S_power=source['aparente'],
                hora=dt.datetime.now(),
            )
            registro_1 = Registro.objects.create(
                name="machine 01",  # Aquí puedes definir un nombre para la fuente, o usar otro dato
                type_comp="machine",  # Aquí puedes poner el tipo de la fuente, o usar otro dato del diccionario
                active_power=machine_01['activa'],  # Usando los valores del diccionario
                reactive_power=machine_01['reactiva'],
                factor=machine_01['factor'],
                S_power=machine_01['aparente'],
                hora=dt.datetime.now(),
            )
            registro_2 = Registro.objects.create(
                name="machine 02",  # Aquí puedes definir un nombre para la fuente, o usar otro dato
                type_comp="machine",  # Aquí puedes poner el tipo de la fuente, o usar otro dato del diccionario
                active_power=machine_02['activa'],  # Usando los valores del diccionario
                reactive_power=machine_02['reactiva'],
                factor=machine_02['factor'],
                S_power=machine_02['aparente'],
                hora=dt.datetime.now(),
            )
            registro_3 = Registro.objects.create(
                name="machine 03",  # Aquí puedes definir un nombre para la fuente, o usar otro dato
                type_comp="machine",  # Aquí puedes poner el tipo de la fuente, o usar otro dato del diccionario
                active_power=machine_03['activa'],  # Usando los valores del diccionario
                reactive_power=machine_03['reactiva'],
                factor=machine_03['factor'],
                S_power=machine_03['aparente'],
                hora=dt.datetime.now(),
            )
            registro_4 = Registro.objects.create(
                name="machine 04",  # Aquí puedes definir un nombre para la fuente, o usar otro dato
                type_comp="machine",  # Aquí puedes poner el tipo de la fuente, o usar otro dato del diccionario
                active_power=machine_04['activa'],  # Usando los valores del diccionario
                reactive_power=machine_04['reactiva'],
                factor=machine_04['factor'],
                S_power=machine_04['aparente'],
                hora=dt.datetime.now(),
            )
            registro_s.save()
            registro_1.save()
            registro_2.save()
            registro_3.save()
            registro_4.save()
            # Redirigir al main con el mensaje de éxito
            return redirect('main')

        # Si el método es GET, mostrar la página de confirmación
        return render(request, 'app/confirmar.html')

    else:
        return render(request, 'app/access_denied.html', status=403)
    
@login_required
def restart_machines(request):
    user_groups = request.user.groups.values_list('name', flat=True)
    if 'engineer' in user_groups:
        if request.method == 'POST':
            sim.restart_all()
            Registro.objects.all().delete()
            messages.success(request, "Máquinas reiniciadas y datos de simulación limpiados")
            return redirect('main')
    if 'tecnician' in user_groups:
        if request.method =='POST':
        
            Revision.objects.all().delete()
            #messages.success(request, "Máquinas reiniciadas y datos de simulación limpiados")
            return redirect('main')
    else:
        return HttpResponse("No posees permisos suficientes para realizar esta accion")
        #return render(request, 'app/reiniciar.html')

@login_required
def inicio(request):
    #return render(request, 'app/inicio.html')
    return redirect('login')

def custom_logout(request):
    logout(request)
    return redirect('login')

@login_required
def vista(request):
    user_groups = request.user.groups.values_list('name', flat=True)
    if 'engineer' in user_groups:
        filtro = request.GET.get('filtro', '')

        # Aplicar filtros según el valor seleccionado
        if filtro == 'machine':
            registros = Registro.objects.filter(type_comp='machine')
        elif filtro == 'Source':
            registros = Registro.objects.filter(type_comp='Source')
        elif filtro == 'machine_01':
            registros = Registro.objects.filter(name='machine 01')
        elif filtro == 'machine_02':
            registros = Registro.objects.filter(name='machine 02')
        elif filtro == 'machine_03':
            registros = Registro.objects.filter(name='machine 03')
        elif filtro == 'machine_04':
            registros = Registro.objects.filter(name='machine 04')
        else:
            registros = Registro.objects.all()  # Mostrar todos si no hay filtro

        # Paginación: 15 registros por página
        paginator = Paginator(registros, 15)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'app/listar_registros.html', {'page_obj': page_obj, 'filtro': filtro})

    return render(request, 'app/access_denied.html', status=403)

@login_required
def make_revision(request):
    user_groups = request.user.groups.values_list('name', flat=True)
    if 'engineer' in user_groups:
        # Filtrar los registros que sean de tipo "machine" y con potencia activa en el rango deseado
        registros = Registro.objects.filter(
            Q(type_comp="machine") & 
            (Q(active_power__gte=120) | Q(active_power__lte=20)) & 
            (Q(description__exact=None)|Q(description__exact="") | Q(description__regex=r'^\s*$')|Q(description__exact="None"))

        )
        if request.method == 'POST':
            for registro in registros:
                descripcion = request.POST.get(f'description_{registro.id}', '').strip()
                if descripcion and descripcion != "None" and descripcion!= "":  # Actualizar solo si hay una descripción válida
                    registro.description = descripcion
                    registro.hora_revision= dt.datetime.now()
                    registro.save()

                    # Crear una nueva instancia en el modelo Revision
                    Revision.objects.create(
                            name=registro.name,
                            observation=descripcion,
                            hora=dt.datetime.now(),
                            hecho=False
                    )

            messages.success(request, "Descripciones actualizadas correctamente")
            return redirect('revision')
        
        # Paginación
        paginator = Paginator(registros, 15)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'app/make_revision.html', {'page_obj': page_obj})

    return render(request, 'app/access_denied.html', status=403)

@login_required
def work(request):
    user_groups = request.user.groups.values_list('name', flat=True)
    
    if 'tecnician' not in user_groups:
        return HttpResponse("Acceso denegado", status=403)

    if request.method == 'POST':
        tarea_id = request.POST.get('tarea_id')
        if tarea_id:
            Revision.objects.filter(id=tarea_id).update(hecho=True,hora_hecho=dt.datetime.now())
            messages.success(request, "Tarea marcada como completada.")

    registro = Revision.objects.filter(hecho=False)
    paginator = Paginator(registro, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'app/tareas.html', {'page_obj': page_obj})

@login_required
def sup_engineer(request):
    user_groups = request.user.groups.values_list('name', flat=True)
    
    if 'supervisor' not in user_groups:
        return HttpResponse("Acceso denegado", status=403)
    
    filtro = request.GET.get('filtro', '')

    if filtro == "todas":
        registros = Registro.objects.filter(
            Q(type_comp="machine") & 
            (Q(active_power__gte=120) | Q(active_power__lte=20)))
    elif filtro == "sin hacer":
        registros = Registro.objects.filter(Q(type_comp="machine")&
            (Q(active_power__gte=120) | Q(active_power__lte=20))&
            (Q(description__exact=None)|Q(description__exact="") | Q(description__regex=r'^\s*$')|Q(description__exact="None")))
    elif filtro=="hechas":
        registros = Registro.objects.filter(
            Q(type_comp="machine") &
            (Q(active_power__gte=120) | Q(active_power__lte=20)) &
            ~Q(description__exact=None) &
            ~Q(description__exact="") &
            ~Q(description__exact="None") &
            ~Q(description__regex=r'^\s*$')  # Excluye las cadenas vacías y espacios en blanco
        )
    else:
        registros = Registro.objects.none()
    
    paginator = Paginator(registros, 10)  # Mostrar 10 registros por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    return render(request, 'app/sup_engineer.html', {'page_obj': page_obj, 'filtro': filtro})

@login_required
def sup_tecnician(request):
    user_groups = request.user.groups.values_list('name', flat=True)
    
    if 'supervisor' not in user_groups:
        return HttpResponse("Acceso denegado", status=403)
    
    filtro = request.GET.get('filtro', '')  # Captura el filtro desde el GET
    if filtro == 'All':
        registros = Revision.objects.all()
    elif filtro == 'Sin hacer':
        registros = Revision.objects.filter(hecho=False)
    elif filtro == 'Hechas':
        registros = Revision.objects.filter(hecho=True)
    else:
        registros = Revision.objects.all()  # Cambié a mostrar todo como fallback

    paginator = Paginator(registros, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'app/sup_tecnician.html', {'page_obj': page_obj, 'filtro': filtro})

