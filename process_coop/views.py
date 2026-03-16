import datetime
import pdb
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
# Importing Q
from django.db.models import Q
# Importing Forms
import pre_register.views
from .forms import *
# Import json response
from django.http import JsonResponse
# Import dashboad models
from dashboard.models import SesionControl, CeosRegisterList, PromotersRegisterList
# Importing coop info models
from coop_info.models import IdentifyInformation, GeneralInformation, NumberContact, UserAddressProcess, \
    CotizacionImss, CotImssRelation, EconomicDependents, PersonalReferences, DataBnkRec, EconomicActivity, \
    AlternativeEmails, DocumentationUser
# Importing catalogues
from catalogues.models import UserType, AffiliateType, AffiliationReason, StatusReason, StatusUser, LocationCatalogue, \
    StatusImss, PaymentImss, ActivityType, Status, OfficesList, UserType, CeoListStatus
# Pre register views
from pre_register.views import add_promoters_list

# Import timezone
import pytz
from django.utils import timezone

# PDF Libraries
import os
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa


# Create your views here.


# Create sesion control function
def sesion_control(id_user, session_number):
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
            sesion=str(session_number),
            user=user
        )
    # Si el registro ya existe
    else:
        # Lo modificamos
        session_control_id = SesionControl.objects.filter(
            Q(user=user)
        ).update(
            sesion=str(session_number),
            user=user
        )


# Create user view
@login_required()
@csrf_exempt
def create_user(request):
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

            # TMP
            for data in user:
                user_id = data['id']
            # Creamos registro de sesion de usuasrio
            sesion_control(user_id, 1)
            return redirect('identify_info', user_id)
    return render(request, "process_coop/create_user.html", {'form': form})


# Update User view
@login_required()
def update_user(request, id_user):
    # Instancia de usuario
    instancia = User.objects.get(id=id_user)
    # Creamos un form con la instancia
    form = UpdateUserForm(instance=instancia)
    # Si se envia un POST
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=instancia)
        # Validamos el form
        if form.is_valid():
            instancia = form.save(commit=False)
            instancia.save()
            return redirect('dashboard')
    return render(request, "process_coop/update_user.html", {'form': form})


# Identify user info
@login_required()
def identify_info(request, id_user):
    # Obtenemos los datos del logeado
    user_login = IdentifyInformation.objects.get(user=request.user)
    # Creamos un formulario vacio
    form = IdentifyInforForm()
    # Si recibe un formulario POST
    if request.method == 'POST':
        # Obtenemos tipo afiliacion
        affiliate_type = AffiliateType.objects.get(id=request.POST.get("affiliate_type"))
        # Obtenemos motivo afiliacion
        affiliation_reason = AffiliationReason.objects.get(id=request.POST.get("affiliation_reason"))
        # Obtenemos status motivo
        status_reason = StatusReason.objects.get(id=1)
        # Obtenemos el status user
        status_user = StatusUser.objects.get(id=1)
        # Obtememos la instancia del usuario
        user = User.objects.get(id=id_user)
        # Obtenemos el tipo de usuario
        user_type = UserType.objects.get(id=3)
        # Validamos que no exista el registro
        validate_data = IdentifyInformation.objects.values().filter(
            Q(user=user)
        )
        # Si el registro no existe
        if len(validate_data) == 0:
            # Creamos un registro nuevo
            identify_info_id = IdentifyInformation.objects.create(
                ceo=user_login.ceo,
                upstream_promoter=request.user.username,
                affiliate_type=affiliate_type,
                affiliation_reason=affiliation_reason,
                offices_list=user_login.offices_list,
                status_reason=status_reason,
                status_user=status_user,
                user=user,
                user_type=user_type
            )
        # Si ya existe, lo modificamos
        else:
            identify_info_id = IdentifyInformation.objects.filter(
                Q(user=user)
            ).update(
                ceo=user_login.ceo,
                upstream_promoter=user_login.upstream_promoter,
                affiliate_type=affiliate_type,
                affiliation_reason=affiliation_reason,
                offices_list=user_login.offices_list,
                status_reason=status_reason,
                status_user=status_user,
                user=user,
                user_type=user_type
            )
        if GeneralInformation.objects.filter(user=id_user):
            return redirect('dashboard')
        else:
            return redirect('general_info', id_user)
    return render(request, "process_coop/identify.html", {'form': form, 'user_login': user_login})


# Crear registro en listado de directores
def create_ceo_register(ceo_id, status):
    validate = bool

    try:
        # Obtenemos la instancia del usuario
        user = User.objects.get(id=ceo_id)
        # Obtenemos el estatus
        status = CeoListStatus.objects.get(id=status)

        # Validamos si el registro existe
        if not CeosRegisterList.objects.filter(user=user):
            # Creamos el registro
            ceo_list_id = CeosRegisterList.objects.create(
                user=user,
                status=status
            )
        else:
            # Modificamos el registro
            ceo_list_id = CeosRegisterList.objects.filter(user=user).update(
                status=status
            )
        validate = True

    except:
        validate = False

    return validate


# Update identify information
@login_required()
def update_identify_info(request, id_user):
    # Obtenemos los datos del logeado
    user_login = IdentifyInformation.objects.get(user=request.user)

    # Validamos si es super usuario
    is_superuser = False
    if user_login.user_type.user_type == 'Super usuario':
        is_superuser = True

    # Instancia de usuario
    instancia = IdentifyInformation.objects.get(user=id_user)

    # Obtenemos la lista de los directores
    ceo_list = CeosRegisterList.objects.filter(status=1).exclude(user=instancia.ceo.user)

    # Creamos el formulario de Identify
    form = UpdateIdentifyInforForm(instance=instancia)

    if request.method == 'POST':
        if is_superuser:
            # Validamos si se cambió  a director
            if request.POST.get('is_director') == 'on':
                # Obtenemos el tipo de usuario director
                user_type = UserType.objects.get(id=1)
                # Hacemos staff
                user_id = User.objects.filter(id=id_user).update(is_staff=True)
                # Creamos el registro en el listado
                create_ceo_register(instancia.user.id, 1)
            else:
                # Obtenemos el tipo de usuario socio comercial
                user_type = UserType.objects.get(id=3)
                # Quitamos los permisos de staff
                user_id = User.objects.filter(id=id_user).update(is_staff=False)
                # Creamos el registro en el listado
                create_ceo_register(instancia.user.id, 2)

        form = UpdateIdentifyInforForm(request.POST, instance=instancia)

        if form.is_valid():
            instancia = form.save(commit=False)
            if is_superuser:
                instancia.user_type = user_type
            instancia.save()

            return redirect('dashboard')

    return render(request, "process_coop/update_identify.html",
                  {'user_login': user_login, 'form': form, 'is_superuser': is_superuser, 'instancia': instancia,
                   'ceo_list': ceo_list})


# General info view
@login_required()
def general_info(request, id_user):
    # Validamos si es un pre-registro
    val_preregister = IdentifyInformation.objects.filter(
        Q(user=id_user)
    )
    # Obtenemos instancia del usuario
    user = User.objects.get(id=id_user)
    # Creamos formulario vacio
    form = GeneralInfoForm()
    # Colocamos un dato por default en el select
    form.fields['nationality'].initial = 73
    # Si recibe un formulario POST
    if request.method == 'POST':
        form = GeneralInfoForm(request.POST)
        # Validamos que el formulario sea valido
        if form.is_valid():
            form.save()
            if UserAddressProcess.objects.filter(user=id_user):
                return redirect('dashboard')
            else:
                return redirect('address_registration', id_user)
    return render(request, "process_coop/general_info.html",
                  {'user': user, 'form': form, 'val_preregister': val_preregister})


