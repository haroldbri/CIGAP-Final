from datetime import datetime
from django.shortcuts import redirect
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.contrib.auth.decorators import login_required
from login.models import Usuarios
from django.contrib.auth import login as auth_login
import base64
from django.contrib import messages
from django.db.models import Q

# importacion de las funcionalidaes
from plataform_CIGAP.utils.decoradores import grupo_usuario
from plataform_CIGAP.utils.funcionalidades_fechas import (
    fecha_actual,
    fecha_maxima_respuesta,
)

# importacion de la vista del login que permite cambiar la informacion de ususario
from login.views import editar_usuario
from login.forms import FormEditarUsuario

# Create your views here.

# formulario de retroalimentaciones de correspondencia
from correspondencia.forms import FormObservacionAnteproyecto, FormObservacionProyecto
from correspondencia.views import recuperar_anteproyecto

# importacion de los modelos
from .models import ModelEvaluacionAnteproyecto, ModelEvaluacionProyectoFinal

# importacion de modelos de los estudinates
from estudiante.models import (
    ModelAnteproyecto,
    ModelProyectoFinal,
    ModelObjetivoGeneral,
    ModelObjetivosEspecificos,
    ModelActividades,
    ModelFechasProyecto,
)

# impotacion de recuperaciones
from plataform_CIGAP.utils.recuperaciones import (
    num_anteproyecto_aprobados_director,
    num_anteproyecto_director,
    num_anteproyecto_pendientes_director,
    num_evaluaciones_anteproyecto_director,
    num_evaluaciones_anteproyecto_hechas_director,
    num_evaluaciones_anteproyecto_pendientes_director,
    num_evaluaciones_proyecto_final_director,
    num_evaluaciones_proyecto_final_hechas_director,
    num_evaluaciones_proyecto_final_pendientes_director,
    num_proyecto_final_director,
    num_proyecto_final_pendientes_director,
    num_proyecto_final_terminados_director,
    recuperar_evaluacion_proyecto_final,
    recuperar_fechas_comite,
    recuperar_formatos,
    datosusuario,
)

# datos del usuario


@login_required
def datos_usuario_director(request):
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


#############################################################################################################


def recuperar_actividad(id):
    actividad = (
        ModelActividades.objects.get(id=id)
        if ModelActividades.objects.filter(id=id).exists()
        else None
    )
    return actividad


@login_required
@grupo_usuario("Directores")
def recuperar_proyectos_evaluador(request):
    usuario = request.user
    nombre_usuario = usuario.nombre_completo
    proyectos = ModelProyectoFinal.objects.filter(
        Q(anteproyecto__director=nombre_usuario)
        | Q(anteproyecto__codirector=nombre_usuario)
    )
    if not proyectos:
        return None
    return proyectos


def recuperar_evaluacion_anteproyecto(anteproyecto, request):
    usuario = request.user
    evaluacion = ModelEvaluacionAnteproyecto.objects.get(
        Q(anteproyecto=anteproyecto) & Q(evaluador=usuario)
    )
    if not evaluacion:
        return None
    return evaluacion


def recuperar_documento(documento):
    documento = base64.b64encode(documento).decode("utf-8") if documento else None
    return documento


@login_required
@grupo_usuario("Directores")
def recuperar_anteproyectos_a_evaluar(request):
    usuario = request.user
    ante_a_evaluar = ModelEvaluacionAnteproyecto.objects.filter(
        Q(evaluador=usuario) & Q(anteproyecto__estado=False)
    )
    if not ante_a_evaluar:
        return None
    return ante_a_evaluar


@login_required
@grupo_usuario("Directores")
def recuperar_anteproyectos(request):
    usuario = request.user
    anteproyectos = ModelAnteproyecto.objects.filter(
        (Q(director=usuario.nombre_completo) | Q(codirector=usuario.nombre_completo))
        & Q(estado=False)
    )
    if not anteproyectos.exists():
        anteproyectos = None

    return anteproyectos


def recuperar_anteproyecto(id):
    anteproyecto = (
        ModelAnteproyecto.objects.get(id=id)
        if ModelAnteproyecto.objects.filter(id=id).exists()
        else None
    )
    return anteproyecto


