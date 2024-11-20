# importaciones de funcionalidades
from django.db.models import Q
import base64
from datetime import datetime
from login.forms import FormEditarUsuario

# importaciones de los modelos de cada una de las aplicaciones
from estudiante.models import (
    ModelFechasProyecto,
    ModelProyectoFinal,
    ModelAsignacionJurados,
    ModelAnteproyecto,
)
from director.models import *
from correspondencia.models import (
    ModelDocumentos,
    ModelFechasComite,
    ModelSolicitudes,
    ModelInformacionEntregaFinal,
    ModelRetroalimentaciones,
    ModelDocumentos,
)
from django.contrib.auth.decorators import login_required

# funcion de recuperar documento binario


@login_required
def datosusuario(request):

    usuario = request.user
    imagen = usuario.imagen
    imagen_convertida = base64.b64encode(imagen).decode("utf-8") if imagen else ""
    form_editar_usuario = FormEditarUsuario(instance=usuario)
    fechas_comite = recuperar_fechas_comite()
    ano_actual = datetime.now().year

    context = {
        "ano_actual": ano_actual,
        "fechas_comite": fechas_comite,
        "form_config": form_editar_usuario,
        "usuario": usuario,
        "user_img": imagen_convertida,
    }
    return context


def recuperar_evaluacion_proyecto_final(id):
    evaluacion = (
        ModelEvaluacionProyectoFinal.objects.get(id=id)
        if ModelEvaluacionProyectoFinal.objects.filter(id=id).exists()
        else None
    )
    return evaluacion


def recuperar_documento(documento):
    documento = base64.b64encode(documento).decode("utf-8") if documento else None
    return documento


def recuperar_num_respuestas():
    num_respuestas = ModelRetroalimentaciones.objects.all().count()
    return num_respuestas


def recuperar_num_proyectos_terminados():
    num_proyectos = ModelProyectoFinal.objects.filter(estado=True).count()
    return num_proyectos


def recuperar_num_proyectos_pendientes():
    num_proyectos_pendientes = ModelProyectoFinal.objects.filter(estado=False).count()
    return num_proyectos_pendientes


def recuperar_num_solicitudes():
    num_solicitudes = ModelSolicitudes.objects.filter(estado=False).count()
    num_anteproyectos = ModelAnteproyecto.objects.filter(
        Q(solicitud_enviada=True) & Q(estado=False)
    ).count()
    num_proyectos_finales = ModelProyectoFinal.objects.filter(
        Q(solicitud_enviada=True) & Q(estado=False)
    ).count()
    print(num_solicitudes)
    print(num_anteproyectos)
    print(num_proyectos_finales)
    suma = num_solicitudes + num_anteproyectos + num_proyectos_finales
    return suma


def recuperar_num_formatos_comite():
    num_formatos = ModelDocumentos.objects.all().count()
    return num_formatos


#######################################################################################################

# revisar


def recuperar_proyectos_pendientes():

    proyectos_finales = ModelProyectoFinal.objects.filter(
        Q(Q(solicitud_enviada=False) & Q(estado=False))
        | Q(Q(solicitud_enviada=True) & Q(estado=False))
    )
    if proyectos_finales:
        return proyectos_finales
    else:
        return None


def recuperar_proyectos_finalizados():

    proyectos_finalizados = ModelInformacionEntregaFinal.objects.all()
    if not proyectos_finalizados:
        proyectos_finalizados = None
    return proyectos_finalizados


def recuperar_proyecto_finalizado(id):
    proyecto = (
        ModelProyectoFinal.objects.get(id=id)
        if ModelProyectoFinal.objects.filter(id=id).exists()
        else None
    )
    return proyecto


def recuperar_proyecto_actual(id):
    proyecto = (
        ModelProyectoFinal.objects.get(id=id)
        if ModelProyectoFinal.objects.filter(id=id).exists()
        else None
    )
    return proyecto


def recuperar_solicitudes_especiales_proyecto(proyecto, anteproyecto):
    solicitudes_especiales_proyecto = ModelSolicitudes.objects.filter(
        Q(proyecto_final=proyecto) | Q(anteproyecto=anteproyecto)
    )
    print(solicitudes_especiales_proyecto.count())
    return solicitudes_especiales_proyecto


def recuperar_fechas_proyecto(proyecto):
    fechas = (
        ModelFechasProyecto.objects.get(proyecto_final=proyecto)
        if ModelFechasProyecto.objects.filter(proyecto_final=proyecto).exists()
        else None
    )
    return fechas