# Update general info
@login_required()
def update_general_info(request, id_user):
    instancia = GeneralInformation.objects.get(user=id_user)
    form = UpdateGeneralInfoForm(instance=instancia)
    if request.method == 'POST':
        form = UpdateGeneralInfoForm(request.POST, instance=instancia)
        if form.is_valid():
            instancia = form.save(commit=False)
            instancia.save()
            return redirect('dashboard')
    return render(request, "process_coop/update_general.html", {'form': form, 'instancia': instancia})


# Address registration
@login_required()
@csrf_exempt
def address_registration(request, id_user):
    # Validamos si es un pre-registro
    val_preregister = IdentifyInformation.objects.filter(
        Q(user=id_user)
    )
    # Obtenemos instancia del usuario
    user = User.objects.get(id=id_user)
    # Creamos un formulario vacio
    form = UserAddressForm()
    # Obtenemos el action del form
    if 'action' in request.POST:
        data = []
        for i in LocationCatalogue.objects.filter(zip_code=request.POST['zip_code']):
            data.append({'id': i.id, 'suburb': i.suburb})
        return JsonResponse(data, safe=False)
    if 'action_info' in request.POST:
        data_del = []
        for i_del in LocationCatalogue.objects.filter(id=request.POST['suburb']):
            data_del.append({'id': i_del.id, 'delegation': i_del.delegation, 'state': i_del.state})
        return JsonResponse(data_del, safe=False)
    # Validamos si es un POST
    if request.method == 'POST':
        # Obtenemos la calle
        street = request.POST.get("street")
        # Obtenemos el num int
        int_number = request.POST.get("int_number")
        # Obtenemos el num ext
        ext_number = request.POST.get("ext_number")
        # Obtenemos una instancia del usuario
        user = User.objects.get(id=id_user)
        # Obtenemos la colonia
        suburb = LocationCatalogue.objects.get(id=request.POST.get("suburb"))
        # Validamos que no exista el registro
        validate_data = UserAddressProcess.objects.values().filter(
            Q(user=user)
        )
        # Si el registro no existe
        if len(validate_data) == 0:
            # Creamos un registro nuevo
            user_address_id = UserAddressProcess.objects.create(
                street=street,
                int_number=int_number,
                ext_number=ext_number,
                suburb=suburb,
                user=user
            )
        # Si ya existe
        else:
            # Actualizamos el registro
            user_address_id = UserAddressProcess.objects.filter(
                Q(user=user)
            ).update(
                street=street,
                int_number=int_number,
                ext_number=ext_number,
                suburb=suburb,
                user=user
            )
        if NumberContact.objects.filter(user=id_user):
            return redirect('dashboard')
        else:
            return redirect('numbers_registration', id_user)
    return render(request, "process_coop/address.html",
                  {'user': user, 'form': form, 'val_preregister': val_preregister})


# Update Address
@login_required()
@csrf_exempt
def update_address(request, id_user):
    # Obtenemos la instancia del usuario
    user = User.objects.get(id=id_user)
    # Obtenemos los datos actuales del usuario
    current_address = UserAddressProcess.objects.filter(
        Q(user=user)
    )
    # Creamos un formulario vacio
    form = UpdateUserAddressForm()
    # Obtenemos el action del select del form
    if 'action' in request.POST:
        data = []
        for i in LocationCatalogue.objects.filter(zip_code=request.POST['zip_code']):
            data.append({'id': i.id, 'suburb': i.suburb})
        return JsonResponse(data, safe=False)
    if 'action_info' in request.POST:
        data_del = []
        for i_del in LocationCatalogue.objects.filter(id=request.POST['suburb']):
            data_del.append({'id': i_del.id, 'delegation': i_del.delegation, 'state': i_del.state})
        return JsonResponse(data_del, safe=False)
    # Validamos si es un POST
    if request.method == 'POST':
        # Obtenemos la calle
        street = request.POST.get("street")
        # Obtenemos el num int
        int_number = request.POST.get("int_number")
        # Obtenemos el num ext
        ext_number = request.POST.get("ext_number")
        # Obtenemos la colonia
        suburb = LocationCatalogue.objects.get(id=request.POST.get("suburb"))
        # Validamos que no exista el registro
        validate_data = UserAddressProcess.objects.values().filter(
            Q(user=user)
        )
        # Si el registro no existe
        if len(validate_data) == 0:
            # Creamos un registro nuevo
            user_address_id = UserAddressProcess.objects.create(
                street=street,
                int_number=int_number,
                ext_number=ext_number,
                suburb=suburb,
                user=user
            )
        # Si ya existe
        else:
            # Actualizamos el registro
            user_address_id = UserAddressProcess.objects.filter(
                Q(user=user)
            ).update(
                street=street,
                int_number=int_number,
                ext_number=ext_number,
                suburb=suburb,
                user=user
            )
            return redirect('dashboard')
    return render(request, "process_coop/update_address.html", {'current_address': current_address, 'form': form})


# Numbers reigstration
@login_required()
def numbers_registration(request, id_user):
    # Validamos si es un pre-registro
    val_preregister = IdentifyInformation.objects.filter(
        Q(user=id_user)
    )
    # Obtenemos instancia del usuario
    user = User.objects.get(id=id_user)
    # Creamos un formulario vacio
    form = ContactNumberForm()
    # Obtenemos los telefonos registrados
    user_number = NumberContact.objects.filter(
        Q(user=id_user)
    )
    # Si se envía un POST
    if request.method == 'POST':
        form = ContactNumberForm(request.POST)
        # Validamos el form
        if form.is_valid():
            form.save()
    return render(request, "process_coop/numbers.html",
                  {'user_num': user_number, 'user': user, 'form': form, 'val_preregister': val_preregister})


# Matrix number registration
@login_required()
def m_number_registration(request, id_user):
    # Obtenemos instancia del usuario
    user = User.objects.get(id=id_user)
    # Obtenemos la información actual
    current_numbers = NumberContact.objects.filter(
        Q(user=user)
    )
    # Creamos el form para crear otro contacto
    form = ContactNumberForm()
    # Si se envía un POST
    if request.method == 'POST':
        form = ContactNumberForm(request.POST)
        # Validamos el form
        if form.is_valid():
            form.save()
    return render(request, "process_coop/m_update_numbers.html",
                  {'current_numbers': current_numbers, 'form': form, 'user': user})


# Update numbers
@login_required()
def update_number_registration(request, id_number):
    # Creamos el form con la instancia
    instancia = NumberContact.objects.filter(
        Q(id=id_number)
    )
    for instancia in instancia:
        form = UpdateContactNumberForm(instance=instancia)
    # Si se envía un POST
    if request.method == 'POST':
        form = UpdateContactNumberForm(request.POST, instance=instancia)
        if form.is_valid():
            instancia = form.save(commit=False)
            instancia.save()
            return redirect('dashboard')
    return render(request, "process_coop/update_numbers.html", {'form': form})


# Alternative emails
@login_required()
def alternative_emails(request, id_user):
    # Validamos si no existe un proceso adelante
    val_data = CotImssRelation.objects.filter(user=id_user)
    # Obtenemos instancia del usuario
    user = User.objects.get(id=id_user)
    # Creamos un form vacio
    form = AlternativeEmailForm()
    # Si envía un POST
    if request.method == 'POST':
        form = AlternativeEmailForm(request.POST)
        # Validamos el form
        if form.is_valid():
            form.save()
            if val_data:
                return redirect('dashboard')
            else:
                return redirect('imss_info', id_user)
    return render(request, "process_coop/alternative_emails.html", {'user': user, 'form': form, 'val_data': val_data})


