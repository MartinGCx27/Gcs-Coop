import pdb
from tokenize import String
from turtle import pd

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
import qrcode
import os
from django.conf import settings
# Import coop info models
from coop_info.models import IdentifyInformation, GeneralInformation, UserAddressProcess, NumberContact, \
    AlternativeEmails, CotImssRelation, EconomicActivity, EconomicDependents, PersonalReferences, DataBnkRec, \
    DocumentationUser, PreRegisterLog
# Import catalogues models
from catalogues.models import UserType, StatusIssue, Status, PromotersListStatus
# Import core models
from core.models import UserContact, GcsServices
# Import dashboad models
from .models import SesionControl, InformationIssue, VideoTutorials, VideoTutorialsHeader, PromotersRegisterList
# Import User model
from django.contrib.auth.models import User
# Import .forms
from .forms import *
from django.views.decorators.csrf import csrf_exempt

# Prueba
from django.views.generic import ListView, TemplateView, UpdateView
# Para usar decoradores en clases
from django.utils.decorators import method_decorator


# Change session control function
def change_session_control(id_user, session_number):
    # Obtengo instancia de usuario
    user = User.objects.get(id=id_user)
    # Editamos el registro de sesion
    session_control_id = SesionControl.objects.filter(
        Q(user=user)
    ).update(
        sesion=session_number
    )


# Change user type function
def change_user_type(id_user):
    # Obtengo la instancia de usuario
    user = User.objects.get(id=id_user)
    # Validamos si el usuario tiene algún socio creado
    # Si tiene 'hijos'
    if IdentifyInformation.objects.filter(
            upstream_promoter=PromotersRegisterList.objects.get(user__id=id_user)).exists():
        # Validamos si ya está modificado el campo
        val_user_type = IdentifyInformation.objects.get(user=id_user)
        if val_user_type.user_type == UserType.objects.get(id=3):
            # Modificamos el tipo de usuario
            identify_info_id = IdentifyInformation.objects.filter(
                Q(user=user)
            ).update(
                # Cambiamos la instancia de tipo usuario a Promotor ascendente (2)
                user_type=UserType.objects.get(id=2)
            )
            # Creamos instancia a lista de promotores
            # Validamos si ya existe registro con estatus activo en la lista de promotores
            if not PromotersRegisterList.objects.filter(
                    Q(status=PromotersListStatus.objects.get(id=1)),
                    Q(user__id=id_user)
            ).exists():
                # Modificamos el tipo de usuario
                # Nombre relacionado con el modelo + _id ya que es la instancia
                PromotersRegisterList_id = PromotersRegisterList.objects.filter(
                    user__id=id_user,
                ).update(
                    status=PromotersListStatus.objects.get(id=1)
                )
        elif val_user_type.user_type == UserType.objects.get(id=1) or UserType.objects.get(id=4):
            # Evaluamos si no esta activo el estatus de promotor ascendente
            if not PromotersRegisterList.objects.filter(
                    Q(status=PromotersListStatus.objects.get(id=1)),
                    Q(user__id=id_user)
            ).exists():
                # Cambiamos el estatus de promotor ascendente a activo
                PromotersRegisterList_id = PromotersRegisterList.objects.filter(
                    user__id=id_user,
                ).update(
                    status=PromotersListStatus.objects.get(id=1))


def contracts_validation(id_user):
    # Obtenemos la documentacion del socio
    docu = DocumentationUser.objects.filter(
        Q(user=id_user)
    )

    if docu:

        validate_contracts = dict()

        if docu[0].contract_coop:
            validate_contracts['val_contract_coop'] = True
        else:
            validate_contracts['val_contract_coop'] = False
            validate_contracts['msg_contract_coop'] = "Contrato cooperativista"

        if docu[0].contract_user:
            validate_contracts['val_contract_user'] = True
        else:
            validate_contracts['val_contract_user'] = False
            validate_contracts['msg_contract_user'] = "Contrato de socio individual"

        if validate_contracts['val_contract_coop'] and validate_contracts['val_contract_user']:
            validate_contracts['contracts_val'] = True
        else:
            validate_contracts['contracts_val'] = False

        return validate_contracts
    
    else:
        return "Sin_contratos"


# Create your views here.