@login_required
@grupo_usuario("Directores")
def recuperar_proyectos(request):
    usuario = request.user
    proyectos = ModelProyectoFinal.objects.filter(
        (
            Q(anteproyecto__director=usuario.nombre_completo)
            | Q(anteproyecto__codirector=usuario.nombre_completo)
        )
        & Q(estado=False)
    )
    print(proyectos)
    if not proyectos:
        return None
    return proyectos


def recuperar_proyecto(id):
    proyecto = (
        ModelProyectoFinal.objects.get(id=id)
        if ModelProyectoFinal.objects.filter(id=id).exists()
        else None
    )
    if not proyecto:
        return None
    return proyecto


#############################################################################################################


@login_required
@grupo_usuario("Directores")
def principal_director(request):

    usuario = request.user
    imagen = usuario.imagen
    imagen_convertida = base64.b64encode(imagen).decode("utf-8") if imagen else ""
    grupos = usuario.groups.all()
    if request.method == "POST":
        editar_usuario(request)
    else:
        form = FormEditarUsuario(instance=usuario)
        return render(
            request,
            "director/base_director.html",
            {"form_config": form, "usuario": usuario, "user_img": imagen_convertida, "grupos":grupos},
        )


# def base_director(request):
#     usuario = request.user
#     # recuperacion de la imagen propia del usuaario en formato binario
#     # print(imagen, 'esta es la imagen')
#     imagen = usuario.imagen
#     imagen_convertida = base64.b64encode(imagen).decode('utf-8') if imagen else ''

#     if request.method == 'POST':
#         form = FormEditarUsuario(request.POST, request.FILES, instance=usuario)
#         if form.is_valid():
#             user = form.save()


@login_required
@grupo_usuario("Directores")
def view_anteproyectos(request):
    context = datos_usuario_director(request)
    anteproyectos = recuperar_anteproyectos(request)
    if anteproyectos:
        context["anteproyectos"] = anteproyectos
    return render(request, "director/anteproyectos/anteproyectos.html", context)


@login_required
@grupo_usuario("Directores")
def anteproyecto(request, id):
    context = datosusuario(request)
    anteproyecto = recuperar_anteproyecto(id)
    context["anteproyecto"] = anteproyecto
    if anteproyecto:
        if anteproyecto.fecha_envio:
            context["fecha_respuesta_maxima"] = fecha_maxima_respuesta(
                anteproyecto.fecha_envio
            )
        doc_anteproyecto = recuperar_documento(anteproyecto.anteproyecto)
        doc_carta_presentacion = recuperar_documento(anteproyecto.carta_presentacion)
        context["doc_anteproyecto"] = doc_anteproyecto
        context["doc_carta_presentacion"] = doc_carta_presentacion

    if request.method == "POST":
        formulario_observacion = FormObservacionAnteproyecto(
            request.POST, request.FILES
        )

        if formulario_observacion.is_valid():

            retroalimentacion = formulario_observacion.save(commit=False)
            retroalimentacion.user = request.user
            retroalimentacion.anteproyecto = anteproyecto
            retroalimentacion.fecha_retroalimentacion = fecha_actual()

            retroalimentacion.save()

            messages.success(request, "La retroalimentación se envió correctamente.")

        else:
            messages.error(
                request,
                f"Hubo un error al enviar la retroalimentación. Por favor, revise los campos. {formulario_retroalimentacion.errors}",
            )

    else:
        formulario_retroalimentacion = FormObservacionAnteproyecto()
        context["from_retroalimentacion"] = formulario_retroalimentacion
    return render(request, "director/anteproyectos/anteproyecto.html", context)


@login_required
@grupo_usuario("Directores")
def eliminar_anteproyecto(request, id):
    anteproyecto = ModelAnteproyecto.objects.get(id=id)
    anteproyecto.delete()
    messages.success(
        request,
        f'Su participación en el anteproyecto "{anteproyecto.nombre_anteproyecto}" ha sido eliminada.',
    )
    return redirect("director:view_anteproyectos")