# Update alternative emails
@login_required()
def update_alternative_emails(request, id_user):
    # Creamos el form con la instancia
    instancia = AlternativeEmails.objects.get(user=id_user)
    form = UpdateAlternativeEmailForm(instance=instancia)
    # Si envía un POST
    if request.method == 'POST':
        form = UpdateAlternativeEmailForm(request.POST, instance=instancia)
        if form.is_valid():
            instancia = form.save(commit=False)
            instancia.save()
            return redirect('dashboard')
    return render(request, "process_coop/update_alternative_email.html", {'form': form})


# IMSS relacion function
def imss_rel_func(request, id_user, id_imss):
    # Obtenemos la instancia del usuario
    user = User.objects.get(id=id_user)
    # Obtenemos la instancia del imss
    imss = CotizacionImss.objects.get(id=id_imss)
    # Obtenemos la instancia del status_imss
    status_imss = StatusImss.objects.get(id=1)
    # Validamos que no exista el registro
    validate_data = CotImssRelation.objects.values().filter(
        Q(user=user)
    )
    # Si el registro no existe
    if len(validate_data) == 0:
        # Creamos un registro
        cot_imss_id = CotImssRelation.objects.create(
            imss_register_date=request.POST.get("imss_register_date"),
            coti_weeks=request.POST.get("coti_weeks"),
            cotizacion_imss=imss,
            status_imss=status_imss,
            user=user
        )
    # Si existe
    else:
        # Lo modificamos
        cot_imss_id = CotImssRelation.objects.filter(
            Q(user=user)
        ).update(
            imss_register_date=request.POST.get("imss_register_date"),
            coti_weeks=request.POST.get("coti_weeks"),
            cotizacion_imss=imss,
            status_imss=status_imss,
            user=user
        )


# IMSS
@login_required()
def imss_info(request, id_user):
    # Validamos si es un pre-registro
    val_preregister = IdentifyInformation.objects.filter(
        Q(user=id_user)
    )
    user = User.objects.get(id=id_user)
    # Hacemos un formulario vacio
    form = CotIMSForm()
    # Si envía un POST
    if request.method == 'POST':
        form = CotIMSForm(request.POST)
        # Validamos el form
        if form.is_valid():
            ob_form = form.save()
            imss_rel_func(request, id_user, ob_form.id)
            if EconomicActivity.objects.filter(user=id_user):
                return redirect('dashboard')
            else:
                return redirect('economic_act', id_user)
    return render(request, "process_coop/imss.html", {'user': user, 'form': form, 'val_preregister': val_preregister})


# Update IMSS
@login_required()
def update_imss_info(request, id_user):
    # Creamos el form con la instancia
    instancia = CotImssRelation.objects.filter(user=id_user)
    for instancia in instancia:
        instancia_imss = CotizacionImss.objects.get(id=instancia.cotizacion_imss.id)
    form = UpdateCotIMSForm(instance=instancia_imss)
    # Si se envia un POST
    if request.method == 'POST':
        form = UpdateCotIMSForm(request.POST, instance=instancia_imss)
        if form.is_valid():
            instancia_imss = form.save(commit=False)
            instancia_imss.save()
            imss_rel_func(request, id_user, instancia.cotizacion_imss.id)
            return redirect('dashboard')
    return render(request, "process_coop/update_imss.html", {'form': form, 'instancia': instancia})


# Economic Activities
@login_required()
@csrf_exempt
def economic_act(request, id_user):
    # Validamos si es un pre-registro
    val_preregister = IdentifyInformation.objects.filter(
        Q(user=id_user)
    )
    # Obtenemos la instancia del usuario
    user = User.objects.get(id=id_user)
    # Obtengo las actividades de mi usuario
    act_register = EconomicActivity.objects.filter(
        Q(user=user)
    )
    # Creamos un form vacio
    form = EconomicActForm()
    # Obtenemos el action del form
    if 'action' in request.POST:
        data_act = []
        for i_act in ActivityType.objects.filter(type=request.POST['activity']):
            data_act.append({'id': i_act.id, 'activity_description': i_act.activity_description})
        return JsonResponse(data_act, safe=False)
    # Si envía un POST
    if request.method == 'POST':
        # Obtenemos el tipo de actividad
        activity = request.POST.get("activity")
        # Obtengo la descripción
        activity_description = request.POST.get("activity_description")
        # Obtengo la actividad
        activity_type = ActivityType.objects.get(id=request.POST.get("activity_type"))
        # Si no existe creamos un registro
        economic_activity_id = EconomicActivity.objects.create(
            activity=activity,
            activity_description=activity_description,
            activity_type=activity_type,
            user=user
        )
    return render(request, "process_coop/economic_act.html",
                  {'form': form, 'user': user, 'act_register': act_register, 'val_preregister': val_preregister})


# Matrix Economic Activities
@login_required()
@csrf_exempt
def m_economic_activity(request, id_user):
    # Obtenemos instancia del usuario
    user = User.objects.get(id=id_user)
    # Obtenemos la información actual
    current_eco_act = EconomicActivity.objects.filter(
        Q(user=user)
    )
    # Creamos un form vacio
    form = EconomicActForm()
    # Obtenemos el action del form
    if 'action' in request.POST:
        data_act = []
        for i_act in ActivityType.objects.filter(type=request.POST['activity']):
            data_act.append({'id': i_act.id, 'activity_description': i_act.activity_description})
        return JsonResponse(data_act, safe=False)
    # Si envía un POST
    if request.method == 'POST':
        # Obtenemos el tipo de actividad
        activity = request.POST.get("activity")
        # Obtengo la descripción
        activity_description = request.POST.get("activity_description")
        # Obtengo la actividad
        activity_type = ActivityType.objects.get(id=request.POST.get("activity_type"))
        # Si no existe creamos un registro
        economic_activity_id = EconomicActivity.objects.create(
            activity=activity,
            activity_description=activity_description,
            activity_type=activity_type,
            user=user
        )
    return render(request, "process_coop/m_update_eco_act.html", {'current_eco_act': current_eco_act, 'form': form})


# Update Economic Activities
@login_required()
@csrf_exempt
def update_economic_activity(request, id_act):
    # Obtenemos la información actual
    current_eco_act = EconomicActivity.objects.filter(
        Q(id=id_act)
    )
    # Creamos un form vacio
    form = UpdateEconomicActForm()
    # Obtenemos el action del form
    if 'action' in request.POST:
        data_act = []
        for i_act in ActivityType.objects.filter(type=request.POST['activity']):
            data_act.append({'id': i_act.id, 'activity_description': i_act.activity_description})
        return JsonResponse(data_act, safe=False)
    # Si envía un POST
    if request.method == 'POST':
        # Obtenemos el tipo de actividad
        activity = request.POST.get("activity")
        # Obtengo la descripción
        activity_description = request.POST.get("activity_description")
        # Obtengo la actividad
        activity_type = ActivityType.objects.get(id=request.POST.get("activity_type"))
        # Obtengo el status
        status = Status.objects.get(id=request.POST.get("status"))
        # Si no existe creamos un registro
        economic_activity_id = EconomicActivity.objects.filter(
            Q(id=id_act)
        ).update(
            activity=activity,
            activity_description=activity_description,
            activity_type=activity_type,
            status=status
        )
    return render(request, "process_coop/update_economic_activity.html",
                  {'current_eco_act': current_eco_act, 'form': form})


# Data bnk rec view
@login_required()
def data_bnk_rec(request, id_user):
    # Obtenemos la instancia del usuario
    user = User.objects.get(id=id_user)
    # Obtenemos los dep eco
    ecodep_data = EconomicDependents.objects.filter(user=user)
    # Creamos un form vacio
    form = DataBnkRecForm()
    # Si envía un POST
    if request.method == 'POST':
        form = DataBnkRecForm(request.POST)
        # Validamos el form
        if form.is_valid():
            form.save()
            if EconomicDependents.objects.filter(user=id_user):
                return redirect('dashboard')
            else:
                return redirect('economic_dependent', id_user)
    return render(request, "process_coop/data_bnk_rec.html", {'form': form, 'user': user, 'ecodep_data': ecodep_data})


