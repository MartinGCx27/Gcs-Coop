import pdb
import os
from django.conf import settings
from django.shortcuts import render, redirect
# Import decorators
from django.views.decorators.csrf import csrf_exempt
# Importing Q
from django.db.models import Q
# Import json response
from django.http import JsonResponse
# Importing forms
from .forms import *
# Import dashboad models
from dashboard.models import SesionControl, PromotersRegisterList
# Importing coop info models
from coop_info.models import IdentifyInformation, GeneralInformation, NumberContact, UserAddressProcess, \
    CotizacionImss, CotImssRelation, EconomicDependents, PersonalReferences, DataBnkRec, EconomicActivity, \
    AlternativeEmails, DocumentationUser, PreRegisterLog
# Importing catalogues
from catalogues.models import UserType, AffiliateType, AffiliationReason, StatusReason, StatusUser, LocationCatalogue, \
    StatusImss, PaymentImss, ActivityType, Status, PromotersListStatus
# Import process_coop views
from process_coop import views


# Create your views here.

# Create pre-register log
def pre_register_log(id_user):
    # Obtenemos la instancia del usuario
    user = User.objects.get(id=id_user)
    # Validamos que no exista el registro
    validate_data = PreRegisterLog.objects.values().filter(
        Q(user=user)
    )
    # Si el registro no existe
    if len(validate_data) == 0:
        # Creamos el registro
        pre_register_log_id = PreRegisterLog.objects.create(
            user=user
        )
    # Si el registro ya existe
    else:
        # Lo modificamos
        pre_register_log_id = PreRegisterLog.objects.filter(
            Q(user=user)
        ).update(
            user=user
        )


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


def add_promoters_list(user_id):
    # Obtenemos la instancia de usuario
    user = User.objects.get(id=user_id)
    # Validamos que no exista un registro
    if PromotersRegisterList.objects.values().filter(user=user).exists():
        pass
    else:
        # Creamos el registro
        status = PromotersListStatus.objects.filter(id=2)
        promoters_register_list_id = PromotersRegisterList.objects.create(
            user=user,
            status=status[0]
        )


# Crear nuevo usuario
@csrf_exempt
def pre_create_user(request):
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
                # Creamos registro de sesion de usuario
                sesion_control(user_id)
                # Creamos registro en lista de socios promotores con status inactivo
                add_promoters_list(user_id)
                return redirect('pre_identify_info', user_id)
            # Si no existe, regresamos a crear usuarios
            else:
                return redirect('create_user')
    return render(request, "pre_register/pre_create_user.html", {'form': form})


# Información de identificación
def pre_identify_info(request, id_user):
    # Obtenemos los datos del logeado
    user_login = IdentifyInformation.objects.get(user=request.user)

    # Creamos un formulario vacio
    form = IdentifyInforForm()

    # Si recibe un formulario POST
    if request.method == 'POST':
        identify_dict = dict()

        # Obtenemos director y promotor
        identify_dict['ceo'] = user_login.ceo
        identify_dict['upstream_promoter'] = PromotersRegisterList.objects.get(user=user_login.user)

        # Obtenemos tipo afiliacion
        affiliate_type = request.POST.get("affiliate_type")
        if affiliate_type:
            identify_dict['affiliate_type'] = AffiliateType.objects.get(id=affiliate_type)

        # Obtenemos motivo afiliacion
        affiliation_reason = request.POST.get("affiliation_reason")
        if affiliation_reason:
            identify_dict['affiliation_reason'] = AffiliationReason.objects.get(id=affiliation_reason)

        # Obtenemos la oficina
        identify_dict['offices_list'] = user_login.offices_list

        # Obtenemos status motivo
        identify_dict['status_reason'] = StatusReason.objects.get(id=1)

        # Obtenemos el status user
        identify_dict['status_user'] = StatusUser.objects.get(id=1)

        # Obtememos la instancia del usuario
        identify_dict['user'] = User.objects.get(id=id_user)

        # Obtenemos el tipo de usuario
        identify_dict['user_type'] = UserType.objects.get(id=3)

        # btememos la instancia del pago y sesion de usuario
        identify_dict['status_pmnt_sesion'] = SesionControl.objects.get(user=id_user)

        # Validamos que no exista el registro
        validate_data = IdentifyInformation.objects.values().filter(
            Q(user=identify_dict['user'])
        )
        # Si el registro no existe
        if len(validate_data) == 0:
            # Creamos un registro nuevo
            identify_info_id = IdentifyInformation.objects.create(**identify_dict)
            return redirect('pre_general_info', id_user)

    return render(request, "pre_register/pre_identify_info.html", {'form': form, 'user_login': user_login})


# Información general
def pre_general_info(request, id_user):
    # Obtenemos instancia del usuario
    user = User.objects.get(id=id_user)

    # Creamos formulario vacio
    form = GeneralInfoForm()

    # Colocamos la nacionalidad 'Mexicana' como default en el select
    form.fields['nationality'].initial = 73

    # Si recibe un formulario POST
    if request.method == 'POST':
        form = GeneralInfoForm(request.POST)
        # Validamos el formulario
        if form.is_valid():
            form.save()
            return redirect('pre_address_registration', id_user)
    return render(request, "pre_register/pre_general_info.html", {'user': user, 'form': form})