@login_required
@grupo_usuario("Directores")
def enviar_anteproyecto(request, id):
    anteproyecto = recuperar_anteproyecto(id)
    if anteproyecto.solicitud_enviada == True:
        messages.error(
            request,
            f'El anteproyecto "{anteproyecto.nombre_anteproyecto}" ya fue enviado al comité el {anteproyecto.fecha_envio}. Por favor, esté atento a posibles respuestas.',
        )
        return redirect("director:anteproyecto", id=id)
    if anteproyecto:
        anteproyecto.solicitud_enviada = True
        anteproyecto.fecha_envio = fecha_actual()
        anteproyecto.save()
        messages.success(
            request,
            f'El anteproyecto "{anteproyecto.nombre_anteproyecto}" ha sido enviado al comité. Por favor, esté atento a posibles respuestas.',
        )
        return redirect("director:anteproyecto", id=id)
    else:
        messages.error(request, "No se pudo encontrar el anteproyecto especificado.")
        return redirect("director:anteproyecto", id=id)


#############################################################################################################


#############################################################################################################
# configuracion de las vistas del modulo de proyectos


def recuperar_objetivo_general(id_gen):
    objetivo_general = (
        ModelObjetivoGeneral.objects.get(id=id_gen)
        if ModelObjetivoGeneral.objects.filter(id=id_gen)
        else None
    )
    return objetivo_general


def recuperar_objetivo_especifico(id):
    obj_especifico = ModelObjetivosEspecificos.objects.get(id=id)
    if not obj_especifico:
        return None
    return obj_especifico


@login_required
@grupo_usuario("Directores")
def view_proyectos(request):
    context = datos_usuario_director(request)
    proyectos = recuperar_proyectos(request)
    if proyectos:
        context["proyectos"] = proyectos

    return render(request, "director/proyectos/proyectos.html", context)


@login_required
@grupo_usuario("Directores")
def proyecto(request, id):
    context = datosusuario(request)
    proyecto = recuperar_proyecto(id)

    if proyecto:
        context["proyecto_final"] = proyecto
        doc_proyecto_final = recuperar_documento(proyecto.proyecto_final)
        doc_carta_presentacion_final = recuperar_documento(
            proyecto.carta_presentacion_final
        )
        context["doc_proyecto_final"] = doc_proyecto_final
        context["doc_carta_presentacion_final"] = doc_carta_presentacion_final
        objetivo_general = (
            ModelObjetivoGeneral.objects.get(proyecto_final=proyecto)
            if ModelObjetivoGeneral.objects.filter(proyecto_final=proyecto).exists()
            else None
        )
        objetivos_especificos = (
            ModelObjetivosEspecificos.objects.filter(objetivo_general=objetivo_general)
            if ModelObjetivosEspecificos.objects.filter(
                objetivo_general=objetivo_general
            ).exists()
            else None
        )
        actividades = ModelActividades.objects.filter(objetivo_general=objetivo_general)
        print(proyecto, objetivo_general, objetivos_especificos, actividades)
        if objetivo_general:
            dict_documentos_avance = {}
            if objetivos_especificos:
                num_obj_especificos = objetivos_especificos.count()
                contador_aprovados = 0
                for i, objetivo_especifico in enumerate(objetivos_especificos):
                    if objetivo_especifico.estado:
                        contador_aprovados += 1
                    if objetivo_especifico.documento_avance:
                        dict_documentos_avance[f"doc_avance{i}"] = recuperar_documento(
                            objetivo_especifico.documento_avance
                        )
                if num_obj_especificos == contador_aprovados:
                    messages.success(
                        request,
                        "El desarrollo de los objetivos específicos ha sido aceptado satisfactoriamente. Ahora puede proceder a enviar la solicitud de proyecto de final al comité para su revisión y posterior aprobación.",
                    )
                    context["puede_enviar"] = True
                context["objetivos_especificos"] = objetivos_especificos

            context["docs_avances"] = dict_documentos_avance
            context["objetivo_general"] = objetivo_general
            context["actividades"] = actividades

    if request.method == "POST":
        formulario_observacion = FormObservacionProyecto(request.POST, request.FILES)

        if formulario_observacion.is_valid():

            retroalimentacion = formulario_observacion.save(commit=False)
            retroalimentacion.proyecto_final = proyecto
            retroalimentacion.user = request.user
            retroalimentacion.fecha_retroalimentacion = fecha_actual()
            retroalimentacion.estado = None
            retroalimentacion.save()

            messages.success(request, "La retroalimentación se envió correctamente.")
            return redirect("director:proyecto", id=proyecto.id)

        else:
            messages.error(
                request,
                f"Hubo un error al enviar la retroalimentación. Por favor, revise los campos. {formulario_retroalimentacion.errors}",
            )
            return redirect("director:proyecto", id=proyecto.id)

    else:
        formulario_observacion = FormObservacionProyecto()
        context["from_retroalimentacion"] = formulario_observacion
    return render(request, "director/proyectos/proyecto.html", context)