# Update bnk rec info
@login_required()
def update_bnkrec(request, id_user):
    # Obtenemos usuario
    user = User.objects.get(id=id_user)
    # Obtenemos los datos del usuario
    dnkrec_info = DataBnkRec.objects.filter(
        Q(user=user)
    )
    # Instancia de usuario
    instancia = DataBnkRec.objects.filter(
        Q(user=id_user)
    )
    if instancia:
        for instancia in instancia:
            # Creamos un form con la instancia
            form = UpdateDataBnkRecForm(instance=instancia)
        if request.method == 'POST':
            form = UpdateDataBnkRecForm(request.POST, instance=instancia)
            # Validamos el form
            if form.is_valid():
                instancia = form.save(commit=False)
                instancia.save()
                return redirect('dashboard')
    else:
        form = UpdateDataBnkRecForm()
        # Si se envia un POST
        if request.method == 'POST':
            form = UpdateDataBnkRecForm(request.POST)
            # Validamos el form
            if form.is_valid():
                form.save()
                return redirect('dashboard')
    return render(request, "process_coop/update_bnkrec.html", {'form': form, 'user': user, 'dnkrec_info': dnkrec_info})


# Economic dependent view
@login_required()
def economic_dependent(request, id_user):
    # Obtenemos la instancia del usuario
    user = User.objects.get(id=id_user)
    # Creamos un formulario vacio
    form = EconomicDependentForm()
    # Obtenemos los registros del usuario
    depen_data = EconomicDependents.objects.filter(
        Q(user=user)
    )
    # Obtenemos las referencias personales
    ref_data = PersonalReferences.objects.filter(user=id_user)
    # Si envia un POST
    if request.method == 'POST':
        form = EconomicDependentForm(request.POST)
        # Validamos el form
        if form.is_valid():
            form.save()
    return render(request, "process_coop/economic_depen.html",
                  {'form': form, 'user': user, 'depen_data': depen_data, 'ref_data': ref_data})


# Matriz economic dependents
@login_required()
def m_economic_dependent(request, id_user):
    # Obtenemos instancia del usuario
    user = User.objects.get(id=id_user)
    # Obtenemos la información actual
    current_eco_dep = EconomicDependents.objects.filter(
        Q(user=user)
    )
    # Creamos un formulario vacio
    form = EconomicDependentForm()
    # Si envia un POST
    if request.method == 'POST':
        form = EconomicDependentForm(request.POST)
        # Validamos el form
        if form.is_valid():
            form.save()
    return render(request, "process_coop/m_update_eco_dep.html",
                  {'current_eco_dep': current_eco_dep, 'form': form, 'user': user})


# Update economic dependent
@login_required()
def update_economic_dependent(request, id_dep):
    instancia = EconomicDependents.objects.get(id=id_dep)
    # Creamos el formulario con instancia
    form = UpdateEconomicDependentForm(instance=instancia)
    # Si envia POST
    if request.method == 'POST':
        form = UpdateEconomicDependentForm(request.POST, instance=instancia)
        if form.is_valid():
            instancia = form.save(commit=False)
            instancia.save()
            return redirect('dashboard')
    return render(request, "process_coop/update_economic_depen.html", {'form': form, 'instancia': instancia})


# Personal references view
@login_required()
def personal_references(request, id_user):
    # Validamos si es un pre-registro
    val_preregister = IdentifyInformation.objects.filter(
        Q(user=id_user)
    )
    # Obtenemos la instancia del usuario
    user = User.objects.get(id=id_user)
    # Creamos un form vacio
    form = PersonalRefForm()
    # Obtenemos las referencias del usuario
    ref_data = PersonalReferences.objects.filter(
        Q(user=user)
    )
    # Obtenemos información de contratos
    contract_data = "" + str(user.id) + "_" + str(user.username) + "_contratocooperativista.pdf"
    val_contract = 0
    import os.path as path
    if path.exists('media/empty_contracts/' + contract_data):
        val_contract = 1
    else:
        val_contract = 0
    # Si envia un POST
    if request.method == 'POST':
        form = PersonalRefForm(request.POST)
        # Validamos el form
        if form.is_valid():
            form.save()
    return render(request, "process_coop/personal_ref.html",
                  {'form': form, 'user': user, 'ref_data': ref_data, 'val_contract': val_contract,
                   'val_preregister': val_preregister})


# Matrix personal references
@login_required()
def m_update_references(request, id_user):
    # Obtenemos la instancia del usuario
    user = User.objects.get(id=id_user)
    # Creamos un form vacio
    form = PersonalRefForm()
    # Obtenemos las referencias del usuario
    ref_data = PersonalReferences.objects.filter(
        Q(user=user)
    )
    # Si envia un POST
    if request.method == 'POST':
        form = PersonalRefForm(request.POST)
        # Validamos el form
        if form.is_valid():
            form.save()
    return render(request, "process_coop/m_update_ref.html", {'form': form, 'user': user, 'ref_data': ref_data})


# Update personal references
@login_required()
def update_personal_references(request, id_ref):
    # Obtenemos la instancia
    instancia = PersonalReferences.objects.get(id=id_ref)
    # Creamos el form con la instancia
    form = UpdatePersonalRefForm(instance=instancia)
    if request.method == 'POST':
        form = UpdatePersonalRefForm(request.POST, instance=instancia)
        if form.is_valid():
            instancia = form.save(commit=False)
            instancia.save()
            return redirect('dashboard')
    return render(request, "process_coop/update_personal_ref.html", {'form': form})


# Pasamos la fecha a local
def convert_to_localtime(utctime):
    fmt = '%d/%m/%Y'
    utc = utctime.replace(tzinfo=pytz.UTC)
    localtz = utc.astimezone(timezone.get_current_timezone())
    return localtz.strftime(fmt)