# Dashboard view
@login_required()
def dashboard(request):
    # Obtenemos valor de barra de busqueda
    search_validate = False
    queryset_search = request.GET.get('buscar')

    # Obtenemos Identify information
    identify_info = IdentifyInformation.objects.filter(user=request.user)
    # Validamos si es superuser
    is_superuser = bool
    if identify_info[0].user_type.user_type == 'Super usuario':
        # Si la barra de busqueda tiene datos
        if queryset_search:
            general_info = IdentifyInformation.objects.filter(
                Q(user__first_name__icontains=queryset_search) |
                Q(user__last_name__icontains=queryset_search) |
                Q(user__username__icontains=queryset_search)
            )
            # Validamos si la consulta trae datos
            if IdentifyInformation.objects.all():
                search_validate = True
        else:
            general_info = IdentifyInformation.objects.all().exclude(user=request.user)
        is_superuser = True
    else:
        # Si la barra de busqueda tiene datos
        if queryset_search:
            general_info = IdentifyInformation.objects.filter(
                Q(upstream_promoter=PromotersRegisterList.objects.get(user=request.user)),
                Q(user__first_name__icontains=queryset_search) |
                Q(user__username__icontains=queryset_search)
            )
            # Validamos si la consulta trae datos
            if IdentifyInformation.objects.filter(
                    upstream_promoter=PromotersRegisterList.objects.get(user=request.user)):
                search_validate = True
        else:
            general_info = IdentifyInformation.objects.filter(
                upstream_promoter=PromotersRegisterList.objects.get(user=request.user))
        is_superuser = False

    # Creamos una instancia del usuario
    instancia = User.objects.get(id=request.user.id)

    # Validamos si es primer inicio de sesión
    session_control = SesionControl.objects.filter(
        Q(user=request.user)
    )
    for data_session in session_control:
        if data_session.sesion == '1':
            session_flag = 1
        elif data_session.sesion == '2':
            session_flag = 2
        elif data_session.sesion == '3':
            session_flag = 3

        else:
            session_flag = 2
    change_user_type(request.user.id)

    # Si recibimos POST de cambio de pass
    if request.method == 'POST':
        if request.POST.get("password") != '':
            if request.POST.get("password") == request.POST.get("password_2"):
                instancia.set_password(request.POST.get("password"))
                instancia.save()
                change_session_control(request.user.id, 2)
                return redirect('logout')
        else:
            return redirect('dashboard')
    # pdb.set_trace()
    return render(request, "dashboard/dashboard.html", {
        'search_validate': search_validate,
        'gen_info': general_info,
        'session_flag': session_flag,
        'identify_info': identify_info,
        'is_superuser': is_superuser,
    })


@login_required()
def my_info(request):
    # Obtenemos informacion USer
    user = User.objects.filter(
        Q(id=request.user.id)
    )
    # Obtenemos Identify information
    identify_info = IdentifyInformation.objects.filter(
        Q(user=request.user)
    )
    # Obtenemos General information
    general_info = GeneralInformation.objects.filter(
        Q(user=request.user)
    )
    # Obtenemos Direccion
    address_info = UserAddressProcess.objects.filter(
        Q(user=request.user)
    )
    # Obtenemos Number Contact
    number_info = NumberContact.objects.filter(
        Q(user=request.user),
        Q(status=1)
    )
    # Obtenemos correos alternativos
    altermail_info = AlternativeEmails.objects.filter(
        Q(user=request.user)
    )
    # Obtenemos datos IMSS
    imss_info = CotImssRelation.objects.filter(
        Q(user=request.user)
    )
    # Obtenemos actividad economica
    act_eco_info = EconomicActivity.objects.filter(
        Q(user=request.user)
    )
    # Obtenemos dependientes economicos
    eco_dependent_info = EconomicDependents.objects.filter(
        Q(user=request.user)
    )
    # Obtenemos referencias
    reference_info = PersonalReferences.objects.filter(
        Q(user=request.user)
    )
    # Si recibimos un POST
    if request.method == 'POST':
        # Obtenemos la instancia de usuario
        user = User.objects.get(id=request.user.id)
        # Obtenemos instancia de status issue
        status_issue = StatusIssue.objects.get(id=1)
        # Obtememos el promotor del usuario
        for identify_info in identify_info:
            promoter = identify_info.upstream_promoter
        info_issue_id = InformationIssue.objects.create(
            title=request.POST.get("title"),
            message=request.POST.get("message"),
            status_issue=status_issue,
            user=user,
            upstream_promoter=promoter
        )
        return redirect('issue_sended')

    # VALIDACIÓN DE PAGO PARA ACTIVACIÓN DE NAVBAR
    # Validamos si es superuser
    is_superuser = bool
    if identify_info[0].user_type.user_type == 'Super usuario':
        is_superuser = True
    else:
        is_superuser = False

    # Validamos si es primer inicio de sesión
    session_control = SesionControl.objects.filter(
        Q(user=request.user)
    )
    for data_session in session_control:
        if data_session.sesion == '1':
            session_flag = 1
        elif data_session.sesion == '2':
            session_flag = 2
        elif data_session.sesion == '3':
            session_flag = 3
        else:
            session_flag = 2

    return render(request, "dashboard/my_info.html", {
        'user': user,
        'identify_info': identify_info,
        'general_info': general_info,
        'address_info': address_info,
        'number_info': number_info,
        'altermail_info': altermail_info,
        'imss_info': imss_info,
        'act_eco_info': act_eco_info,
        'eco_dependent_info': eco_dependent_info,
        'reference_info': reference_info,
        'session_flag': session_flag,
        'identify_info': identify_info,
        'is_superuser': is_superuser
    })