@login_required
@grupo_usuario("Directores")
def enviar_proyecto(request, id):
    proyecto = recuperar_proyecto(id)
    if proyecto.solicitud_enviada == True:
        messages.error(
            request,
            f'El proyecto "{proyecto.anteproyecto.nombre_anteproyecto}" ya fue enviado al comité el {proyecto.fecha_envio}. Por favor, esté atento a posibles respuestas.',
        )
        return redirect("director:proyecto", id=id)
    if proyecto:
        proyecto.solicitud_enviada = True
        proyecto.fecha_envio = fecha_actual()
        proyecto.save()
        messages.success(
            request,
            f'El proyecto "{proyecto.anteproyecto.nombre_anteproyecto}" ha sido enviado al comité. Por favor, esté atento a posibles respuestas.',
        )
        return redirect("director:proyecto", id=id)
    else:
        messages.error(request, "No se pudo encontrar el proyecto especificado.")
        return redirect("director:proyecto", id=id)

    # funcion para actualizar el estado de la actividad


@login_required
@grupo_usuario("Directores")
def enviar_observacion_objetivo(request, id_proyect, id_esp):
    proyecto = recuperar_proyecto(id_proyect)
    obj_especifico = recuperar_objetivo_especifico(id_esp)

    if request.method == "POST":
        if obj_especifico:
            observaciones = request.POST.get("observaciones")
            documento = request.FILES.get("doc_retroalimentacion")

            if not documento or documento.content_type != "application/pdf":
                messages.warning(
                    request,
                    "No se ha subido un archivo PDF válido. Por favor, suba un archivo PDF.",
                )
                return redirect("director:proyecto", id=proyecto.id)

            obj_especifico.observaciones = observaciones
            obj_especifico.user = request.user
            obj_especifico.proyecto_final = proyecto
            obj_especifico.documento_correcciones = documento.read()
            obj_especifico.documento_avance = documento.read()
            obj_especifico.fecha_observacion = fecha_actual()
            obj_especifico.save()

            messages.success(request, "Las observaciones se han enviado correctamente.")
            return redirect("director:proyecto", id=proyecto.id)
        else:
            messages.error(request, "No se pudo encontrar el objetivo específico.")
            return redirect("director:proyecto", id=proyecto.id)

    messages.error(request, "Método no permitido. Solo se permiten solicitudes POST.")
    return redirect("director:proyecto", id=proyecto.id)


@login_required
@grupo_usuario("Directores")
def actualizar_estado_objetivo_especifico(request, id_proyect, id_esp):
    proyecto = recuperar_proyecto(id_proyect)
    objetivo_especifico = recuperar_objetivo_especifico(id_esp)
    objetivo_especifico.estado = not objetivo_especifico.estado
    objetivo_especifico.save()
    if objetivo_especifico.estado:
        messages.success(
            request, "El estado del objetivo específico se ha actualizado exitosamente."
        )
        return redirect("director:proyecto", id=proyecto.id)
    else:
        messages.success(
            request, "El estado del objetivo específico se ha actualizado exitosamente."
        )
        return redirect("director:proyecto", id=proyecto.id)


@login_required
@grupo_usuario("Directores")
def actualizar_estado_actividad(request, actividad_id, id_proyecto):

    try:
        actividad = ModelActividades.objects.get(id=actividad_id)
        actividad.estado = not actividad.estado
        actividad.save()

        messages.success(
            request,
            f"La actividad '{actividad.descripcion}' ha sido actualizada correctamente.",
        )
    except ModelActividades.DoesNotExist:
        messages.error(request, "La actividad que intentas actualizar no existe.")
    return redirect("director:proyecto", id=id_proyecto)


#############################################################################################################


#############################################################################################################
# configuracion de las vistas del modulo de anteproyecto
def recuperar_anteproyectos_para_evaluar(usuario):
    anteproyectos = ModelEvaluacionAnteproyecto.objects.filter(evaluador=usuario)
    if not anteproyectos:
        return None
    return anteproyectos