# Create coop card function
def create_coop_card(id_user):
    # Import lab library
    from reportlab.pdfgen import canvas

    # Obtenemos los datos del usuario
    user = User.objects.get(id=id_user)
    gen_info = GeneralInformation.objects.get(user=id_user)

    # PDF Content
    filename = "" + str(user.id) + "_" + user.username + "_credencial_socio.pdf"
    documenttitle = 'Tarjeta de cooperativista'
    image = 'static/img/logo_card.jpg'
    title = 'GCS Protección y Beneficio Familiar S.C.C.'
    subtitle = 'Empoderando tu futuro.'
    label = 'Tarjeta de identificación'
    first_name = 'Nombre(s):'
    first_name_r = user.first_name
    last_name = 'Apellidos:'
    last_name_r = user.last_name
    puesto = 'Puesto:'
    puesto_r = 'Promotor GCS-Coop'
    actividad = 'Actividad:'
    actividad_r = 'Incorporar a nuevos socios a la empresa'
    nss = 'Número IMSS:'
    nss_r = user.username
    curp = 'CURP:'
    curp_r = gen_info.curp
    date = 'Fecha de alta:'
    date_r = '' + str(convert_to_localtime(user.date_joined))
    site = 'gcs-coop.com.mx'
    tel = '55 5379 4972'
    firma = 'Firma del socio'
    footer = 'Ante cualquier trámite con IMSS o INFONAVIT presentar esta'
    footer_2 = 'identificación'
    tel_img = 'static/img/site_card.png'
    site_img = 'static/img/tel_card.png'
    title_back = 'GCS Protección y Beneficio Familiar SCC'
    subtitle_back = 'Alta en clínica del IMSS'
    p_1 = '1. Identifica la Clínica del IMSS que te corresponde.'
    p_2 = '2. Presentarse de lunes a viernes de 08:00 a 19:30 horas.'
    p_3 = '3. Presentar la siguiente documentación de todos los que se vayan'
    p_3_p = 'a registrar:'
    r1 = 'a) Identificación Oficial, NSS, CURP, Fotografía Infantil, Comprobante'
    r2 = 'de Domicilio, Acta de Nacimiento (Concubina, Hijos, Padres) y Acta'
    r3 = 'de Matrimonio (Esposa).'
    r4 = 'b) Para Cualquier duda o comentario comunícate al 800 623 2323'
    r5 = 'Ó ingresa a la página http://www.imss.gob.mx/tramites/registro-umf'
    footer_back = 'Descarga la Aplicación Digital del IMSS y facilita'
    footer_back_2 = 'todos tus procesos.'
    qr_image = 'static/img/qr_back.jpg'

    # Creamos el archivo
    pdf = canvas.Canvas('media/empty_contracts/' + filename)
    pdf.setTitle(documenttitle)

    # Colocamos el logo de la tarjeta
    pdf.drawInlineImage(image, 20, 775)

    # Colocamos el titulo
    # Register a new font
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfbase import pdfmetrics
    pdfmetrics.registerFont(
        TTFont('big_caslon', 'static/font/big-caslon/big-caslon.ttf')
    )

    # Hacemos marco de la card
    pdf.line(15, 800, 405, 800)
    pdf.line(15, 800, 15, 620)
    pdf.line(15, 620, 405, 620)
    pdf.line(405, 620, 405, 800)

    # Colocamos el titulo
    # Set the current font
    pdf.setFont('Helvetica', 8)
    pdf.drawString(50, 785, title)
    pdf.drawString(75, 775, subtitle)

    # Set the current font
    pdf.setFont('Helvetica', 7)
    # Colocamos los datos de la tarjeta
    pdf.drawString(20, 760, label)
    pdf.line(20, 757, 90, 757)

    # Set the current font
    pdf.setFont('Helvetica', 5)
    pdf.drawString(20, 748, first_name)
    # Set the current font
    pdf.setFont('Helvetica', 6)
    pdf.drawString(20, 740, first_name_r)
    # Set the current font
    pdf.setFont('Helvetica', 5)
    pdf.drawString(20, 730, last_name)
    # Set the current font
    pdf.setFont('Helvetica', 6)
    pdf.drawString(20, 722, last_name_r)
    # Set the current font
    pdf.setFont('Helvetica', 5)
    pdf.drawString(20, 712, puesto)
    # Set the current font
    pdf.setFont('Helvetica', 6)
    pdf.drawString(20, 706, puesto_r)
    # Set the current font
    pdf.setFont('Helvetica', 5)
    pdf.drawString(20, 696, actividad)
    # Set the current font
    pdf.setFont('Helvetica', 6)
    pdf.drawString(20, 688, actividad_r)

    # Cuadro interno
    # Set the current font
    pdf.setFont('Helvetica', 5)
    pdf.drawString(120, 748, nss)
    # Set the current font
    pdf.setFont('Helvetica', 6)
    pdf.drawString(120, 740, nss_r)
    # Set the current font
    pdf.setFont('Helvetica', 5)
    pdf.drawString(120, 730, curp)
    # Set the current font
    pdf.setFont('Helvetica', 6)
    pdf.drawString(120, 722, curp_r)
    # Set the current font
    pdf.setFont('Helvetica', 5)
    pdf.drawString(120, 712, date)
    # Set the current font
    pdf.setFont('Helvetica', 6)
    pdf.drawString(120, 706, date_r)
    pdf.line(117, 753, 200, 753)
    pdf.line(117, 753, 117, 702)
    pdf.line(117, 702, 200, 702)
    pdf.line(200, 702, 200, 753)

    # Footer de la card
    # Set the current font
    pdf.setFont('Helvetica', 5)
    pdf.drawString(35, 675, site)
    pdf.setFont('Helvetica', 5)
    pdf.drawString(35, 665, tel)
    pdf.line(165, 680, 205, 680)
    pdf.drawString(170, 675, firma)
    # Set the current font
    pdf.setFont('Helvetica', 6)
    pdf.drawString(30, 650, footer)
    pdf.drawString(100, 640, footer_2)

    # Parte trasera
    pdf.line(210, 780, 210, 635)

    # Set the current font
    pdf.setFont('Helvetica', 8)
    pdf.drawString(240, 785, title_back)

    # Set the current font
    pdf.setFont('Helvetica', 6)
    pdf.drawString(215, 770, subtitle_back)

    # Set the current font
    pdf.setFont('Helvetica', 7)
    pdf.drawString(215, 755, p_1)
    pdf.drawString(215, 745, p_2)
    pdf.setFont('Helvetica', 6.3)
    pdf.drawString(215, 735, p_3)
    pdf.drawString(220, 725, p_3_p)
    # Set the current font
    pdf.setFont('Helvetica', 5.9)
    pdf.drawString(220, 715, r1)
    pdf.drawString(225, 705, r2)
    pdf.drawString(225, 695, r3)
    pdf.drawString(220, 685, r4)
    pdf.drawString(225, 675, r5)

    # Set the current font
    pdf.setFont('Helvetica', 6)
    pdf.drawString(220, 650, footer_back)
    pdf.drawString(260, 640, footer_back_2)
    # Colocamos el QR de la tarjeta
    pdf.drawInlineImage(qr_image, 350, 625)

    # Save the document
    pdf.save()


# Validamos si puede generar contratos
def validate_contract_data(id_user):
    validate_data = False
    if IdentifyInformation.objects.filter(user=id_user):
        if GeneralInformation.objects.filter(user=id_user):
            if UserAddressProcess.objects.filter(user=id_user):
                if NumberContact.objects.filter(user=id_user, status=1):
                    if CotImssRelation.objects.filter(user=id_user):
                        if PersonalReferences.objects.filter(user=id_user, status=1):
                            validate_data = True
    return validate_data