# Message view
@login_required()
def message(request):
    # Obtenemos Identify information
    identify_info = IdentifyInformation.objects.filter(
        Q(user=request.user)
    )
    # Obtenemos los mensajes de contacto
    message = UserContact.objects.order_by(
        'first_name'
    )

    # VALIDACIÓN DE PAGO PARA ACTIVACIÓN DE NAVBAR
    # Validamos si es superuser
    is_superuser = bool
    if identify_info[0].user_type.user_type == 'Super usuario':
        is_superuser = True
    else:
        is_superuser = False

    # Validamos si es primer inicio de sesión
    session_control = SesionControl.objects.filter(
        Q(user=request.user)
    )
    for data_session in session_control:
        if data_session.sesion == '1':
            session_flag = 1
        elif data_session.sesion == '2':
            session_flag = 2
        elif data_session.sesion == '3':
            session_flag = 3
        else:
            session_flag = 2

    return render(request, "dashboard/message.html", {
        'message': message,
        'identify_info': identify_info,
        'session_flag': session_flag,
        'identify_info': identify_info,
        'is_superuser': is_superuser
    })


# Issue sended message view
@login_required()
def issue_sended(request):
    # VALIDACIÓN DE PAGO PARA ACTIVACIÓN DE NAVBAR
    # Obtenemos Identify information
    identify_info = IdentifyInformation.objects.filter(
        Q(user=request.user)
    )

    # Validamos si es superuser
    is_superuser = bool
    if identify_info[0].user_type.user_type == 'Super usuario':
        is_superuser = True
    else:
        is_superuser = False

    # Validamos si es primer inicio de sesión
    session_control = SesionControl.objects.filter(
        Q(user=request.user)
    )
    for data_session in session_control:
        if data_session.sesion == '1':
            session_flag = 1
        elif data_session.sesion == '2':
            session_flag = 2
        elif data_session.sesion == '3':
            session_flag = 3
        else:
            session_flag = 2

    return render(request, "dashboard/issue_sended.html", {
        'session_flag': session_flag,
        'identify_info': identify_info,
        'is_superuser': is_superuser
    })


# Information issue message
@login_required()
def info_recived(request):
    # Obtenemos Identify information
    identify_info = IdentifyInformation.objects.filter(
        Q(user=request.user)
    )
    # Obtemeos lista de solicitudes de cambio
    issue_info = InformationIssue.objects.filter(
        Q(status_issue=1)
    )
    # Obtenemos número de mensajes
    issue_number = len(issue_info)

    # VALIDACIÓN DE PAGO PARA ACTIVACIÓN DE NAVBAR
    # Validamos si es superuser
    is_superuser = bool
    if identify_info[0].user_type.user_type == 'Super usuario':
        is_superuser = True
    else:
        is_superuser = False

    # Validamos si es primer inicio de sesión
    session_control = SesionControl.objects.filter(
        Q(user=request.user)
    )
    for data_session in session_control:
        if data_session.sesion == '1':
            session_flag = 1
        elif data_session.sesion == '2':
            session_flag = 2
        elif data_session.sesion == '3':
            session_flag = 3
        else:
            session_flag = 2

    return render(request, "dashboard/info_issue.html", {
        'issue_info': issue_info,
        'issue_number': issue_number,
        'identify_info': identify_info,
        'session_flag': session_flag,
        'identify_info': identify_info,
        'is_superuser': is_superuser
    })