def recuperar_proyectos_finales_para_evaluar(usuario):
    proyectos_finales = ModelEvaluacionProyectoFinal.objects.filter(jurado=usuario)
    if not proyectos_finales:
        return None
    return proyectos_finales


@login_required
@grupo_usuario("Directores")
def evaluacion_proyectos(request):
    usuario = request.user
    context = datos_usuario_director(request)
    evaluaciones_anteproyecto_pendientes = (
        num_evaluaciones_anteproyecto_pendientes_director(usuario)
    )
    print(
        "Evaluaciones de anteproyecto pendientes:", evaluaciones_anteproyecto_pendientes
    )

    evaluaciones_proyecto_final_pendientes = (
        num_evaluaciones_proyecto_final_pendientes_director(usuario)
    )
    print(
        "Evaluaciones de proyecto final pendientes:",
        evaluaciones_proyecto_final_pendientes,
    )
    if evaluaciones_anteproyecto_pendientes:
        context["evaluaciones_anteproyecto_pendientes"] = (
            evaluaciones_anteproyecto_pendientes
        )
    if evaluaciones_proyecto_final_pendientes:
        context["evaluaciones_proyecto_final_pendientes"] = (
            evaluaciones_proyecto_final_pendientes
        )
    return render(request, "director/evaluacion_proyectos/eva_proyectos.html", context)


@login_required
@grupo_usuario("Directores")
def view_evaluador_anteproyectos(request):
    context = datos_usuario_director(request)
    anteproyectos = recuperar_anteproyectos_a_evaluar(request)
    print(anteproyecto)
    if anteproyectos:
        context["anteproyectos"] = anteproyectos
    return render(request, "director/evaluacion_proyectos/list_evaluador.html", context)


@login_required
@grupo_usuario("Directores")
def evaluar_anteproyecto(request, id):
    context = datos_usuario_director(request)
    anteproyecto = recuperar_anteproyecto(id)
    if anteproyecto:
        evaluacion = recuperar_evaluacion_anteproyecto(anteproyecto, request)
        if evaluacion:
            documento_evaluacion = recuperar_documento(
                evaluacion.doc_evaluacion_anteproyecto
            )
            context["doc_evaluacion_anteproyecto"] = documento_evaluacion
            context["evaluacion"] = evaluacion
        context["anteproyecto"] = anteproyecto
        doc_anteproyecto = recuperar_documento(anteproyecto.anteproyecto)
        context["doc_anteproyecto"] = doc_anteproyecto
    return render(request, "director/evaluacion_proyectos/anteproyecto.html", context)


@login_required
@grupo_usuario("Directores")
def enviar_evaluacion(request, id):
    context = datos_usuario_director(request)
    anteproyecto = recuperar_anteproyecto(id)
    if anteproyecto:
        evaluacion_anteproyecto = recuperar_evaluacion_anteproyecto(
            anteproyecto, request
        )
        if evaluacion_anteproyecto:

            evaluacion_anteproyecto.calificacion = request.POST.get("calificacion")
            evaluacion_anteproyecto.comentarios = request.POST.get("comentarios")
            evaluacion_anteproyecto.estado = True
            doc_retro = request.FILES.get("doc_retroalimentacion_convert")

            if doc_retro:
                evaluacion_anteproyecto.doc_evaluacion_anteproyecto = doc_retro.read()

            evaluacion_anteproyecto.fecha_evaluacion = fecha_actual()
            evaluacion_anteproyecto.save()

            messages.success(
                request,
                f'La evaluación del anteproyecto "{anteproyecto.nombre_anteproyecto}" ha sido guardada con la calificación {evaluacion_anteproyecto.calificacion}.',
            )

            return redirect("director:evaluar_anteproyecto", id=id)

        else:
            messages.error(
                request,
                f'No se encontró la evaluación para el anteproyecto "{anteproyecto.nombre_anteproyecto}".',
            )

    else:
        messages.error(request, f"El anteproyecto con ID {id} no existe.")

    return redirect("director:evaluar_anteproyecto", id=id)