# Creamos los contratos del usuario
def create_user_contracts(id_user):
    # Obtenemos la instancia del usuario y los datos de identificacion
    user = User.objects.get(id=id_user)
    iden_info = IdentifyInformation.objects.get(user=user)
    # Obtenemos datos del promotor
    upstream_name = User.objects.get(username=iden_info.upstream_promoter.user.username)
    # Obtenemos datos generales
    gen_info = GeneralInformation.objects.get(user=user)
    # Obtenemos direccion del usuario
    address_info = UserAddressProcess.objects.get(user=user)
    street_no = "" + address_info.street + ", No ext #" + address_info.ext_number
    if address_info.int_number:
        street_no += ", No int #" + address_info.int_number
    # Obtenemos datos del IMSS
    data_imss = CotImssRelation.objects.get(user=user)
    # Obtenemos los numeros
    numbers_info = NumberContact.objects.filter(
        Q(user=user)
    )
    numbers_list = []
    for number in numbers_info:
        numbers_list.append(str(number.number) + ", tipo " + str(number.number_type))
    # Obtenemos los correos
    email_info = AlternativeEmails.objects.filter(
        Q(user=user)
    )
    email_list = []
    if email_info:
        for email in email_info:
            email_list.append(email.alternative_email)
            email_list.append(user.email)
    else:
        email_list.append(user.email)
    # Obtenemos los dependientes economicos
    dependent_info = EconomicDependents.objects.filter(
        Q(user=user)
    )
    dependent_list = []
    if dependent_info:
        for dependent in dependent_info:
            dependent_dict = {}
            dependent_dict['d_full_name'] = "" + dependent.ape_pat + " " + dependent.ape_mat + " " + dependent.name
            dependent_dict['d_relation'] = dependent.relation
            dependent_dict['d_age'] = str(dependent.age) + " años"
            dependent_list.append(dependent_dict)
    # Obtenemos referencias personales
    references_info = PersonalReferences.objects.filter(
        Q(user=user)
    )
    references_list = []
    if references_info:
        for references in references_info:
            references_dict = {}
            references_dict[
                'r_full_name'] = "" + references.ape_pat_ref + " " + references.ape_mat_ref + " " + references.name_ref
            references_dict['r_number'] = references.num_contact
            references_dict['r_meet'] = references.meet_time
            references_list.append(references_dict)
    # Obtenemos los datos de bnkrec
    bnkrec_info = DataBnkRec.objects.filter(
        Q(user=user)
    )
    bnk_name = ''
    css_number = ''
    css_clave = ''
    account_type = ''
    if bnkrec_info:
        for bnkrec_info in bnkrec_info:
            bnk_name = bnkrec_info.bnk_name
            css_number = bnkrec_info.css_number
            css_clave = bnkrec_info.css_clave
            account_type = bnkrec_info.account_type
    # Creamos el nombre del archivo
    file_name = "" + str(user.id) + "_" + user.username + "_contratocooperativista.pdf"
    # Creamos dict de Contrato cooperativista
    data = dict()
    data['file_name'] = file_name
    data['id'] = user.id
    data['date_joined'] = user.date_joined
    data['upstream'] = upstream_name.get_full_name()
    data['nss'] = iden_info.user
    data['last_name'] = user.last_name
    data['first_name'] = user.first_name
    data['full_name'] = user.get_full_name
    data['age'] = gen_info.coop_age
    data['place_birth'] = gen_info.place_of_birth
    data['date_birth'] = gen_info.date_of_birth
    data['nationality'] = gen_info.nationality
    data['marri_status'] = gen_info.marital_status
    data['curp'] = gen_info.curp
    data['rfc'] = gen_info.rfc
    data['sex'] = gen_info.sex
    data['street_no'] = street_no
    data['suburb'] = address_info.suburb
    data['delegation'] = address_info.suburb.delegation
    data['state'] = address_info.suburb.state
    data['data_imss'] = data_imss.cotizacion_imss.salario_cot.aport_coop
    data['data_imss_letter'] = data_imss.cotizacion_imss.salario_cot.aport_letter
    data['numbers'] = numbers_list
    data['emails'] = email_list
    data['dependents'] = dependent_list
    data['references'] = references_list
    data['bank'] = bnk_name
    if css_number != None:
        data['account'] = css_number
    if css_clave != None:
        data['clave'] = css_clave
    data['type'] = account_type

    # Creamos una sola cadena con toda la direccion
    address_full = "" + data['street_no'] + ", " + str(data['suburb'])
    address_full_2 = "" + str(data['delegation']) + ", " + str(data['state'])
    # Creamos el nombre del archivo
    file_ind_name = "" + str(user.id) + "_" + user.username + "_contratocoindustrial.pdf"
    # Creamoos dict de Contrato Industrial
    data_ind = dict()
    data_ind['full_name'] = user.get_full_name
    data_ind['full_address'] = address_full
    data_ind['full_address_2'] = address_full_2
    data_ind['rfc'] = data['rfc']
    data_ind['curp'] = data['curp']
    data_ind['date'] = user.date_joined
    data_ind['id'] = user.id
    data_ind['nss'] = user.username

    # Contrato cooperativista
    # Creamos el PDF con base en el HTML
    template = get_template('process_coop/contract/contract_coop.html')
    html = template.render(data)
    f = open(os.path.join(settings.MEDIA_ROOT, file_name), "w+b")
    pisaStatus = pisa.CreatePDF(html, dest=f)

    # Contrato industrial
    # Creamos el PDF con base en el HTML
    template_ind = get_template('process_coop/contract/contract_ind_associate.html')
    html_ind = template_ind.render(data_ind)
    f_ind = open(os.path.join(settings.MEDIA_ROOT, file_ind_name), "w+b")
    pisaStatus = pisa.CreatePDF(html_ind, dest=f_ind)

    # Credencial cooperativista
    # Creamos el PDF con la función de Reportlab
    file_card_name = "" + str(user.id) + "_" + user.username + "_credencial_socio.pdf"
    create_coop_card(id_user)

    return file_name, file_ind_name, file_card_name


# Create Bank Instruction Letter function
def bank_instruction_letter(letter_response):
    from PyPDF2 import PdfFileWriter, PdfFileReader
    import io
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter

    packet = io.BytesIO()
    # create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=letter)
    can.drawString(120, 651, str(letter_response['created_datetime'].strftime('%d/%m/%Y')))
    can.drawString(170, 358, str(letter_response['username']))
    can.drawString(110, 343, str(letter_response['user_rfc']))
    can.drawString(118, 329, str(letter_response['user_curp']))
    can.save()

    # move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(open(os.path.join(settings.BASE_DIR, 'static', 'files', 'carta_instruccion.pdf'), "rb"))
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    # finally, write "output" to a real file
    outputStream = open(os.path.join(settings.MEDIA_ROOT, 'empty_contracts', letter_response['letter_name']), "wb")
    output.write(outputStream)
    outputStream.close()