def recuperar_fechas_comite():
    fecha_actual = datetime.now()
    mes_actual = fecha_actual.month
    if mes_actual <= 6:
        periodo_academico_actual = int(1)
    else:
        periodo_academico_actual = int(2)

    fechas = (
        ModelFechasComite.objects.get(periodo_academico=int(periodo_academico_actual))
        if ModelFechasComite.objects.filter(
            periodo_academico=int(periodo_academico_actual)
        ).exists()
        else None
    )

    if fechas:
        return fechas
    else:

        return None


#######################################################################################################
# recuperacion de los documentos cargados por el comite


def recuperar_formatos():
    documentos_model = ModelDocumentos.objects.all()
    documentos = {}
    if documentos_model:
        for i, documento in enumerate(documentos_model):
            documento_binario = documento.documento
            documento_convert = recuperar_documento(documento_binario)
            documentos[f"documento{i}"] = {
                "id": documento.id,
                "nombre_documento": documento.nombre_documento,
                "descripcion": documento.descripcion,
                "version": documento.version,
                "documento": documento_convert,
                "fecha_cargue": documento.fecha_cargue,
            }
    else:
        documentos = None

    return documentos


def num_evaluaciones_anteproyecto_director(user):
    num_evaluaciones_anteproyectos = ModelEvaluacionAnteproyecto.objects.filter(
        evaluador=user
    ).count()
    return num_evaluaciones_anteproyectos


def num_evaluaciones_proyecto_final_director(user):
    num_evaluaciones_final = ModelEvaluacionProyectoFinal.objects.filter(
        jurado=user
    ).count()
    return num_evaluaciones_final


def num_evaluaciones_anteproyecto_hechas_director(user):
    num_evaluaciones_anteproyectos = ModelEvaluacionAnteproyecto.objects.filter(
        Q(evaluador=user) & Q(estado=True)
    ).count()
    return num_evaluaciones_anteproyectos


def num_evaluaciones_proyecto_final_hechas_director(user):
    num_evaluaciones_final = ModelEvaluacionProyectoFinal.objects.filter(
        Q(jurado=user) & Q(estado=True)
    ).count()
    return num_evaluaciones_final


def num_evaluaciones_anteproyecto_pendientes_director(user):
    num_evaluaciones_anteproyectos = ModelEvaluacionAnteproyecto.objects.filter(
        Q(evaluador=user) & Q(estado=False)
    ).count()
    return num_evaluaciones_anteproyectos


def num_evaluaciones_proyecto_final_pendientes_director(user):
    num_evaluaciones_final = ModelEvaluacionProyectoFinal.objects.filter(
        Q(jurado=user) & Q(estado=False)
    ).count()
    return num_evaluaciones_final


def num_anteproyecto_pendientes_director(user):
    num_anteproyectos = ModelAnteproyecto.objects.filter(
        Q(director=user.nombre_completo)
        | Q(codirector=user.nombre_completo) & Q(estado=False)
    ).count()
    return num_anteproyectos


def num_anteproyecto_aprobados_director(user):
    num_anteproyectos = ModelAnteproyecto.objects.filter(
        Q(director=user.nombre_completo)
        | Q(codirector=user.nombre_completo) & Q(estado=True)
    ).count()
    return num_anteproyectos


def num_proyecto_final_pendientes_director(user):
    num_proyectos_finales = ModelProyectoFinal.objects.filter(
        Q(anteproyecto__director=user.nombre_completo)
        | Q(anteproyecto__codirector=user.nombre_completo) & Q(estado=False)
    ).count()
    return num_proyectos_finales


def num_proyecto_final_terminados_director(user):
    num_proyectos_finales = ModelProyectoFinal.objects.filter(
        Q(anteproyecto__director=user.nombre_completo)
        | Q(anteproyecto__codirector=user.nombre_completo) & Q(estado=True)
    ).count()
    return num_proyectos_finales


def num_anteproyecto_director(user):
    num_anteproyecto = ModelAnteproyecto.objects.filter(
        Q(director=user.nombre_completo)
        | Q(codirector=user.nombre_completo) & Q(Q(estado=False) | Q(estado=True))
    ).count()
    return num_anteproyecto


def num_proyecto_final_director(user):
    num_proyectos_finales = ModelProyectoFinal.objects.filter(
        (
            Q(anteproyecto__codirector=user)
            | Q(anteproyecto__director=user.nombre_completo)
        )
        & Q(Q(estado=True) | Q(estado=False))
    ).count()
    return num_proyectos_finales