# Update Information Issue
@login_required()
def update_info_issue(request, id_issue):
    # Obtenemos instancia de status issue
    status_issue = StatusIssue.objects.get(id=2)
    # Obtenemos el mensaje del usuario
    issue_user = InformationIssue.objects.get(id=id_issue)
    # Si envía un POST
    if request.method == 'POST':
        # Actualizamos el registro a 'Atendido'
        issue_update = InformationIssue.objects.filter(
            Q(id=id_issue)
        ).update(
            status_issue=status_issue
        )
        return redirect('info_recived')

    # VALIDACIÓN DE PAGO PARA ACTIVACIÓN DE NAVBAR
    # Obtenemos Identify information
    identify_info = IdentifyInformation.objects.filter(
        Q(user=request.user)
    )
    # Validamos si es superuser
    is_superuser = bool
    if identify_info[0].user_type.user_type == 'Super usuario':
        is_superuser = True
    else:
        is_superuser = False

    # Validamos si es primer inicio de sesión
    session_control = SesionControl.objects.filter(
        Q(user=request.user)
    )
    for data_session in session_control:
        if data_session.sesion == '1':
            session_flag = 1
        elif data_session.sesion == '2':
            session_flag = 2
        elif data_session.sesion == '3':
            session_flag = 3
        else:
            session_flag = 2

    return render(request, "dashboard/update_info_issue.html", {
        'issue_user': issue_user,
        'session_flag': session_flag,
        'identify_info': identify_info,
        'is_superuser': is_superuser
    })


# Services view
@login_required()
@staff_member_required
def services(request):
    # Obtenemos Identify information
    identify_info = IdentifyInformation.objects.filter(
        Q(user=request.user)
    )
    # Obtenemos todos los servicios del sitio
    services_list = GcsServices.objects.all()

    # VALIDACIÓN DE PAGO PARA ACTIVACIÓN DE NAVBAR

    # Validamos si es superuser
    is_superuser = bool
    if identify_info[0].user_type.user_type == 'Super usuario':
        is_superuser = True
    else:
        is_superuser = False

    # Validamos si es primer inicio de sesión
    session_control = SesionControl.objects.filter(
        Q(user=request.user)
    )
    for data_session in session_control:
        if data_session.sesion == '1':
            session_flag = 1
        elif data_session.sesion == '2':
            session_flag = 2
        elif data_session.sesion == '3':
            session_flag = 3
        else:
            session_flag = 2

    return render(request, "dashboard/services.html", {
        'services_list': services_list,
        'identify_info': identify_info,
        'session_flag': session_flag,
        'identify_info': identify_info,
        'is_superuser': is_superuser
    })


# Create service view
@login_required()
@staff_member_required
def create_service(request):
    # Obtenemos Identify information
    identify_info = IdentifyInformation.objects.filter(
        Q(user=request.user)
    )
    # Creamos un form vacio
    form = CreateServiceForm()
    # Si se envia un POST
    if request.method == 'POST':
        form = CreateServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('services')

    # VALIDACIÓN DE PAGO PARA ACTIVACIÓN DE NAVBAR

    # Validamos si es superuser
    is_superuser = bool
    if identify_info[0].user_type.user_type == 'Super usuario':
        is_superuser = True
    else:
        is_superuser = False

    # Validamos si es primer inicio de sesión
    session_control = SesionControl.objects.filter(
        Q(user=request.user)
    )
    for data_session in session_control:
        if data_session.sesion == '1':
            session_flag = 1
        elif data_session.sesion == '2':
            session_flag = 2
        elif data_session.sesion == '3':
            session_flag = 3
        else:
            session_flag = 2

    return render(request, "dashboard/create_service.html", {
        'form': form,
        'identify_info': identify_info,
        'session_flag': session_flag,
        'identify_info': identify_info,
        'is_superuser': is_superuser
    })


# Update service view
@login_required()
@staff_member_required
def update_service(request, id_service):
    # Obtenemos la instancia del servicio
    instancia = GcsServices.objects.get(id=id_service)
    # Creamos el form con la instancia
    form = UpdateServiceForm(instance=instancia)
    if request.method == 'POST':
        form = UpdateServiceForm(request.POST, request.FILES, instance=instancia)
        if form.is_valid():
            form.save()
            return redirect('services')

    # VALIDACIÓN DE PAGO PARA ACTIVACIÓN DE NAVBAR

    # Obtenemos Identify information
    identify_info = IdentifyInformation.objects.filter(
        Q(user=request.user)
    )
    # Validamos si es superuser
    is_superuser = bool
    if identify_info[0].user_type.user_type == 'Super usuario':
        is_superuser = True
    else:
        is_superuser = False

    # Validamos si es primer inicio de sesión
    session_control = SesionControl.objects.filter(
        Q(user=request.user)
    )
    for data_session in session_control:
        if data_session.sesion == '1':
            session_flag = 1
        elif data_session.sesion == '2':
            session_flag = 2
        elif data_session.sesion == '3':
            session_flag = 3
        else:
            session_flag = 2

    return render(request, "dashboard/update_service.html", {
        'form': form,
        'session_flag': session_flag,
        'identify_info': identify_info,
        'is_superuser': is_superuser
    })