# Contract view
@login_required()
def contract_user(request, id_user):
    # Obtenemos la instancia del usuario y los datos de identificacion
    user = User.objects.get(id=id_user)
    iden_info = IdentifyInformation.objects.get(user=user)
    # Obtenemos datos del promotor
    upstream_name = User.objects.get(username=iden_info.upstream_promoter.user.username)
    # Obtenemos datos generales
    gen_info = GeneralInformation.objects.get(user=user)
    # Obtenemos direccion del usuario
    address_info = UserAddressProcess.objects.get(user=user)
    street_no = "" + address_info.street + ", No ext #" + address_info.ext_number
    if address_info.int_number:
        street_no += ", No int #" + address_info.int_number
    # Obtenemos datos del IMSS
    data_imss = CotImssRelation.objects.get(user=user)
    # Obtenemos los numeros
    numbers_info = NumberContact.objects.filter(
        Q(user=user)
    )
    numbers_list = []
    for number in numbers_info:
        numbers_list.append(str(number.number) + ", tipo " + str(number.number_type))
    # Obtenemos los correos
    email_info = AlternativeEmails.objects.filter(
        Q(user=user)
    )
    email_list = []
    if email_info:
        for email in email_info:
            email_list.append(email.alternative_email)
            email_list.append(user.email)
    else:
        email_list.append(user.email)
    # Obtenemos los dependientes economicos
    dependent_info = EconomicDependents.objects.filter(
        Q(user=user)
    )
    dependent_list = []
    if dependent_info:
        for dependent in dependent_info:
            dependent_dict = {}
            dependent_dict['d_full_name'] = "" + dependent.ape_pat + " " + dependent.ape_mat + " " + dependent.name
            dependent_dict['d_relation'] = dependent.relation
            dependent_dict['d_age'] = str(dependent.age) + " años"
            dependent_list.append(dependent_dict)
    # Obtenemos referencias personales
    references_info = PersonalReferences.objects.filter(
        Q(user=user)
    )
    references_list = []
    if references_info:
        for references in references_info:
            references_dict = {}
            references_dict[
                'r_full_name'] = "" + references.ape_pat_ref + " " + references.ape_mat_ref + " " + references.name_ref
            references_dict['r_number'] = references.num_contact
            references_dict['r_meet'] = references.meet_time
            references_list.append(references_dict)
    # Obtenemos los datos de bnkrec
    bnkrec_info = DataBnkRec.objects.filter(
        Q(user=user)
    )
    bnk_name = ''
    css_number = ''
    css_clave = ''
    account_type = ''
    if bnkrec_info:
        for bnkrec_info in bnkrec_info:
            bnk_name = bnkrec_info.bnk_name
            css_number = bnkrec_info.css_number
            css_clave = bnkrec_info.css_clave
            account_type = bnkrec_info.account_type
    # Creamos el nombre del archivo
    file_name = "" + str(user.id) + "_" + user.username + "_contratocooperativista.pdf"
    # Creamos dict de Contrato cooperativista
    data = dict()
    data['file_name'] = file_name
    data['id'] = user.id
    data['date_joined'] = user.date_joined
    data['upstream'] = upstream_name.get_full_name()
    data['nss'] = iden_info.user
    data['last_name'] = user.last_name
    data['first_name'] = user.first_name
    data['full_name'] = user.get_full_name
    data['age'] = gen_info.coop_age
    data['place_birth'] = gen_info.place_of_birth
    data['date_birth'] = gen_info.date_of_birth
    data['nationality'] = gen_info.nationality
    data['marri_status'] = gen_info.marital_status
    data['curp'] = gen_info.curp
    data['rfc'] = gen_info.rfc
    data['sex'] = gen_info.sex
    data['street_no'] = street_no
    data['suburb'] = address_info.suburb
    data['delegation'] = address_info.suburb.delegation
    data['state'] = address_info.suburb.state
    data['data_imss'] = data_imss.cotizacion_imss.salario_cot.aport_coop
    data['data_imss_letter'] = data_imss.cotizacion_imss.salario_cot.aport_letter
    data['numbers'] = numbers_list
    data['emails'] = email_list
    data['dependents'] = dependent_list
    data['references'] = references_list
    data['bank'] = bnk_name
    if css_number != None:
        data['account'] = css_number
    if css_clave != None:
        data['clave'] = css_clave
    data['type'] = account_type

    # Creamos una sola cadena con toda la direccion
    address_full = "" + data['street_no'] + ", " + str(data['suburb'])
    address_full_2 = "" + str(data['delegation']) + ", " + str(data['state'])
    # Creamos el nombre del archivo
    file_ind_name = "" + str(user.id) + "_" + user.username + "_contratocoindustrial.pdf"
    # Creamoos dict de Contrato Industrial
    data_ind = dict()
    data_ind['full_name'] = user.get_full_name
    data_ind['full_address'] = address_full
    data_ind['full_address_2'] = address_full_2
    data_ind['rfc'] = data['rfc']
    data_ind['curp'] = data['curp']
    data_ind['date'] = user.date_joined
    data_ind['id'] = user.id

    # Contrato cooperativista
    # Creamos el PDF con base en el HTML
    template = get_template('process_coop/contract/contract_coop.html')
    html = template.render(data)
    f = open(os.path.join(settings.MEDIA_ROOT + '/empty_contracts', file_name), "w+b")
    pisaStatus = pisa.CreatePDF(html, dest=f)

    # Contrato industrial
    # Creamos el PDF con base en el HTML
    template_ind = get_template('process_coop/contract/contract_ind_associate.html')
    html_ind = template_ind.render(data_ind)
    f_ind = open(os.path.join(settings.MEDIA_ROOT + '/empty_contracts', file_ind_name), "w+b")
    pisaStatus = pisa.CreatePDF(html_ind, dest=f_ind)

    # Credencial cooperativista
    # Creamos el PDF con la función de Reportlab
    file_card_name = "" + str(user.id) + "_" + user.username + "_credencial_socio.pdf"
    create_coop_card(id_user)

    # Creacion de carta instruccion
    letter_response = dict()

    letter_response['letter_name'] = "" + str(user.id) + "_" + user.username + "_carta_instruccion.pdf"
    letter_response['username'] = user.get_full_name()
    letter_response['user_rfc'] = data['rfc']
    letter_response['user_curp'] = data['curp']
    letter_response['created_datetime'] = datetime.datetime.today()

    bank_instruction_letter(letter_response)
    return render(request, "process_coop/contract.html", {
        'user': user,
        'file_name': file_name,
        'file_ind_name': file_ind_name,
        'file_card_name': file_card_name,
        'letter_name': letter_response['letter_name']
    })


# Update contracts
@login_required()
def update_contract_user(request, id_user):
    # Obtenemos la instancia del usuario y los datos de identificacion
    user = User.objects.get(id=id_user)
    iden_info = IdentifyInformation.objects.get(user=user)
    # Obtenemos datos del promotor
    upstream_name = User.objects.get(username=iden_info.upstream_promoter.user.username)
    # Obtenemos datos generales
    gen_info = GeneralInformation.objects.get(user=user)
    # Obtenemos direccion del usuario
    address_info = UserAddressProcess.objects.get(user=user)
    # Juntamos Calle con los numeros
    street_no = "" + address_info.street + ", No ext #" + address_info.ext_number
    # Validamos si tiene No int
    if address_info.int_number:
        street_no += ", No int #" + address_info.int_number
    # Obtenemos datos del IMSS
    data_imss = CotImssRelation.objects.get(user=user)
    # Obtenemos los numeros
    numbers_info = NumberContact.objects.filter(
        Q(user=user)
    )
    numbers_list = []
    for number in numbers_info:
        numbers_list.append(str(number.number) + ", tipo " + str(number.number_type))
    # Obtenemos los correos
    email_info = AlternativeEmails.objects.filter(
        Q(user=user)
    )
    email_list = []
    if email_info:
        for email in email_info:
            email_list.append(email.alternative_email)
            email_list.append(user.email)
    else:
        email_list.append(user.email)
    # Obtenemos los dependientes economicos
    dependent_info = EconomicDependents.objects.filter(
        Q(user=user)
    )
    dependent_list = []
    if dependent_info:
        for dependent in dependent_info:
            dependent_dict = {}
            dependent_dict['d_full_name'] = "" + dependent.ape_pat + " " + dependent.ape_mat + " " + dependent.name
            dependent_dict['d_relation'] = dependent.relation
            dependent_dict['d_age'] = str(dependent.age) + " años"
            dependent_list.append(dependent_dict)
    # Obtenemos referencias personales
    references_info = PersonalReferences.objects.filter(
        Q(user=user)
    )
    references_list = []
    if references_info:
        for references in references_info:
            references_dict = {}
            references_dict[
                'r_full_name'] = "" + references.ape_pat_ref + " " + references.ape_mat_ref + " " + references.name_ref
            references_dict['r_number'] = references.num_contact
            references_dict['r_meet'] = references.meet_time
            references_list.append(references_dict)
        # Obtenemos los datos de bnkrec
        bnkrec_info = DataBnkRec.objects.filter(
            Q(user=user)
        )
        bnk_name = ''
        css_number = ''
        css_clave = ''
        account_type = ''
        if bnkrec_info:
            for bnkrec_info in bnkrec_info:
                bnk_name = bnkrec_info.bnk_name
                css_number = bnkrec_info.css_number
                css_clave = bnkrec_info.css_clave
                account_type = bnkrec_info.account_type
    # Creamos el nombre del archivo
    file_name = "" + str(user.id) + "_" + user.username + "_contratocooperativista.pdf"
    # Creamos dict de Contrato cooperativista
    data = {}
    data['file_name'] = file_name
    data['id'] = user.id
    data['date_joined'] = user.date_joined
    data['upstream'] = upstream_name.get_full_name()
    data['nss'] = iden_info.user
    data['last_name'] = user.last_name
    data['first_name'] = user.first_name
    data['full_name'] = user.get_full_name
    data['age'] = gen_info.coop_age
    data['place_birth'] = gen_info.place_of_birth
    data['date_birth'] = gen_info.date_of_birth
    data['nationality'] = gen_info.nationality
    data['marri_status'] = gen_info.marital_status
    data['curp'] = gen_info.curp
    data['rfc'] = gen_info.rfc
    data['sex'] = gen_info.sex
    data['street_no'] = street_no
    data['suburb'] = address_info.suburb
    data['delegation'] = address_info.suburb.delegation
    data['state'] = address_info.suburb.state
    data['data_imss'] = data_imss.cotizacion_imss.salario_cot.aport_coop
    data['data_imss_letter'] = data_imss.cotizacion_imss.salario_cot.aport_letter
    data['numbers'] = numbers_list
    data['emails'] = email_list
    data['dependents'] = dependent_list
    data['references'] = references_list
    data['bank'] = bnk_name
    if css_number != None:
        data['account'] = css_number
    if css_clave != None:
        data['clave'] = css_clave
    data['type'] = account_type

    # Creamos una sola cadena con toda la direccion
    address_full = "" + data['street_no'] + ", " + str(data['suburb'])
    address_full_2 = "" + str(data['delegation']) + ", " + str(data['state'])
    # Creamos el nombre del archivo
    file_ind_name = "" + str(user.id) + "_" + user.username + "_contratocoindustrial.pdf"
    # Creamoos dict de Contrato Industrial
    data_ind = {}
    data_ind['full_name'] = user.get_full_name
    data_ind['full_address'] = address_full
    data_ind['full_address_2'] = address_full_2
    data_ind['rfc'] = data['rfc']
    data_ind['curp'] = data['curp']
    data_ind['date'] = user.date_joined
    data_ind['id'] = user.id
    data_ind['nss'] = user.username

    # Contrato cooperativista
    # Creamos el PDF con base en el HTML
    template = get_template('process_coop/contract/contract_coop.html')
    html = template.render(data)
    f = open(os.path.join(settings.MEDIA_ROOT, 'empty_contracts', file_name), "w+b")
    pisaStatus = pisa.CreatePDF(html, dest=f)

    # Contrato industrial
    # Creamos el PDF con base en el HTML
    template_ind = get_template('process_coop/contract/contract_ind_associate.html')
    html_ind = template_ind.render(data_ind)
    f_ind = open(os.path.join(settings.MEDIA_ROOT, 'empty_contracts', file_ind_name), "w+b")
    pisaStatus = pisa.CreatePDF(html_ind, dest=f_ind)

    # Credencial cooperativista
    # Creamos el PDF con la función de Reportlab
    file_card_name = "" + str(user.id) + "_" + user.username + "_credencial_socio.pdf"
    create_coop_card(id_user)

    # Creacion de carta instruccion
    letter_response = dict()

    letter_response['letter_name'] = "" + str(user.id) + "_" + user.username + "_carta_instruccion.pdf"
    letter_response['username'] = user.get_full_name()
    letter_response['user_rfc'] = data['rfc']
    letter_response['user_curp'] = data['curp']
    letter_response['created_datetime'] = datetime.datetime.today()

    bank_instruction_letter(letter_response)

    return render(request, "process_coop/update_contract.html",
                  {'user': user, 'file_name': file_name, 'file_ind_name': file_ind_name,
                   'file_card_name': file_card_name, 'letter_name': letter_response['letter_name']})


