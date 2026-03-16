from django.shortcuts import render, redirect
from django.db.models import Q
# Import json response
from django.http import JsonResponse
# Import dashboad models
from dashboard.models import SesionControl
# Importing coop info models
from coop_info.models import IdentifyInformation
# Importing Services model
from .models import GcsServices
# Importing forms
from .forms import *
# Import Django decorators
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
# Import . forms
from .forms import CreateUserForm


# Create your views here.

# Template error 404
def error404template(request):
    return render(request, "temp_error/404_error.html")


# Template error 500
def error500template(request):
    return render(request, "temp_error/500_error.html")


# Home view
def gcs_home(request):
    services_instance = GcsServices.objects.filter(
        Q(status=1)
    )
    return render(request, "home.html", {'services': services_instance})


# Filosofy view
def filosofy(request):
    return render(request, "filosofy.html")


# Magazine view
def magazine(request):
    return render(request, "magazine.html")


# Process view
def process(request):
    return render(request, "process.html")


# Contact view
def contact(request):
    # Obtenemos el formulario
    form = UserContactForm()
    # Validamos si envía un POST
    if request.method == 'POST':
        # Ingresamos info al formulario
        form = UserContactForm(request.POST)
        # Validamos el formulario
        if form.is_valid():
            # Guardamos y redireccionamos
            form.save()
            return redirect('message_ok')
    return render(request, "contact.html")


# Message ok view
def message_ok(request):
    return render(request, "message_ok.html")


# Working view
def working(request):
    return render(request, "construccion.html")

    # Benefits view


def benefits(request):
    return render(request, "benefits.html")


# Social security view
def social_security(request):
    return render(request, "social_security.html")


# Modality 40 view
def modality_40(request):
    return render(request, "modality_40.html")


# Pension view
def pension_97(request):
    return render(request, "pension_97.html")


# Promoter view
def promoter(request):
    return render(request, "promoter.html")


# Related videos view
def related_videos(request):
    return render(request, "related_videos.html")


# Create sesion control function
def sesion_control(id_user):
    # Obtenemos la instancia de usuario
    user = User.objects.get(id=id_user)
    # Validamos que no exista un registro
    validate_data = SesionControl.objects.values().filter(
        Q(user=user)
    )
    # Si el registro no existe
    if len(validate_data) == 0:
        # Creamos el registro
        session_control_id = SesionControl.objects.create(
            sesion='1',
            user=user
        )
    # Si el registro ya existe
    else:
        # Lo modificamos
        session_control_id = SesionControl.objects.filter(
            Q(user=user)
        ).update(
            sesion='1',
            user=user
        )


# Pre-register view
@csrf_exempt
def pre_register(request):
    # Creamos el formulario vacio
    form = CreateUserForm()

    # Obtenemos la respuesta del ajax
    if 'action' in request.POST:
        data = []
        validate_user = User.objects.values().filter(
            Q(username=request.POST['nss'])
        )
        # Primero validamos si existe
        if validate_user:
            # Validamos que tenga registro en identificacion de usuario
            user = User.objects.get(username=request.POST['nss'])
            validate_identify = IdentifyInformation.objects.filter(
                Q(user=user)
            )
            if not validate_identify:
                data.append({'exist': 1, 'not_complete': 1, 'id_user': user.id})
            data.append({'exist': 1})
        return JsonResponse(data, safe=False)
    # Si recibe un formulario POST
    if request.method == 'POST':
        # Ingresamos la información al formulario
        form = CreateUserForm(request.POST)
        # Si el formulario es valido
        if form.is_valid():
            form.save()
            # Obtenemos username del input del formulario
            queryset_name = request.POST.get("username")
            # Hacemos la busqueda del usuario por el username
            user = User.objects.values().filter(
                Q(username=queryset_name)
            )
            # Si existe, obtenemos el ID y lo mandamos como parametro
            if user:
                for data in user:
                    user_id = data['id']
                # Creamos registro de sesion de usuasrio
                sesion_control(user_id)
                # Cambiamos status de user
                user_model_id = User.objects.filter(
                    id=user_id
                ).update(
                    is_active=0
                )
                return redirect('general_info', user_id)
            # Si no existe, regresamos a crear usuarios
            else:
                return redirect('create_user')
    return render(request, "pre-register.html")


# Preregister success
def pre_register_success(request):
    return render(request, "pre_success.html")


# Gcs-Arquitectos temporal
def gcs_arquitectos(request):
    return render(request, "gcs-arquitectos/arquitectos.html")