# Direccion de socio
@csrf_exempt
def pre_address_registration(request, id_user):
    # Obtenemos instancia del usuario
    user = User.objects.get(id=id_user)

    # Creamos un formulario vacio
    form = UserAddressForm()

    # Obtenemos respuesta de ajax en select
    if 'action' in request.POST:
        data = []
        for i in LocationCatalogue.objects.filter(zip_code=request.POST['zip_code']):
            data.append({'id': i.id, 'suburb': i.suburb})
        return JsonResponse(data, safe=False)

    # Obtenemos respuesta de ajax en select 2
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
        return redirect('pre_numbers_registration', id_user)
    return render(request, "pre_register/pre_address.html", {'user': user, 'form': form})


# Numeros de contacto
def pre_numbers_registration(request, id_user):
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
    return render(request, "pre_register/pre_numbers.html", {'user_num': user_number, 'user': user, 'form': form})


# Correos alternativos
def pre_alternative_emails(request, id_user):
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
            return redirect('pre_imss', id_user)
    return render(request, "pre_register/pre_alternative_emails.html", {'user': user, 'form': form})


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


# Datos de cotizacion
def pre_imss(request, id_user):
    # Instancia del usuario
    user = User.objects.get(id=id_user)

    # Hacemos un formulario vacio
    form = CotIMSForm()

    # Si envía un POST
    if request.method == 'POST':
        form = CotIMSForm(request.POST)
        # Validamos el form
        if form.is_valid():
            ob_form = form.save()
            # Ingresamos los datos a la bd con la funcion
            imss_rel_func(request, id_user, ob_form.id)
            return redirect('pre_economic_act', id_user)
    return render(request, "pre_register/pre_imss.html", {'user': user, 'form': form})


# Actividades economicas
@csrf_exempt
def pre_economic_act(request, id_user):
    # Obtenemos la instancia del usuario
    user = User.objects.get(id=id_user)

    # Obtengo las actividades de mi usuario
    act_register = EconomicActivity.objects.filter(
        Q(user=user)
    )

    # Creamos un form vacio
    form = EconomicActForm()

    # Obtenemos datos de ajax
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

        # Creamos el registro
        economic_activity_id = EconomicActivity.objects.create(
            activity=activity,
            activity_description=activity_description,
            activity_type=activity_type,
            user=user
        )
    return render(request, "pre_register/pre_economic_act.html",
                  {'form': form, 'user': user, 'act_register': act_register})


# Pre databnk rec
def pre_data_bnk_rec(request, id_user):
    # Obtenemos la instancia del usuario
    user = User.objects.get(id=id_user)

    # Creamos un form vacio
    form = DataBnkRecForm()

    # Si envía un POST
    if request.method == 'POST':
        form = DataBnkRecForm(request.POST)
        # Validamos el form
        if form.is_valid():
            form.save()
            return redirect('pre_economic_depen', id_user)
    return render(request, "pre_register/pre_databnk_rec.html",
                  {'form': form, 'user': user})


# Pre economic_dependent
def pre_economic_dependent(request, id_user):
    # Obtenemos la instancia del usuario
    user = User.objects.get(id=id_user)

    # Creamos un formulario vacio
    form = EconomicDependentForm()

    # Obtenemos los registros del usuario
    depen_data = EconomicDependents.objects.filter(
        Q(user=user)
    )

    # Si envia un POST
    if request.method == 'POST':
        form = EconomicDependentForm(request.POST)
        # Validamos el form
        if form.is_valid():
            form.save()
    return render(request, "pre_register/pre_economic_depen.html",
                  {'form': form, 'user': user, 'depen_data': depen_data})


# Pre personal references
def pre_personal_references(request, id_user):
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
    return render(request, "pre_register/pre_personal_ref.html", {'form': form, 'user': user, 'ref_data': ref_data})


# Resumen de información
def pre_resumen(request, id_user):
    # Obtenemos la instancia del usuario
    user = User.objects.get(id=id_user)
    # Obtenemos la información de identificación
    identify_info = IdentifyInformation.objects.filter(user=user)
    # Obtenemos informacion general
    general_info = GeneralInformation.objects.filter(
        Q(user=user)
    )
    # Obtenemos Direccion
    address_info = UserAddressProcess.objects.filter(
        Q(user=user)
    )
    # Obtenemos Contacto
    number_info = NumberContact.objects.filter(
        Q(user=user),
        Q(status=1)
    )
    # Obtenemos correos alternativos
    altermail_info = AlternativeEmails.objects.filter(
        Q(user=user)
    )
    # Obtenemos datos de cotizacion
    imss_info = CotImssRelation.objects.filter(
        Q(user=user)
    )
    # Obtenemos actividad economica
    act_eco_info = EconomicActivity.objects.filter(
        Q(user=user),
        Q(status=1)
    )
    # Obtenemos datos bnk rec
    bnkrec_info = DataBnkRec.objects.filter(
        Q(user=user)
    )
    # Obtenemos dependientes economicos
    eco_dependent_info = EconomicDependents.objects.filter(
        Q(user=user),
        Q(status=1)
    )
    # Obtenemos referencias
    reference_info = PersonalReferences.objects.filter(
        Q(user=user),
        Q(status=1)
    )

    # Validamos si puede generar contratos
    validate_data = views.validate_contract_data(id_user)
    if validate_data:
        # Creamos los contratos del usuario
        data = views.create_user_contracts(id_user)
        contract_user_id = DocumentationUser.objects.create(
            contract_coop=data[0],
            contract_user=data[1],
            user=user
        )

    return render(request, "pre_register/pre_resumen.html", {
        'user': user,
        'general_info': general_info,
        'address_info': address_info,
        'number_info': number_info,
        'altermail_info': altermail_info,
        'imss_info': imss_info,
        'act_eco_info': act_eco_info,
        'eco_dependent_info': eco_dependent_info,
        'reference_info': reference_info,
        'bnkrec_info': bnkrec_info,
    })