# Documentation view
@login_required()
def documentation(request, id_user):
    # Obtenemos la instancia del usuario
    user = User.objects.get(id=id_user)
    # Validamos si puede generar contratos nuevamente
    validate_data = validate_contract_data(id_user)
    # Creamos un formulario vacio
    form = DocumentationForm()
    # Si recibimos un POST
    if request.method == 'POST':
        form = DocumentationForm(request.POST, request.FILES)
        # Validamos el form
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    return render(request, "process_coop/documentation.html",
                  {'user': user, 'validate_data': validate_data, 'form': form})


# Update user documentation
@login_required()
def update_documentation(request, id_user):
    # Obtenemos mi instancia de usuario
    user = User.objects.get(id=id_user)
    validate_data = DocumentationUser.objects.filter(
        Q(user=user)
    )
    # Validamos si el usuario ya tiene un registro de documentos
    if validate_data:
        instancia = DocumentationUser.objects.get(user=user)
        # Creamos un formulario con nuestra instancia
        form = UpdateDocumentationForm(instance=instancia)
    else:
        return redirect('documentation', user.id)
    # Validamos que el usuario tenga toda la información de los contratos
    val_info_contract = validate_contract_data(id_user)
    # Si se envia un POST
    if request.method == 'POST':
        form = UpdateDocumentationForm(request.POST, request.FILES, instance=instancia)
        if form.is_valid():
            instancia = form.save(commit=False)
            instancia.save()
            return redirect('dashboard')
    return render(request, "process_coop/update_documentation.html",
                  {'form': form, 'user': user, 'val_info_contract': val_info_contract})


# Short register
@csrf_exempt
def qr_register(request, optional_nss=''):
    # Ceo Dummy
    dummy_ceo = '75315948260'

    # Creamos el form de varios modelos
    better_form = ShortProcessForm()

    # Creamos el dict de Identify
    identify_dict = dict()

    # Validamos si hay un usuario autenticado
    if request.user.is_authenticated:
        # Obtenemos la instancia de información de indentificación
        user_identify = IdentifyInformation.objects.get(user=request.user)
        identify_dict['ceo'] = CeosRegisterList.objects.get(user=user_identify.ceo.user)
        identify_dict['upstream_promoter'] = PromotersRegisterList.objects.get(user__username=request.user)
    else:
        # Validamos si la url tiene parametro
        if optional_nss != '':
            # Obtenemos la instancia de información de indentificación del socio dueño del QR
            promoter_identify = IdentifyInformation.objects.get(user=User.objects.get(username=optional_nss))
            identify_dict['ceo'] = CeosRegisterList.objects.get(user=promoter_identify.ceo.user)
            identify_dict['upstream_promoter'] = PromotersRegisterList.objects.get(user__username=optional_nss)

        else:
            identify_dict['ceo'] = CeosRegisterList.objects.get(user__username=dummy_ceo)
            identify_dict['upstream_promoter'] = PromotersRegisterList.objects.get(user__username=dummy_ceo)

    identify_dict['offices_list'] = OfficesList.objects.get(id=1)
    identify_dict['status_reason'] = StatusReason.objects.get(id=1)
    identify_dict['status_user'] = StatusUser.objects.get(id=1)
    identify_dict['user_type'] = UserType.objects.get(id=3)

    # Recibimos la peticion de ajax
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

    # Validamos si se envía un POST
    if request.method == 'POST':
        better_form = ShortProcessForm(request.POST)
        if better_form.is_valid():
            # User form
            user = better_form['user_form'].save()
            # Contact form
            contact = better_form['contact_form'].save(commit=False)
            contact.user = user
            contact.save()
            # General form
            general = better_form['general_form'].save(commit=False)
            general.user = user
            general.save()

            # Creamos el registro de identificacion
            identify_dict['user'] = user
            # Creamos registro de sesion de usuario
            sesion_control(user.id, 2)
            identify_dict['status_pmnt_sesion'] = SesionControl.objects.get(user=user)
            id_identify_info = IdentifyInformation.objects.create(**identify_dict)
            add_promoters_list(user.id)
            if request.user.is_authenticated:
                return redirect('dashboard')
            else:
                return redirect('qr_register_success')

    return render(request, "process_coop/short_register.html", {'better_form': better_form})


# Short Register Successfully
def qr_register_success(request):
    return render(request, "process_coop/short_register_success.html")