@login_required
@grupo_usuario("Directores")
def eliminar_evaluacion(request, id):
    evaluacion = (
        ModelEvaluacionAnteproyecto.objects.get(id=id)
        if ModelEvaluacionAnteproyecto.objects.filter(id=id).exists()
        else None
    )
    if evaluacion:
        evaluacion.delete()
        messages.success(request, "La evaluación ha sido eliminada exitosamente.")
    else:
        messages.error(request, "No se encontró la evaluación especificada.")
    return redirect("director:view_evaluador_anteproyectos")


def recuperar_proyectos_jurado(usuario):
    evaluaciones = ModelEvaluacionProyectoFinal.objects.filter(
        Q(jurado=usuario) & Q(estado=False)
    )
    return evaluaciones


@login_required
@grupo_usuario("Directores")
def view_jurado(request):
    context = datos_usuario_director(request)
    proyectos_evaluar = recuperar_proyectos_jurado(request.user)
    if proyectos_evaluar:
        context["proyectos_a_evaluar"] = proyectos_evaluar

    return render(request, "director/evaluacion_proyectos/list_jurado.html", context)


@login_required
@grupo_usuario("Directores")
def evaluar_proyecto_final(request, id):
    context = datosusuario(request)

    evaluacion = recuperar_evaluacion_proyecto_final(id)
    print(evaluacion)

    if evaluacion:
        context["evaluacion"] = evaluacion
        context["doc_evaluacion_proyecto_final"] = recuperar_documento(
            evaluacion.doc_evaluacion_proyecto
        )
    doc_proyecto_final = recuperar_documento(evaluacion.proyecto_final.proyecto_final)
    if doc_proyecto_final:
        context["doc_proyecto_final"] = doc_proyecto_final
        context["proyecto_final"] = evaluacion.proyecto_final
    return render(request, "director/evaluacion_proyectos/proyecto.html", context)


@login_required
@grupo_usuario("Directores")
def enviar_evaluacion_proyecto_final(request, id):
    evaluacion = recuperar_evaluacion_proyecto_final(id)
    proyecto = evaluacion.proyecto_final

    if proyecto:

        if evaluacion:
            comentarios = request.POST.get("comentarios")
            estado = True
            calificacion = request.POST.get("calificacion")
            doc_retroalimentacion_convert = request.FILES.get(
                "doc_retroalimentacion_convert"
            )

            if not all(
                [comentarios, estado, calificacion, doc_retroalimentacion_convert]
            ):
                messages.error(
                    request,
                    "Todos los campos son obligatorios para enviar la evaluación.",
                )
                return redirect("director:evaluar_proyecto_final", id=evaluacion.id)

            try:
                evaluacion.comentarios = comentarios
                evaluacion.estado = estado
                evaluacion.fecha_evaluacion = fecha_actual()
                evaluacion.calificacion = float(calificacion)
                evaluacion.doc_evaluacion_proyecto = (
                    doc_retroalimentacion_convert.read()
                )
                evaluacion.save()

                messages.success(request, "La evaluación se ha enviado correctamente.")
            except Exception as e:
                messages.error(request, f"Error al enviar la evaluación: {e}")

            return redirect("director:evaluar_proyecto_final", id=evaluacion.id)

        else:
            messages.error(
                request, "No se encontró una evaluación para este proyecto final."
            )
            return redirect("director:evaluar_proyecto_final", id=proyecto.id)

    else:
        messages.error(request, "No se encontró el proyecto final solicitado.")
        return redirect("director:evaluar_proyecto_final", id=id)