# View information user view
@login_required()
def v_info_user(request, id_user):
    
    # Obtenemos Identify information
    identify_info = IdentifyInformation.objects.filter(
        Q(user=request.user)
    )
    # Obtenemos instancia de usuario
    user = User.objects.get(id=id_user)
    # Obtenemos la documentacion del socio
    docu = DocumentationUser.objects.filter(
        Q(user=user)
    )
    # Obtenemos Identify information del usuario a modificar
    identify_info_user = IdentifyInformation.objects.filter(
        Q(user=user)
    )
    # Obtenemos General information
    general_info = GeneralInformation.objects.filter(
        Q(user=user)
    )
    # Obtenemos Direccion
    address_info = UserAddressProcess.objects.filter(
        Q(user=user)
    )
    # Obtenemos Number Contact
    number_info = NumberContact.objects.filter(
        Q(user=user),
        Q(status=1)
    )
    # Obtenemos correos alternativos
    altermail_info = AlternativeEmails.objects.filter(
        Q(user=user)
    )
    # Obtenemos datos IMSS
    imss_info = CotImssRelation.objects.filter(
        Q(user=user)
    )
    # Obtenemos actividad economica
    act_eco_info = EconomicActivity.objects.filter(
        Q(user=user),
        Q(status=1)
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
    # Obtenemos datos bnk rec
    bnkrec_info = DataBnkRec.objects.filter(
        Q(user=user)
    )
    # Obtenemos los hijos del usuario
    sons_info = IdentifyInformation.objects.filter(
        Q(upstream_promoter=user.username)
    )

    info_complete = 0
    profile_progress = 0
    REQUIRED_TABLES = 9
    missing_tables = []

    if identify_info:
        info_complete += 1
    else:
        missing_tables.append("Identificación")

    if user:
        info_complete += 1

    if general_info:
        info_complete += 1
    else:
        missing_tables.append("Información general")

    if address_info:
        info_complete += 1
    else:
        missing_tables.append("Domicilio")

    if number_info:
        info_complete += 1
    else:
        missing_tables.append("Contacto")

    # if altermail_info:
    #     info_complete += 1
    # else:
    #     missing_tables.append("Correos alternativos")

    if imss_info:
        info_complete += 1
    else:
        missing_tables.append("Datos de IMSS")

    if act_eco_info:
        info_complete += 1
    else:
        missing_tables.append("Actividad económica del socio")

    # if eco_dependent_info:
    #     info_complete += 1
    # else:
    #     missing_tables.append("Dependientes económicos del socio")

    if reference_info:
        info_complete += 1
    else:
        missing_tables.append("Referencias personales")

    # if bnkrec_info:
    #     info_complete += 1
    # else:
    #     missing_tables.append("Datos de cobro de comisiones")

    if docu:
        info_complete += 1
    else:
        missing_tables.append("Documentación")

    profile_progress = (100 / REQUIRED_TABLES) * info_complete

    validate_contracts = contracts_validation(id_user)

    # VALIDACIÓN DE PAGO PARA ACTIVACIÓN DE NAVBAR

    # Validamos si es superuser
    is_superuser = bool
    if identify_info[0].user_type.user_type == 'Super usuario':
        is_superuser = True
    else:
        is_superuser = False

    # Validamos si es primer inicio de sesión
    session_control = SesionControl.objects.filter(
        Q(user=request.user)
    )
    for data_session in session_control:
        if data_session.sesion == '1':
            session_flag = 1
        elif data_session.sesion == '2':
            session_flag = 2
        elif data_session.sesion == '3':
            session_flag = 3
        else:
            session_flag = 2
    pmnt_status_user_aux = SesionControl.objects.filter(user__id=id_user)
    pmnt_status_user = pmnt_status_user_aux[0].sesion

    return render(request, "dashboard/v_info_user.html", {
        'user': user,
        'docu': docu,
        'identify_info_user': identify_info_user,
        'general_info': general_info,
        'address_info': address_info,
        'number_info': number_info,
        'altermail_info': altermail_info,
        'imss_info': imss_info,
        'act_eco_info': act_eco_info,
        'eco_dependent_info': eco_dependent_info,
        'reference_info': reference_info,
        'bnkrec_info': bnkrec_info,
        'sons_info': sons_info,
        'identify_info': identify_info,
        'info_complete': info_complete,
        'profile_progress': profile_progress,
        'missing_tables': missing_tables,
        'REQUIRED_TABLES': REQUIRED_TABLES,
        'session_flag': session_flag,
        'is_superuser': is_superuser,
        'id_user': id_user,
        'pmnt_status_user': pmnt_status_user,
        'validate_contracts': validate_contracts,

        ### Paciencia, prudencia, verbal continencia, presencia o ausencia según conveniencia ###

    })


# Pre register list view
@login_required()
@staff_member_required
def pre_register_list(request):
    # Obtenemos la instancia de status
    status = Status.objects.get(id=2)
    # Obtenemos Identify information
    identify_info = IdentifyInformation.objects.filter(
        Q(user=request.user)
    )
    # Obtenemos los usuarios de preregistro
    preregis_users = PreRegisterLog.objects.filter(
        Q(status=1)
    )
    # Validamos si los usuarios en pre-registro no tienen identificacion
    # Iteramos en preregis_users donde están todos los usuarios del preregistro
    for data in preregis_users:
        # Validamos si este usuario tiene identificacion
        val_identify = IdentifyInformation.objects.filter(
            Q(user=data.user)
        )
        if val_identify:
            # Si tiene identificacion, cambiamos el status del log
            preregister_log_id = PreRegisterLog.objects.filter(
                Q(user=data.user)
            ).update(
                status=status
            )
    # Obtenemos la lista de usuarios actualizada
    pre_users = PreRegisterLog.objects.filter(
        Q(status=1)
    )

    # VALIDACIÓN DE PAGO PARA ACTIVACIÓN DE NAVBAR

    # Validamos si es superuser
    is_superuser = bool
    if identify_info[0].user_type.user_type == 'Super usuario':
        is_superuser = True
    else:
        is_superuser = False

    # Validamos si es primer inicio de sesión
    session_control = SesionControl.objects.filter(
        Q(user=request.user)
    )
    for data_session in session_control:
        if data_session.sesion == '1':
            session_flag = 1
        elif data_session.sesion == '2':
            session_flag = 2
        elif data_session.sesion == '3':
            session_flag = 3
        else:
            session_flag = 2
    return render(request, "dashboard/pre_registers_list.html", {
        'identify_info': identify_info,
        'pre_users': pre_users,
        'session_flag': session_flag,
        'identify_info': identify_info,
        'is_superuser': is_superuser})


# V_pre_user
@login_required()
@staff_member_required
def v_pre_user(request, id_user):
    # Obtenemos la instancia del usuario
    user = User.objects.get(id=id_user)
    # Obtenemos General information
    general_info = GeneralInformation.objects.filter(
        Q(user=user)
    )
    # Obtenemos Direccion
    address_info = UserAddressProcess.objects.filter(
        Q(user=user)
    )
    # Obtenemos Number Contact
    number_info = NumberContact.objects.filter(
        Q(user=user),
        Q(status=1)
    )
    # Obtenemos correos alternativos
    altermail_info = AlternativeEmails.objects.filter(
        Q(user=user)
    )
    # Obtenemos datos IMSS
    imss_info = CotImssRelation.objects.filter(
        Q(user=user)
    )
    # Obtenemos actividad economica
    act_eco_info = EconomicActivity.objects.filter(
        Q(user=user),
        Q(status=1)
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
    # Obtenemos datos bnk rec
    bnkrec_info = DataBnkRec.objects.filter(
        Q(user=user)
    )

    # VALIDACIÓN DE PAGO PARA ACTIVACIÓN DE NAVBAR

    # Obtenemos Identify information
    identify_info = IdentifyInformation.objects.filter(
        Q(user=request.user)
    )
    # Validamos si es superuser
    is_superuser = bool
    if identify_info[0].user_type.user_type == 'Super usuario':
        is_superuser = True
    else:
        is_superuser = False

    # Validamos si es primer inicio de sesión
    session_control = SesionControl.objects.filter(
        Q(user=request.user)
    )
    for data_session in session_control:
        if data_session.sesion == '1':
            session_flag = 1
        elif data_session.sesion == '2':
            session_flag = 2
        elif data_session.sesion == '3':
            session_flag = 3
        else:
            session_flag = 2

    return render(request, "dashboard/v_pre_user.html", {
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
        'session_flag': session_flag,
        'identify_info': identify_info,
        'is_superuser': is_superuser
    })


# Oficial pages view
@login_required()
def oficial_pages(request):
    # Obtenemos Identify information
    identify_info = IdentifyInformation.objects.filter(
        Q(user=request.user)
    )

    # VALIDACIÓN DE PAGO PARA ACTIVACIÓN DE NAVBAR

    # Validamos si es superuser
    is_superuser = bool
    if identify_info[0].user_type.user_type == 'Super usuario':
        is_superuser = True
    else:
        is_superuser = False

    # Validamos si es primer inicio de sesión
    session_control = SesionControl.objects.filter(
        Q(user=request.user)
    )
    for data_session in session_control:
        if data_session.sesion == '1':
            session_flag = 1
        elif data_session.sesion == '2':
            session_flag = 2
        elif data_session.sesion == '3':
            session_flag = 3
        else:
            session_flag = 2
    return render(request, "dashboard/oficial_pages.html", {
        'identify_info': identify_info,
        'session_flag': session_flag,
        'is_superuser': is_superuser
    })


# Downloads view
@login_required()
def downloads(request):
    # Obtenemos Identify information
    identify_info = IdentifyInformation.objects.filter(
        Q(user=request.user)
    )

    # Creamos el nombre del PDF
    file_card_name = "" + str(request.user.id) + "_" + request.user.username + "_credencial_socio.pdf"

    # VALIDACIÓN DE PAGO PARA ACTIVACIÓN DE NAVBAR

    # Validamos si es superuser
    is_superuser = bool
    if identify_info[0].user_type.user_type == 'Super usuario':
        is_superuser = True
    else:
        is_superuser = False

    # Validamos si es primer inicio de sesión
    session_control = SesionControl.objects.filter(
        Q(user=request.user)
    )
    for data_session in session_control:
        if data_session.sesion == '1':
            session_flag = 1
        elif data_session.sesion == '2':
            session_flag = 2
        elif data_session.sesion == '3':
            session_flag = 3
        else:
            session_flag = 2

    # pdb.set_trace()
    return render(request, "dashboard/downloads.html", {
        'identify_info': identify_info,
        'file_card_name': file_card_name,
        'session_flag': session_flag,
        'is_superuser': is_superuser
    })


# Tutorials View
@login_required()
def tuto_process(request, id_category):
    # Obtenemos Identify information
    identify_info = IdentifyInformation.objects.filter(
        Q(user=request.user)
    )
    # Instancia de la categoria
    category = VideoTutorialsHeader.objects.filter(
        Q(id=id_category)
    )
    for data_category in category:
        # Instancia de los videos de la categoria
        tutorials = VideoTutorials.objects.filter(
            Q(videoheader=data_category)
        )

    # VALIDACIÓN DE PAGO PARA ACTIVACIÓN DE NAVBAR

    # Obtenemos Identify information
    identify_info = IdentifyInformation.objects.filter(
        Q(user=request.user)
    )
    # Validamos si es superuser
    is_superuser = bool
    if identify_info[0].user_type.user_type == 'Super usuario':
        is_superuser = True
    else:
        is_superuser = False

    # Validamos si es primer inicio de sesión
    session_control = SesionControl.objects.filter(
        Q(user=request.user)
    )
    for data_session in session_control:
        if data_session.sesion == '1':
            session_flag = 1
        elif data_session.sesion == '2':
            session_flag = 2
        elif data_session.sesion == '3':
            session_flag = 3
        else:
            session_flag = 2

    return render(request, "dashboard/tuto_process.html", {
        'category': category,
        'tutorials': tutorials,
        'identify_info': identify_info,
        'session_flag': session_flag,
        'identify_info': identify_info,
        'is_superuser': is_superuser
    })


# Related videos view
@login_required()
def related_videos(request):
    # Obtenemos Identify information
    identify_info = IdentifyInformation.objects.filter(
        Q(user=request.user)
    )

    # VALIDACIÓN DE PAGO PARA ACTIVACIÓN DE NAVBAR

    # Validamos si es superuser
    is_superuser = bool
    if identify_info[0].user_type.user_type == 'Super usuario':
        is_superuser = True
    else:
        is_superuser = False

    # Validamos si es primer inicio de sesión
    session_control = SesionControl.objects.filter(
        Q(user=request.user)
    )
    for data_session in session_control:
        if data_session.sesion == '1':
            session_flag = 1
        elif data_session.sesion == '2':
            session_flag = 2
        elif data_session.sesion == '3':
            session_flag = 3
        else:
            session_flag = 2

    return render(request, "dashboard/related_videos.html", {
        'identify_info': identify_info,
        'session_flag': session_flag,
        'identify_info': identify_info,
        'is_superuser': is_superuser
    })


# Digital magazine view
@login_required()
def digital_magazine(request):
    # VALIDACIÓN DE PAGO PARA ACTIVACIÓN DE NAVBAR

    # Obtenemos Identify information
    identify_info = IdentifyInformation.objects.filter(
        Q(user=request.user)
    )
    # Validamos si es superuser
    is_superuser = bool
    if identify_info[0].user_type.user_type == 'Super usuario':
        is_superuser = True
    else:
        is_superuser = False

    # Validamos si es primer inicio de sesión
    session_control = SesionControl.objects.filter(
        Q(user=request.user)
    )
    for data_session in session_control:
        if data_session.sesion == '1':
            session_flag = 1
        elif data_session.sesion == '2':
            session_flag = 2
        elif data_session.sesion == '3':
            session_flag = 3
        else:
            session_flag = 2

    return render(request, "dashboard/digital_magazine.html", {
        'session_flag': session_flag,
        'identify_info': identify_info,
        'is_superuser': is_superuser
    })


# # Pmnt validator view
# @login_required()
# @staff_member_required
# def pmnt_validator(request, id_user):
#     # Obtenemos Identify information
#     identify_info = IdentifyInformation.objects.filter(
#         Q(user=id_user)
#     )
#
#     # Validamos si es primer inicio de sesión
#     session_control = SesionControl.objects.filter(
#         Q(user=id_user)
#     )
#     for data_session in session_control:
#         if data_session.sesion == '1':
#             session_flag = 1
#         elif data_session.sesion == '2':
#             session_flag = 2
#         elif data_session.sesion == '3':
#             session_flag = 3
#         else:
#             session_flag = 3
#
#         # Obtenemos la matriz de usuario
#         general_info = IdentifyInformation.objects.filter(
#             Q(user=id_user)
#         )
#
#     information_list = list()
#     for data in general_info:
#         info_dict = dict()
#         info_dict['id'] = data.user.id
#         info_dict['first_name'] = data.user.first_name
#         info_dict['last_name'] = data.user.last_name
#         info_dict['username'] = data.user.username
#         info_dict['status_user'] = data.user.is_active
#
#         promotor = User.objects.filter(username=data.upstream_promoter)
#         director = User.objects.get(username=data.ceo)
#
#         info_dict['upstream_promoter'] = promotor[0].get_full_name()
#         info_dict['ceo'] = director.get_full_name()
#
#
#     return render(request, "dashboard/pmnt_validator.html", {
#         'session_flag': session_flag,
#         'identify_info': identify_info,
#         'gen_info': info_dict,
#
#     })


# Pmnt validator class

class Pmnt_validator(ListView):

    @method_decorator(login_required)
    @method_decorator(staff_member_required())
    def get(self, request, *args, **kwargs):

        # Obtenemos informacion User
        user = User.objects.filter(
            Q(id=self.kwargs['id_user'])
        )

        # Obtenemos Identify information
        identify_info = IdentifyInformation.objects.filter(
            Q(user=self.kwargs['id_user'])
        )

        # Validamos status de pago del usuario seleccionado
        pmnt_session_control = SesionControl.objects.filter(
            Q(user=self.kwargs['id_user'])
            # Q(user=request.user.id) #Para obtener id de usuario logueado
        )
        for data_session in pmnt_session_control:
            if data_session.sesion == '1':
                pmnt_session_flag = 1
            elif data_session.sesion == '2':
                pmnt_session_flag = 2
            elif data_session.sesion == '3':
                pmnt_session_flag = 3
            else:
                pmnt_session_flag = 2

        # Obtenemos la matriz de usuario
        general_info = IdentifyInformation.objects.filter(
            Q(user=self.kwargs['id_user'])
        )

        for data in general_info:
            info_dict = dict()
            info_dict['id'] = data.user.id
            info_dict['first_name'] = data.user.first_name
            info_dict['last_name'] = data.user.last_name
            info_dict['username'] = data.user.username
            info_dict['status_user'] = data.user.is_active

        return render(request, "dashboard/pmnt_validator.html", {
            'pmnt_session_flag': pmnt_session_flag,
            'identify_info': identify_info,
            'gen_info': info_dict,
        })

    def post(self, request, *args, **kwargs):
        pmnt = request.POST['pmnt']
        data = {}
        if pmnt == 'false':
            change_session_control(self.kwargs['id_user'], 2)
        else:
            change_session_control(self.kwargs['id_user'], 3)
        # pdb.set_trace()
        return JsonResponse(data)


# QR Code generate
def create_qrcode(url, nss):
    # Creamos el nombre de la img
    qr_name = 'QR_' + nss + '.jpg'

    # Validamos si existe la img
    if not os.path.isfile(os.path.join(settings.MEDIA_ROOT, qr_name)):
        # Generamos el QR con el enlace
        qr = qrcode.QRCode(
            version=10,
            box_size=3,
            border=0
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        img.save(os.path.join(settings.MEDIA_ROOT, qr_name))

    return qr_name


# Link register
@login_required()
def invitation_code(request):
    # Creamos el URL personalizado
    url_custom = 'https://gcs-coop.com.mx/process_coop/nuevo-registro/' + request.user.username

    # Creamos el QR y obtenemos el nombre
    qr_name = create_qrcode(url_custom, request.user.username)

    return render(request, "dashboard/invitation_code.html", {'url_custom': url_custom, 'qr_name': qr_name})