@login_required
@grupo_usuario("Directores")
def carga(request):
    context = datosusuario(request)
    usuario = request.user
    num_evaluaciones_anteproyecto = num_evaluaciones_anteproyecto_director(usuario)
    print("Número de evaluaciones de anteproyecto:", num_evaluaciones_anteproyecto)

    num_evaluaciones_proyecto = num_evaluaciones_proyecto_final_director(usuario)
    print("Número de evaluaciones de proyecto:", num_evaluaciones_proyecto)

    evaluaciones_anteproyecto_pendientes = (
        num_evaluaciones_anteproyecto_pendientes_director(usuario)
    )
    print(
        "Evaluaciones de anteproyecto pendientes:", evaluaciones_anteproyecto_pendientes
    )

    evaluaciones_proyecto_final_pendientes = (
        num_evaluaciones_proyecto_final_pendientes_director(usuario)
    )
    print(
        "Evaluaciones de proyecto final pendientes:",
        evaluaciones_proyecto_final_pendientes,
    )

    evaluaciones_anteproyecto_hechas = num_evaluaciones_anteproyecto_hechas_director(
        usuario
    )
    print("Evaluaciones de anteproyecto hechas:", evaluaciones_anteproyecto_hechas)

    evaluaciones_proyecto_final_hechas = (
        num_evaluaciones_proyecto_final_hechas_director(usuario)
    )
    print("Evaluaciones de proyecto final hechas:", evaluaciones_proyecto_final_hechas)

    # Variables de anteproyectos y proyectos
    num_anteproyectos_aprobados = num_anteproyecto_aprobados_director(usuario)
    print("Número de anteproyectos aprobados:", num_anteproyectos_aprobados)

    num_anteproyectos_pendientes = num_anteproyecto_pendientes_director(usuario)
    print("Número de anteproyectos pendientes:", num_anteproyectos_pendientes)

    num_proyectos_aprobados = num_proyecto_final_terminados_director(usuario)
    print("Número de proyectos aprobados:", num_proyectos_aprobados)

    num_proyectos_pendientes = num_proyecto_final_pendientes_director(usuario)
    print("Número de proyectos pendientes:", num_proyectos_pendientes)

    num_proyectos = num_proyecto_final_director(usuario)
    print("Número total de proyectos:", num_proyectos)

    num_anteproyectos = num_anteproyecto_director(usuario)
    print("Número total de anteproyectos:", num_anteproyectos)

    # Porcentajes de anteproyectos y proyectos
    porcentaje_ante_aprobados = (
        (num_anteproyectos_aprobados / num_anteproyectos * 100)
        if num_anteproyectos > 0
        else 0
    )
    print("Porcentaje de anteproyectos aprobados:", porcentaje_ante_aprobados)

    porcentaje_ante_curso = (
        (num_anteproyectos_pendientes / num_anteproyectos * 100)
        if num_anteproyectos > 0
        else 0
    )
    print("Porcentaje de anteproyectos en curso:", porcentaje_ante_curso)

    porcentaje_proyect_aprobados = (
        (num_proyectos_aprobados / num_proyectos * 100) if num_proyectos > 0 else 0
    )
    print("Porcentaje de proyectos aprobados:", porcentaje_proyect_aprobados)

    porcentaje_proyect_curso = (
        (num_proyectos_pendientes / num_proyectos * 100) if num_proyectos > 0 else 0
    )
    print("Porcentaje de proyectos en curso:", porcentaje_proyect_curso)

    context["num_evaluaciones_anteproyecto"] = num_evaluaciones_anteproyecto
    context["num_evaluaciones_proyecto"] = num_evaluaciones_proyecto
    context["evaluaciones_anteproyecto_pendientes"] = (
        evaluaciones_anteproyecto_pendientes
    )
    context["evaluaciones_proyecto_final_pendientes"] = (
        evaluaciones_proyecto_final_pendientes
    )
    context["evaluaciones_anteproyecto_hechas"] = evaluaciones_anteproyecto_hechas
    context["evaluaciones_proyecto_final_hechas"] = evaluaciones_proyecto_final_hechas
    context["num_anteproyectos_aprobados"] = num_anteproyectos_aprobados
    context["num_anteproyectos_pendientes"] = num_anteproyectos_pendientes
    context["num_proyectos_aprobados"] = num_proyectos_aprobados
    context["num_proyectos_pendientes"] = num_proyectos_pendientes
    context["num_proyectos"] = num_proyectos
    context["num_anteproyectos"] = num_anteproyectos
    context["porcentaje_ante_aprobados"] = int(porcentaje_ante_aprobados)
    context["porcentaje_ante_curso"] = int(porcentaje_ante_curso)
    context["porcentaje_proyect_aprobados"] = int(porcentaje_proyect_aprobados)
    context["porcentaje_proyect_curso"] = int(porcentaje_proyect_curso)
    return render(request, "director/evaluacion_proyectos/carga_trabajo.html", context)


#############################################################################################################
# formatos de correspondencia


@login_required
@grupo_usuario("Directores")
def formatos_documentos(request):
    context = datosusuario(request)
    context["formatos"] = recuperar_formatos()

    return render(request, "director/formatos/formatos.html", context)
