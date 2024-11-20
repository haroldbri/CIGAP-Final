from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponsePermanentRedirect
from plataform_CIGAP.utils.envio_correos import (
    correo_anteproyecto_aprobado,
    correo_anteproyecto_rechazado,
    correo_proyecto_aprobado,
)
from plataform_CIGAP.views import logout_user
from django.contrib.auth.decorators import login_required
import base64
from datetime import datetime
from django.contrib import messages

# importacion de operadores para consultas de django
from django.db.models import Q
from datetime import date, timedelta

# importacion de la vista del login que permite cambiar la informacion de ususario
from login.views import editar_usuario

# importacion de las funcionalidaes
from plataform_CIGAP.utils.decoradores import grupo_usuario
from plataform_CIGAP.utils.recuperaciones import (
    num_anteproyecto_pendientes_director,
    num_evaluaciones_anteproyecto_director,
    num_evaluaciones_anteproyecto_pendientes_director,
    num_evaluaciones_proyecto_final_pendientes_director,
    num_proyecto_final_pendientes_director,
    recuperar_evaluacion_proyecto_final,
    recuperar_fechas_comite,
    recuperar_fechas_proyecto,
    recuperar_num_proyectos_terminados,
    recuperar_num_proyectos_pendientes,
    recuperar_num_solicitudes,
    recuperar_num_formatos_comite,
    recuperar_num_respuestas,
    recuperar_proyectos_pendientes,
    recuperar_proyectos_finalizados,
    recuperar_proyecto_finalizado,
    recuperar_proyecto_actual,
    recuperar_solicitudes_especiales_proyecto,
    recuperar_formatos,
    recuperar_documento,
    datosusuario,
)
from plataform_CIGAP.utils.funcionalidades_fechas import (
    fecha_actual,
    fecha_culminacion_anteproyecto,
)

# importacion de los modelos
from estudiante.models import ModelAnteproyecto, ModelProyectoFinal, ModelFechasProyecto
from director.models import ModelEvaluacionAnteproyecto, ModelEvaluacionProyectoFinal
from login.models import Usuarios
from correspondencia.models import (
    ModelFechasComite,
    ModelRetroalimentaciones,
    ModelSolicitudes,
    ModelInformacionEntregaFinal,
    ModelDocumentos,
)

# importacion de los formularios
from .forms import (
    FormRetroalimentacionAnteproyecto,
    FormRetroalimentacionProyecto,
    FormJurados,
    FormDocumentos,
)
from estudiante.forms import (
    FormAnteproyecto,
    FormProyectoFinal,
    FormActualizarProyectoFinal,
)

# importacion del manejo de clases de vistas
# tener en cuenta para el manejo de clases de vista con cada uno de los metodos y la asignacion de las urls de las mismas con asView
from django.views.generic.edit import CreateView

# from django.views.generic.list import ListView
# from django.urls import reverse_lazy

# Create your views here.
# def funcionando (request):
#     return HttpResponse('app_ correspondencia funcionando.')
########################################################################################################################
# Recuperar informaciones y funciones especificas para las vistas


def recuperar_retroalimentaciones_proyecto_final(proyecto_final):

    retroalimentaciones = ModelRetroalimentaciones.objects.filter(
        proyecto_final=proyecto_final
    )
    respuestas = {}
    if retroalimentaciones.exists():
        for i, retroalimentacion in enumerate(retroalimentaciones):
            doc_convert = recuperar_documento(retroalimentacion.doc_retroalimentacion)
            respuestas[f"retroalimentacion_{i}"] = {
                "respuesta": retroalimentacion,
                "doc_retroalimentacion": doc_convert,
            }
    return respuestas if respuestas else None


def recuperar_directores():
    directores = list(
        Usuarios.objects.filter(groups__name="Directores").values(
            "id", "nombre_completo", "email"
        )
    )
    return directores


def recuperar_usuario(id):
    usuario = Usuarios.objects.get(id=id)
    if not usuario:
        return None
    return usuario


def recuperar_usuario_nombre(nombre):
    usuario = Usuarios.objects.get(nombre_completo=nombre)
    if not usuario:
        return None
    return usuario


def verificar_evaluador(id):
    es_evaluador = ModelEvaluacionAnteproyecto.objects.filter(evaluador__id=id).exists()
    return es_evaluador


def recuperar_anteproyectos_pendientes():
    anteproyectos_pendientes = ModelAnteproyecto.objects.filter(
        estado=False, solicitud_enviada=True
    )
    return anteproyectos_pendientes


def recuperar_proyectos_finales():
    proyectos_finales = ModelProyectoFinal.objects.filter(
        solicitud_enviada=False, estado=False
    )
    if not proyectos_finales:
        return None
    return proyectos_finales


def recuperar_proyectos_finales_pendientes():
    proyectos_finales_pendientes = ModelProyectoFinal.objects.filter(
        solicitud_enviada=True, estado=False
    )
    return proyectos_finales_pendientes


def recuperar_proyectos_finales_finalizados():
    proyectos_finales_finalizados = ModelProyectoFinal.objects.filter(estado=True)
    return proyectos_finales_finalizados


def recuperar_asignaciones_jurados():
    pass


def recuperar_solicitudes_especiales_pendientes():
    solicitudes_pendientes = ModelSolicitudes.objects.filter(
        Q(estado=False)
        & (
            Q(tipo_solicitud="cambio_nombre")
            | Q(tipo_solicitud="ajuste_integrantes")
            | Q(tipo_solicitud="seccion_derechos")
            | Q(tipo_solicitud="otro")
        )
    )

    return solicitudes_pendientes


def recuperar_solicitud_especial_pendiente(id):
    solicitud_pendiente = (
        ModelSolicitudes.objects.get(id=id)
        if ModelSolicitudes.objects.filter(id=id).exists()
        else None
    )
    return solicitud_pendiente


# funcion para traer los anteproyectos


def recuperar_anteproyectos():
    anteproyectos = ModelAnteproyecto.objects.all()
    return anteproyectos


# funcion para recuperar los anteproyectos que aun no estan aprovados


def recuperar_anteproyectos_pendientes():
    anteproyectos = ModelAnteproyecto.objects.filter(
        Q(estado=False) & Q(solicitud_enviada=True)
    )
    return anteproyectos


# funcion para traer un anteproyecto en especifico


def recuperar_anteproyecto(nombre):
    anteproyecto = (
        ModelAnteproyecto.objects.get(nombre_anteproyecto=nombre)
        if ModelAnteproyecto.objects.filter(nombre_anteproyecto=nombre).exists()
        else None
    )
    return anteproyecto


def recuperar_anteproyecto_id(id):
    anteproyecto = ModelAnteproyecto.objects.get(id=id)
    if not anteproyecto:
        return None
    return anteproyecto


def recuperar_proyecto_final_id(id):
    proyecto = (
        ModelProyectoFinal.objects.get(id=id)
        if ModelProyectoFinal.objects.filter(id=id).exists()
        else None
    )

    return proyecto


# funcion para recuperar un proyecto Final


def recuperar_proyecto_final(anteproyecto):
    proyecto_final = (
        ModelProyectoFinal.objects.get(anteproyecto=anteproyecto)
        if ModelProyectoFinal.objects.filter(anteproyecto=anteproyecto).exists()
        else None
    )
    return proyecto_final


# funcion para recuperar proyectos finales


def recuperar_proyecto_aceptado(anteproyecto):
    proyecto_final = (
        ModelProyectoFinal.objects.get(anteproyecto=anteproyecto, estado=True)
        if ModelProyectoFinal.objects.filter(anteproyecto=anteproyecto).exists()
        else None
    )
    return proyecto_final


def recuperar_proyectos_finales():
    proyectos_finales = ModelProyectoFinal.objects.filter(solicitud_enviada=True)
    return proyectos_finales


# funcion para recuperar una solicitud espeial


def recuperar_solicitud_especial(id):
    solicitud_especial = (
        ModelSolicitudes.objects.get(id=id)
        if ModelSolicitudes.objects.filter(id=id).exists()
        else None
    )
    return solicitud_especial


# funcion para recuperar solicitudes espeiales


def recuperar_solicitudes_especiales():
    solicitudes_especiales = ModelSolicitudes.objects.all()
    return solicitudes_especiales


# funcion para recuperar las imagenes de los usuarios


def recuperar_datos_integrantes(nombre):
    usuario = (
        Usuarios.objects.get(nombre_completo=nombre)
        if Usuarios.objects.filter(nombre_completo=nombre).exists()
        else False
    )
    if usuario:
        imagen_binaria = usuario.imagen
        imagen = (
            base64.b64encode(imagen_binaria).decode("utf8") if imagen_binaria else False
        )
        grupos = usuario.groups.values_list("name", flat=True)
        grupo = (
            "Estudiante"
            if "Estudiantes" in grupos
            else "Director" if "Directores" in grupos else "Desconocido"
        )
        return {"nombre": nombre, "imagen": imagen, "grupo": grupo}
    else:
        return {"nombre": nombre, "imagen": False, "grupo": "Desconocido"}


def recuperar_evaluaciones_anteproyecto(anteproyecto):
    evaluaciones_anteproyecto = ModelEvaluacionAnteproyecto.objects.filter(
        anteproyecto=anteproyecto
    )
    if evaluaciones_anteproyecto:
        return evaluaciones_anteproyecto
    else:
        return None


# funcion para traer la lista de solicitudes


def recuperar_solicitudes():
    solicitudes = ModelRetroalimentaciones.objects.all()
    return solicitudes


def recuperar_solicitudes_anteproyecto():
    solicitudes = ModelRetroalimentaciones.objects.filter(anteproyecto__isnull=False)
    return solicitudes


def recuperar_solicitud(anteproyecto):
    solicitud = (
        ModelRetroalimentaciones.objects.get(anteproyecto=anteproyecto)
        if ModelRetroalimentaciones.objects.filter(anteproyecto=anteproyecto).exists()
        else None
    )
    return solicitud


# def recuperar_solicitudes_():
#     solicitudes = ModelRetroalimentaciones.objects.filter(anteproyecto=True)
#     return solicitudes


# funcion para recuperar datos de los directores


def recuperar_directores():
    directores = Usuarios.objects.filter(groups__name="Directores").values(
        "id", "nombre_completo", "email"
    )
    if directores:
        return directores
    else:
        directores = None
        return directores


@login_required
def asignar_fechas_encuentros(request):
    if request.method == "POST":
        ano_actual = datetime.now().year
        periodo_academico = (
            (request.POST.get("periodo_academico"))
            if request.POST.get("periodo_academico")
            else None
        )
        primer_encuentro = (
            request.POST.get("fecha_primer_encuentro")
            if request.POST.get("fecha_primer_encuentro")
            else None
        )
        segundo_encuentro = (
            request.POST.get("fecha_segundo_encuentro")
            if request.POST.get("fecha_segundo_encuentro")
            else None
        )
        tercer_encuentro = (
            request.POST.get("fecha_tercer_encuentro")
            if request.POST.get("fecha_tercer_encuentro")
            else None
        )
        cuarto_encuentro = (
            request.POST.get("fecha_cuarto_encuentro")
            if request.POST.get("fecha_cuarto_encuentro")
            else None
        )
        extraordinaria = (
            request.POST.get("fecha_extraordinaria")
            if request.POST.get("fecha_extraordinaria")
            else None
        )

        fecha_hoy = datetime.now().date()
        fechas_validas = True

        # Determinar el periodo académico actual basado en la fecha actual
        if fecha_hoy.month <= 6:
            periodo_actual = "1"
        else:
            periodo_actual = "2"

        # Verificar si ya existen fechas para el año y periodo académico actual
        if ModelFechasComite.objects.filter(
            ano_actual=ano_actual, periodo_academico=periodo_actual
        ).exists():
            messages.error(
                request,
                "Ya se han registrado fechas para este periodo académico en el año actual, edite las existentes.",
            )
            return redirect("correspondencia:principal_correspondencia")

        # Validar si el periodo académico ingresado coincide con el actual
        if periodo_academico != periodo_actual:
            messages.error(
                request,
                f"No puedes registrar fechas para el periodo académico {periodo_academico}, actualmente estamos en el periodo académico {periodo_actual}.",
            )
            return redirect("correspondencia:principal_correspondencia")

        # Comparar las fechas de los encuentros con la fecha actual
        if primer_encuentro and primer_encuentro < fecha_hoy.isoformat():
            messages.error(
                request,
                "La fecha del primer encuentro debe ser hoy o una fecha futura.",
            )
            fechas_validas = False

        if segundo_encuentro and segundo_encuentro < fecha_hoy.isoformat():
            messages.error(
                request,
                "La fecha del segundo encuentro debe ser hoy o una fecha futura.",
            )
            fechas_validas = False

        if tercer_encuentro and tercer_encuentro < fecha_hoy.isoformat():
            messages.error(
                request,
                "La fecha del tercer encuentro debe ser hoy o una fecha futura.",
            )
            fechas_validas = False

        if cuarto_encuentro and cuarto_encuentro < fecha_hoy.isoformat():
            messages.error(
                request,
                "La fecha del cuarto encuentro debe ser hoy o una fecha futura.",
            )
            fechas_validas = False

        if extraordinaria and extraordinaria < fecha_hoy.isoformat():
            messages.error(
                request,
                "La fecha de la reunión extraordinaria debe ser hoy o una fecha futura.",
            )
            fechas_validas = False

        if fechas_validas:
            new_fechas_encuentro = ModelFechasComite(
                ano_actual=ano_actual,
                periodo_academico=periodo_academico,
                primer_encuentro=primer_encuentro,
                segundo_encuentro=segundo_encuentro,
                tercer_encuentro=tercer_encuentro,
                cuarto_encuentro=cuarto_encuentro,
                extraordinaria=extraordinaria,
            )
            new_fechas_encuentro.save()
            messages.success(
                request, "Las fechas de los encuentros han sido asignadas exitosamente."
            )
            return redirect("correspondencia:principal_correspondencia")
        else:
            # En caso de fechas inválidas, redirigir sin guardar
            return redirect("correspondencia:principal_correspondencia")
    else:
        messages.error(request, "El método utilizado no es válido.")
        return redirect("correspondencia:principal_correspondencia")


@login_required
@grupo_usuario("Correspondencia")
def principal_correspondencia(request):
    context = datosusuario(request)
    fechas_comite = recuperar_fechas_comite()
    ano_actual = datetime.now().year
    context["ano_actual"] = ano_actual
    if fechas_comite:
        context["fechas_comite"] = fechas_comite
    num_solicitudes = recuperar_num_solicitudes()
    num_formatos = recuperar_num_formatos_comite()
    num_proyectos = recuperar_num_proyectos_pendientes()
    num_respuestas = recuperar_num_respuestas()

    fecha_actual = datetime.now().date()
    context["fecha_actual"] = fecha_actual
    context["num_solicitudes"] = num_solicitudes
    context["num_formatos"] = num_formatos
    context["num_proyectos"] = num_proyectos
    context["num_respuestas"] = num_respuestas
    return render(request, "correspondencia/base_correspondencia.html", context)


@login_required
@grupo_usuario("Correspondencia")
def editar_fechas_comite(request, id):
    fechas = (
        ModelFechasComite.objects.get(id=id)
        if ModelFechasComite.objects.filter(id=id).exists()
        else None
    )
    fecha_hoy = datetime.now().date()
    fechas_validas = True

    if fechas:
        primer_encuentro = request.POST.get("fecha_primer_encuentro")
        segundo_encuentro = request.POST.get("fecha_segundo_encuentro")
        tercer_encuentro = request.POST.get("fecha_tercer_encuentro")
        cuarto_encuentro = request.POST.get("fecha_cuarto_encuentro")
        extraordinaria = request.POST.get("fecha_extraordinaria")

        if primer_encuentro < fecha_hoy.isoformat():
            messages.error(
                request,
                "La fecha del primer encuentro debe ser hoy o una fecha futura.",
            )
            fechas_validas = False

        if segundo_encuentro and segundo_encuentro < fecha_hoy.isoformat():
            messages.error(
                request,
                "La fecha del segundo encuentro debe ser hoy o una fecha futura.",
            )
            fechas_validas = False

        if tercer_encuentro and tercer_encuentro < fecha_hoy.isoformat():
            messages.error(
                request,
                "La fecha del tercer encuentro debe ser hoy o una fecha futura.",
            )
            fechas_validas = False

        if cuarto_encuentro and cuarto_encuentro < fecha_hoy.isoformat():
            messages.error(
                request,
                "La fecha del cuarto encuentro debe ser hoy o una fecha futura.",
            )
            fechas_validas = False

        if extraordinaria and extraordinaria < fecha_hoy.isoformat():
            messages.error(
                request,
                "La fecha de la reunión extraordinaria debe ser hoy o una fecha futura.",
            )
            fechas_validas = False
        if fechas_validas:
            fechas.primer_encuentro = primer_encuentro
            fechas.segundo_encuentro = segundo_encuentro
            fechas.tercer_encuentro = tercer_encuentro
            fechas.cuarto_encuentro = cuarto_encuentro
            fechas.extraordinaria = extraordinaria
            fechas.save()
            messages.success(
                request,
                "Las fechas de los encuentros han sido actualizadas exitosamente.",
            )
            return redirect("correspondencia:principal_correspondencia")
        return redirect("correspondencia:principal_correspondencia")


########################################################################################################################
# vista de solicitudes


@login_required
@grupo_usuario("Correspondencia")
def solicitudes(request):
    context = datosusuario(request)
    proyectos_finales_pendientes = recuperar_proyectos_finales_pendientes()
    solicitudes_especiales_pendientes = recuperar_solicitudes_especiales_pendientes()
    anteproyectos_pendientes = recuperar_anteproyectos_pendientes()

    context["proyectos_finales"] = proyectos_finales_pendientes.count()
    context["solicitudes_especiales"] = solicitudes_especiales_pendientes.count()
    context["anteproyectos"] = anteproyectos_pendientes.count()

    total_pendientes = (
        proyectos_finales_pendientes.count()
        + solicitudes_especiales_pendientes.count()
        + anteproyectos_pendientes.count()
    )
    context["solicitudes_pendientes"] = total_pendientes

    return render(request, "correspondencia/views_solicitud/solicitudes.html", context)


@login_required
@grupo_usuario("Correspondencia")
def solicitudes_anteproyectos(request):
    context = datosusuario(request)
    if request.method == "POST":
        pass
    else:
        anteproyectos = (
            ModelAnteproyecto.objects.filter(estado=False)
            if ModelAnteproyecto.objects.filter(estado=False).exists()
            else None
        )
        context["anteproyectos"] = anteproyectos

        return render(
            request, "correspondencia/views_solicitud/list_anteproyectos.html", context
        )


@login_required
@grupo_usuario("Correspondencia")
def solicitudes_proyectos_finales(request):
    context = datosusuario(request)
    proyectos_finales = recuperar_proyectos_finales_pendientes()

    context["proyectos_finales"] = proyectos_finales
    return render(
        request, "correspondencia/views_solicitud/list_proyectos_finales.html", context
    )


# funcion de la vista de lista de solicitudes especiales


@login_required
@grupo_usuario("Correspondencia")
def solicitudes_especiales(request):
    context = datosusuario(request)

    if request.method == "POST":
        pass
    else:
        solicitudes_especiales = recuperar_solicitudes_especiales_pendientes()
        context["solicitudes_especiales"] = solicitudes_especiales
        return render(
            request,
            "correspondencia/views_solicitud/list_solicitud_especiales.html",
            context,
        )


@login_required
@grupo_usuario("Correspondencia")
def view_solicitud_especial(request, id):
    context = datosusuario(request)
    directores = recuperar_directores()
    context["directores"] = directores
    solicitud_especial = recuperar_solicitud_especial(id)

    context["solicitud_especial"] = solicitud_especial

    documento_binario = solicitud_especial.documento_soporte
    documento_soporte = recuperar_documento(documento_binario)
    context["documento_soporte"] = documento_soporte

    if solicitud_especial.anteproyecto:
        form_anteproyecto = FormAnteproyecto(instance=solicitud_especial.anteproyecto)
        form_retroalimentacion_ante = FormRetroalimentacionAnteproyecto(
            instance=solicitud_especial.anteproyecto
        )
        context["form_anteproyecto"] = form_anteproyecto
        context["form_retroalimentacion"] = form_retroalimentacion_ante
    elif solicitud_especial.proyecto_final:
        form_proyecto_final = FormActualizarProyectoFinal(
            instance=solicitud_especial.proyecto_final
        )
        form_retroalimentacion_pro = FormRetroalimentacionProyecto(
            instance=solicitud_especial.proyecto_final
        )
        context["form_proyecto"] = form_proyecto_final
        context["form_retroalimentacion"] = form_retroalimentacion_pro
    else:
        return HttpResponse("Error: No se encontró anteproyecto ni proyecto final.")

    return render(
        request, "correspondencia/views_solicitud/solicitud_especial.html", context
    )


@login_required
@grupo_usuario("Correspondencia")
def actualizar_datos_solicitud_anteproyecto(request, id):
    solicitud_especial = recuperar_solicitud_especial(id)
    anteproyecto = solicitud_especial.anteproyecto

    if request.method == "POST":
        form_anteproyecto = FormAnteproyecto(
            request.POST, request.FILES, instance=anteproyecto
        )

        if form_anteproyecto.is_valid():
            form_anteproyecto.save()
            messages.success(request, "Los datos se han actualizado correctamente.")
            return redirect("correspondencia:view_solicitud_especial", id=id)
        else:
            messages.error(
                request, "Algo pasó: por favor revisa los errores en el formulario."
            )
            return render(
                request,
                "nombre_template.html",
                {"form_anteproyecto": form_anteproyecto},
            )

    messages.warning(request, "Método no permitido. Intenta de nuevo.")
    return redirect("correspondencia:view_solicitud_especial", id=id)


@login_required
@grupo_usuario("Correspondencia")
def actualizar_datos_solicitud_proyecto(request, id):
    context = datosusuario(request)
    solicitud_especial = recuperar_solicitud_especial(id)
    proyecto = solicitud_especial.proyecto_final
    anteproyecto = proyecto.anteproyecto
    if request.method == "POST":
        form_proyecto = FormActualizarProyectoFinal(
            request.POST, request.FILES, instance=proyecto
        )
        director = request.POST.get("director")
        codirector = request.POST.get("codirector")

        if form_proyecto.is_valid():
            if not request.FILES.get("doc_proyecto_final_form"):
                form_proyecto.cleaned_data.pop("doc_proyecto_final_form", None)
            if not request.FILES.get("carta_presentacion_final_form"):
                form_proyecto.cleaned_data.pop("carta_presentacion_final_form", None)

            anteproyecto.director = director
            anteproyecto.codirector = codirector
            anteproyecto.save(update_fields=["director", "codirector"])
            form_proyecto.save()
            return redirect("correspondencia:view_solicitud_especial", id=id)
        else:
            return HttpResponse(f"Error: {form_proyecto.errors}")
    else:

        form_proyecto = FormActualizarProyectoFinal(instance=proyecto)
        context["form_proyecto"] = form_proyecto
    return render(request, "ruta_de_template.html", context)


@login_required
@grupo_usuario("Correspondencia")
def enviar_retroalimentacion_solicitud(request, id):
    solicitud_especial = recuperar_solicitud_especial(id)

    if solicitud_especial.anteproyecto:
        form_retro = FormRetroalimentacionAnteproyecto(request.POST, request.FILES)
        if form_retro.is_valid():

            retroalimentacion = form_retro.save(commit=False)
            retroalimentacion.user = request.user
            retroalimentacion.anteproyecto = solicitud_especial.anteproyecto
            retroalimentacion.fecha_retroalimentacion = fecha_actual()
            retroalimentacion.revs_dadas = (retroalimentacion.revs_dadas or 0) + 1

            if form_retro.cleaned_data["estado"] == "Rechazado":

                solicitud_especial.delete()
                messages.success(
                    request, "La solicitud ha sido rechazada y eliminada correctamente."
                )

            else:
                solicitud_especial.estado = True
                solicitud_especial.save()
                retroalimentacion.estado = "Aprobado"
                retroalimentacion.save()
                messages.success(
                    request,
                    "La retroalimentación del anteproyecto se ha enviado correctamente.",
                )

            return redirect("correspondencia:solicitudes")

        else:
            messages.error(
                request, "Algo pasó: por favor revisa los errores en el formulario."
            )
            return redirect("correspondencia:solicitudes")

    elif solicitud_especial.proyecto_final:
        form_retro = FormRetroalimentacionAnteproyecto(request.POST, request.FILES)
        if form_retro.is_valid():
            retroalimentacion = form_retro.save(commit=False)
            retroalimentacion.proyecto_final = solicitud_especial.proyecto_final
            retroalimentacion.fecha_retroalimentacion = fecha_actual()
            retroalimentacion.revs_dadas = (retroalimentacion.revs_dadas or 0) + 1

            if form_retro.cleaned_data["estado"] == "Rechazado":
                solicitud_especial.delete()
                messages.success(
                    request, "La solicitud ha sido rechazada y eliminada correctamente."
                )
            else:
                solicitud_especial.estado = True
                solicitud_especial.save()
                retroalimentacion.estado = "Aprobado"
                retroalimentacion.save()
                messages.success(
                    request,
                    "La retroalimentación del proyecto final se ha enviado correctamente.",
                )

            return redirect("correspondencia:solicitudes")

        else:
            messages.error(
                request, "Algo pasó: por favor revisa los errores en el formulario."
            )
            return render(request, "nombre_template.html", {"form_retro": form_retro})

    messages.warning(
        request, "No se puede enviar la retroalimentación: solicitud no válida."
    )
    return redirect("correspondencia:solicitudes")


########################################################################################################################
# vista para conocer la informacion del anteproyecto


@login_required
@grupo_usuario("Correspondencia")
def ver_anteproyecto(request, nombre_anteproyecto):
    context = datosusuario(request)
    directores = recuperar_directores()

    if directores:
        context["directores"] = directores
    anteproyecto = recuperar_anteproyecto(nombre_anteproyecto)
    evaluaciones = recuperar_evaluaciones_anteproyecto(anteproyecto)
    if evaluaciones:
        context["evaluaciones"] = evaluaciones
    doc_anteproyecto = recuperar_documento(anteproyecto.anteproyecto)
    doc_carta = recuperar_documento(anteproyecto.carta_presentacion)
    context["inf_anteproyecto"] = {
        "anteproyecto": anteproyecto,
        "form_retroalimentacion": FormRetroalimentacionAnteproyecto,
        "doc_anteproyecto": doc_anteproyecto,
        "doc_carta": doc_carta,
    }

    if anteproyecto:
        if anteproyecto.documento_radicado:
            context["documento_radicado"] = recuperar_documento(
                anteproyecto.documento_radicado
            )
        integrantes = (
            anteproyecto.nombre_integrante1,
            anteproyecto.nombre_integrante2,
            anteproyecto.director,
            anteproyecto.codirector,
        )
        datos_integrantes = {}
        for i, integrante in enumerate(integrantes, start=1):
            if integrante:
                datos_integrantes[f"integrante_{i}"] = recuperar_datos_integrantes(
                    integrante
                )
        context["datos_integrantes"] = datos_integrantes
        return render(
            request, "correspondencia/views_solicitud/anteproyecto.html", context
        )
    else:
        return HttpResponse("Gestiona los proyectos existentes, algo pasó con este.")


@login_required
@grupo_usuario("Correspondencia")
def cargar_radicado(request, id):
    anteproyecto = recuperar_anteproyecto_id(id)

    if not anteproyecto:
        messages.error(request, "El anteproyecto no existe.")
        return redirect("correspondencia:solicitudes")
    if anteproyecto.documento_radicado:
        messages.warning(request, "Este anteproyecto ya tiene un radicado cargado.")
        return redirect(
            "correspondencia:ver_anteproyecto",
            nombre_anteproyecto=anteproyecto.nombre_anteproyecto,
        )

    if "documento_radicado" in request.FILES:
        try:
            anteproyecto.documento_radicado = request.FILES.get(
                "documento_radicado"
            ).read()
            anteproyecto.save()
            messages.success(request, "El radicado ha sido cargado exitosamente.")
        except Exception as e:
            messages.error(request, f"Hubo un error al cargar el radicado: {str(e)}")
            return redirect(
                "correspondencia:ver_anteproyecto",
                nombre_anteproyecto=anteproyecto.nombre_anteproyecto,
            )

        return redirect(
            "correspondencia:ver_anteproyecto",
            nombre_anteproyecto=anteproyecto.nombre_anteproyecto,
        )
    else:
        messages.error(request, "No se ha enviado ningún archivo.")
        return redirect(
            "correspondencia:ver_anteproyecto",
            nombre_anteproyecto=anteproyecto.nombre_anteproyecto,
        )


@login_required
@grupo_usuario("Correspondencia")
def editar_radicado(request, id):
    anteproyecto = recuperar_anteproyecto_id(id)

    if "documento_radicado" in request.FILES:
        try:
            anteproyecto.documento_radicado = request.FILES.get(
                "documento_radicado"
            ).read()
            anteproyecto.save()
            messages.success(request, "El radicado ha sido actualizado exitosamente.")
        except Exception as e:
            messages.error(request, f"Hubo un error al cargar el radicado: {str(e)}")
            return redirect(
                "correspondencia:ver_anteproyecto",
                nombre_anteproyecto=anteproyecto.nombre_anteproyecto,
            )

        return redirect(
            "correspondencia:ver_anteproyecto",
            nombre_anteproyecto=anteproyecto.nombre_anteproyecto,
        )
    else:
        messages.error(request, "No se ha enviado ningún archivo.")
        return redirect(
            "correspondencia:ver_anteproyecto",
            nombre_anteproyecto=anteproyecto.nombre_anteproyecto,
        )


@login_required
@grupo_usuario("Correspondencia")
def enviar_retroalimentacion(request, nombre_anteproyecto):

    anteproyecto = recuperar_anteproyecto(nombre_anteproyecto)
    if anteproyecto is None:
        messages.error(
            request, "Anteproyecto no encontrado. Redirigiendo a solicitudes."
        )
        return redirect("correspondencia:solicitudes")

    if request.method == "POST":

        text_retroalimentaicion = request.POST.get("retroalimentacion")
        estado = request.POST.get("estado")

        if not estado:
            correo_anteproyecto_rechazado(anteproyecto.user, retroalimentacion)
            anteproyecto.delete()
            messages.warning(
                request,
                "El anteproyecto ha sido eliminado debido a un estado no aprobado.",
            )
            return redirect("correspondencia:solicitudes")

        doc_retro = request.FILES.get("doc_retroalimentacion")
        if doc_retro:
            doc_binario = doc_retro.read()

            anteproyecto.estado = True
            anteproyecto.documento_concepto = doc_binario
            anteproyecto.save(update_fields=["estado", "documento_concepto"])

            retroalimentacion = ModelRetroalimentaciones(
                user=request.user,
                anteproyecto=anteproyecto,
                retroalimentacion=text_retroalimentaicion,
                fecha_retroalimentacion=fecha_actual(),
                doc_retroalimentacion=doc_binario,
                estado=estado,
            )
            correo_anteproyecto_aprobado(anteproyecto.user, retroalimentacion)
            retroalimentacion.save()

            nuevo_proyecto_final = ModelProyectoFinal(
                user=anteproyecto.user,
                anteproyecto=anteproyecto,
            )
            nuevo_proyecto_final.save()

            fecha_actual_datetime = datetime.strptime(
                fecha_actual(), "%Y-%m-%d %H:%M:%S"
            ).date()
            fechas_proyecto_final = ModelFechasProyecto(
                proyecto_final=nuevo_proyecto_final,
                fecha_inicio=fecha_actual_datetime,
                fecha_etapa_uno=fecha_actual_datetime + timedelta(days=30),
                fecha_etapa_dos=fecha_actual_datetime + timedelta(days=60),
                fecha_etapa_tres=fecha_actual_datetime + timedelta(days=90),
                fecha_etapa_cuatro=fecha_actual_datetime + timedelta(days=120),
                fecha_etapa_cinco=fecha_actual_datetime + timedelta(days=150),
                fecha_etapa_seis=fecha_actual_datetime + timedelta(days=165),
            )
            fechas_proyecto_final.save()

            messages.success(
                request, "La retroalimentación se ha enviado exitosamente."
            )
            return redirect("correspondencia:solicitudes")
        else:
            messages.error(request, "Error: Documento no encontrado")
            return redirect("correspondencia:solicitudes")

    else:
        messages.error(request, "Por favor, corrige los errores en el formulario.")
        return redirect("correspondencia:solicitudes")


@login_required
@grupo_usuario("Correspondencia")
def enviar_retroalimentacion_concepto(request, id_proyecto):
    if request.method == "POST":
        proyecto = recuperar_proyecto_final_id(id_proyecto)

        if proyecto:
            fechas_proyecto = (
                ModelFechasProyecto.objects.get(proyecto_final=proyecto)
                if ModelFechasProyecto.objects.filter(proyecto_final=proyecto).exists()
                else None
            )
            if fechas_proyecto:
                fechas_proyecto.fecha_finalizacion = fecha_actual()
                fechas_proyecto.save()
            text_retroalimentaicion = request.POST.get("retroalimentacion")
            estado = request.POST.get("estado")
            doc_concepto = request.FILES.get("doc_retroalimentacion")
            if estado == "True":

                new_retro = ModelRetroalimentaciones(
                    user=request.user,
                    proyecto_final=proyecto,
                    retroalimentacion=text_retroalimentaicion,
                    fecha_retroalimentacion=fecha_actual(),
                    doc_retroalimentacion=doc_concepto.read(),
                    estado=True,
                )
                new_retro.save()
                proyecto.estado = True
                proyecto.save()

                new_informacion_entrega_final = ModelInformacionEntregaFinal(
                    anteproyecto=proyecto.anteproyecto,
                    proyecto_final=proyecto,
                    fechas_proyecto=fechas_proyecto,
                    fecha_finalizacion=fecha_actual(),
                )
                new_informacion_entrega_final.save()
                messages.success(
                    request,
                    "¡El proyecto final ha sido aprobado exitosamente! Diríjase al apartado de 'Proyectos - Proyectos Finalizados' para conocer más información.",
                )
                correo_proyecto_aprobado(proyecto, text_retroalimentaicion)
                return redirect("correspondencia:proyectos_finalizados")
            else:

                if estado == "False":
                    evaluaciones_del_proyecto = (
                        ModelEvaluacionProyectoFinal.objects.filter(
                            proyecto_final=proyecto
                        )
                    )
                    evaluaciones_del_proyecto.delete()

                    fechas_proyecto = (
                        ModelFechasProyecto.objects.get(proyecto_final=proyecto)
                        if ModelFechasProyecto.objects.filter(
                            proyecto_final=proyecto
                        ).exists()
                        else None
                    )
                    if fechas_proyecto:
                        fechas_proyecto.fecha_sustentacion = None
                        fechas_proyecto.save()
                    proyecto.proyecto_final = None
                    proyecto.estado = False
                    proyecto.solicitud_enviada = False
                    proyecto.fecha_envio = None
                    proyecto.proyecto_final = None
                    new_retro = ModelRetroalimentaciones(
                        user=request.user,
                        proyecto_final=proyecto,
                        retroalimentacion=text_retroalimentaicion,
                        fecha_retroalimentacion=fecha_actual(),
                        doc_retroalimentacion=doc_concepto.read(),
                        estado=estado,
                    )
                    proyecto.save()
                    new_retro.save()
                    messages.success(
                        request,
                        f"Se ha enviado la retroalimentación para el proyecto {proyecto.anteproyecto.nombre_anteproyecto} que no fue aprobado.",
                    )
                    return redirect("correspondencia:solicitudes")
    else:
        messages.error(request, "Ocurrió algo.")
        return redirect("correspondencia:solicitudes")


def recuperar_evaluaciones_jurados(proyecto):
    evaluaciones = ModelEvaluacionProyectoFinal.objects.filter(proyecto_final=proyecto)
    return evaluaciones


@login_required
@grupo_usuario("Correspondencia")
def ver_proyecto_final(request, nombre):
    print(fecha_actual())
    context = datosusuario(request)
    fecha_actual_str = fecha_actual()
    fecha_actual_dt = datetime.strptime(fecha_actual_str, "%Y-%m-%d %H:%M:%S")
    context["fecha_actual"] = fecha_actual_dt.strftime("%Y-%m-%dT%H:%M")
    ###########################################################################
    dias_habiles = 10
    context["fecha_habil"] = fecha_actual() + str(timedelta(days=dias_habiles))
    ###########################################################################
    anteproyecto = recuperar_anteproyecto(nombre)
    proyecto_final = recuperar_proyecto_final(anteproyecto)
    evaluaciones = recuperar_evaluaciones_jurados(proyecto_final)
    if evaluaciones:
        context["evaluaciones"] = evaluaciones
    if anteproyecto is None or proyecto_final is None:
        return redirect("correspondencia:solicitudes")
    else:
        integrantes = (
            anteproyecto.nombre_integrante1,
            anteproyecto.nombre_integrante2,
            anteproyecto.director,
            anteproyecto.codirector,
        )
        datos_integrantes = {}
        for i, integrante in enumerate(integrantes, start=1):
            if integrante:
                datos_integrantes[f"integrante_{i}"] = recuperar_datos_integrantes(
                    integrante
                )
        context["datos_integrantes"] = datos_integrantes
    if request.method == "POST":
        form_retro = FormRetroalimentacionAnteproyecto(request.POST, request.FILES)

        if form_retro.is_valid():
            retroalimentacion = form_retro.save(commit=False)
            retroalimentacion.proyecto_final = proyecto_final
            retroalimentacion.fecha_retroalimentacion = fecha_actual()
            retroalimentacion.revs_dadas = (retroalimentacion.revs_dadas or 0) + 1
            if retroalimentacion.estado not in [
                "Aprobado",
                "Aprobado_con_correcciones",
            ]:
                proyecto_final.delete()
                return render("correspondenicia:solicitudes")

            else:
                proyecto_final.estado = True
                proyecto_final.save(
                    update_fields=[
                        "estado",
                    ]
                )
                retroalimentacion.save()

            url = reverse("correspondencia:asignar_jurados", kwargs={"nombre": nombre})
            return redirect(url)

        else:
            print(form_retro.errors)
    else:

        anteproyecto = recuperar_anteproyecto(nombre)
        if anteproyecto:

            proyecto_final = recuperar_proyecto_final(anteproyecto)
            if proyecto_final:

                doc_proyecto_final = recuperar_documento(proyecto_final.proyecto_final)
                doc_carta_final = recuperar_documento(
                    proyecto_final.carta_presentacion_final
                )
                doc_radicado = recuperar_documento(proyecto_final.documento_radicado)
                if doc_radicado:
                    context["documento_radicado"] = doc_radicado

                context["inf_proyecto"] = proyecto_final
                context["doc_proyecto_final"] = doc_proyecto_final
                context["doc_carta_final"] = doc_carta_final

        directores = recuperar_directores()

        context["directores"] = directores
        form_retroalimentaciones_proyecto = FormRetroalimentacionProyecto
        form_jurados = FormJurados
        context["form_jurados"] = form_jurados
        context["form_retroalimentacion"] = form_retroalimentaciones_proyecto
        return render(request, "correspondencia/views_solicitud/proyecto.html", context)


@login_required
@grupo_usuario("Correspondencia")
def cargar_radicado_proyecto_final(request, id_proyecto):
    proyecto_final = recuperar_proyecto_final_id(id_proyecto)
    nombre = proyecto_final.anteproyecto.nombre_anteproyecto
    if not proyecto_final:
        messages.error(request, "El proyecto final no existe.")
        return redirect("correspondencia:solicitudes")
    if proyecto_final.documento_radicado:
        messages.warning(request, "Este proyecto final ya tiene un radicado cargado.")

        return redirect("correspondencia:ver_proyecto_final", nombre=nombre)

    if "documento_radicado" in request.FILES:
        try:
            proyecto_final.documento_radicado = request.FILES.get(
                "documento_radicado"
            ).read()
            proyecto_final.save()
            messages.success(request, "El radicado ha sido cargado exitosamente.")
        except Exception as e:
            messages.error(request, f"Hubo un error al cargar el radicado: {str(e)}")
            return redirect("correspondencia:ver_proyecto_final", nombre=nombre)

        return redirect("correspondencia:ver_proyecto_final", nombre=nombre)
    else:
        messages.error(request, "No se ha enviado ningún archivo.")
        return redirect("correspondencia:ver_proyecto_final", nombre=nombre)


@login_required
@grupo_usuario("Correspondencia")
def editar_radicado_proyecto_final(request, id_proyecto):
    proyecto = recuperar_proyecto_final_id(id_proyecto)

    if "documento_radicado" in request.FILES:
        try:
            proyecto.documento_radicado = request.FILES.get("documento_radicado").read()
            proyecto.save()
            messages.success(request, "El radicado ha sido actualizado exitosamente.")
        except Exception as e:
            messages.error(request, f"Hubo un error al cargar el radicado: {str(e)}")
            return redirect(
                "correspondencia:ver_proyecto_final",
                nombre=proyecto.anteproyecto.nombre_anteproyecto,
            )

        return redirect(
            "correspondencia:ver_proyecto_final",
            nombre=proyecto.anteproyecto.nombre_anteproyecto,
        )
    else:
        messages.error(request, "No se ha enviado ningún archivo.")
        return redirect(
            "correspondencia:ver_proyecto_final",
            nombre=proyecto.anteproyecto.nombre_anteproyecto,
        )


@login_required
@grupo_usuario("Correspondencia")
def fue_asignado_jurado_jurado(nombre_completo):
    fue_asignado = ModelEvaluacionProyectoFinal.objects.filter(
        jurado__nombre_completo=nombre_completo
    )
    if fue_asignado:
        return True
    else:
        return False


@login_required
@grupo_usuario("Correspondencia")
def asignar_jurados(request, id):
    context = datosusuario(request)
    proyecto = recuperar_proyecto_final_id(id)
    if proyecto:
        if request.method == "POST":
            directores_seleccionados = request.POST.getlist("directores")
            for director in directores_seleccionados:

                fue_asignado = fue_asignado_jurado_jurado(director)
                if fue_asignado:
                    messages.error(request, "El director ya fue asignado como jurado")
                else:
                    usuario = recuperar_usuario(director)
                    if usuario:
                        new_evaluacion_proyecto_final = ModelEvaluacionProyectoFinal(
                            jurado=usuario,
                            proyecto_final=proyecto,
                            fecha_asignacion=fecha_actual(),
                        )
                        new_evaluacion_proyecto_final.save()
                        messages.success(
                            request,
                            f"El director {director} fue asignado como jurado al proyecto final {proyecto.anteproyecto.nombre_anteproyecto}.",
                        )
            messages.error(request, "El director ya fue asignado como jurado")
            return redirect(
                "correspondencia:ver_proyecto_final",
                nombre=proyecto.anteproyecto.nombre_anteproyecto,
            )
        messages.error(request, "El director ya fue asignado como jurado")
        return redirect(
            "correspondencia:ver_proyecto_final",
            nombre=proyecto.anteproyecto.nombre_anteproyecto,
        )
    messages.error(request, "El director ya fue asignado como jurado")
    return redirect(
        "correspondencia:ver_proyecto_final",
        nombre=proyecto.anteproyecto.nombre_anteproyecto,
    )


@login_required
@grupo_usuario("Correspondencia")
def eliminar_jurado(request, id, nombre_proyecto):
    evaluacion = (
        ModelEvaluacionProyectoFinal.objects.get(id=id)
        if ModelEvaluacionProyectoFinal.objects.filter(id=id).exists()
        else None
    )

    if evaluacion:
        evaluacion.delete()
        messages.success(
            request,
            f"El jurado del proyecto '{nombre_proyecto}' ha sido eliminada exitosamente.",
        )
    else:
        messages.error(
            request,
            f"No se pudo encontrar el jurado para el proyecto '{nombre_proyecto}'.",
        )

    return redirect(
        "correspondencia:ver_proyecto_final",
        nombre=nombre_proyecto,
    )


@login_required
@grupo_usuario("Correspondencia")
def eliminar_evaluador(request, id, nombre_anteproyecto):
    evaluacion = (
        ModelEvaluacionAnteproyecto.objects.get(id=id)
        if ModelEvaluacionAnteproyecto.objects.filter(id=id).exists()
        else None
    )

    if evaluacion:
        evaluacion.delete()
        messages.success(
            request,
            f"El evaluador del proyecto '{nombre_anteproyecto}' ha sido eliminada exitosamente.",
        )
    else:
        messages.error(
            request,
            f"No se pudo encontrar el evaluador para el proyecto '{nombre_anteproyecto}'.",
        )

    return redirect(
        "correspondencia:ver_anteproyecto",
        nombre_anteproyecto=nombre_anteproyecto,
    )


@login_required
@grupo_usuario("Correspondencia")
def asignar_fecha_sustentacion(request, id):
    proyecto = recuperar_proyecto_final_id(id)
    if proyecto:
        fechas_proyecto = recuperar_fechas_proyecto(proyecto)
        if fechas_proyecto:
            fechas_proyecto.fecha_sustentacion = request.POST.get("fecha_presentacion")
            fechas_proyecto.save()
            messages.success(
                request, "La fecha de sustentación ha sido asignada correctamente."
            )
            return redirect(
                "correspondencia:ver_proyecto_final",
                nombre=proyecto.anteproyecto.nombre_anteproyecto,
            )
        else:
            messages.error(
                request,
                "No se encontraron fechas asociadas al proyecto. Por favor, intente de nuevo.",
            )
            return redirect(
                "correspondencia:ver_proyecto_final",
                nombre=proyecto.anteproyecto.nombre_anteproyecto,
            )
    else:
        messages.error(
            request,
            "No se encontró el proyecto solicitado. Por favor, verifique la información e intente de nuevo.",
        )
        return redirect(
            "correspondencia:ver_proyecto_final",
            nombre=proyecto.anteproyecto.nombre_anteproyecto,
        )


@login_required
@grupo_usuario("Correspondencia")
def asignar_evaluadores_ante(request, id):
    anteproyecto = recuperar_anteproyecto_id(id)
    if anteproyecto:
        directores_evaluadores_id = request.POST.getlist("directores")

        for director_id in directores_evaluadores_id:
            usuario = recuperar_usuario(director_id)
            es_evaluador = verificar_evaluador(director_id)
            if es_evaluador:
                messages.error(
                    request,
                    f"El director {usuario.nombre_completo} ya fue asignado para evaluar el anteproyecto {anteproyecto.nombre_anteproyecto}",
                )
                return redirect(
                    "correspondencia:ver_anteproyecto",
                    nombre_anteproyecto=anteproyecto.nombre_anteproyecto,
                )

            evaluacion_anteproyecto = ModelEvaluacionAnteproyecto(
                evaluador=usuario,
                anteproyecto=anteproyecto,
                fecha_asignacion=fecha_actual(),
            )
            evaluacion_anteproyecto.save()
        messages.success(
            request,
            f"Los directores han sido asignados exitosamente para la evaluación del anteproyecto {anteproyecto.nombre_anteproyecto}.",
        )
        return redirect(
            "correspondencia:ver_anteproyecto",
            nombre_anteproyecto=anteproyecto.nombre_anteproyecto,
        )
    else:
        messages.error(
            request,
            f"Hubo un error al asignar los directores para la evaluación del anteproyecto {anteproyecto.nombre_anteproyecto}",
        )
    return redirect(
        "correspondencia:ver_anteproyecto",
        nombre_anteproyecto=anteproyecto.nombre_anteproyecto,
    )
    ########################################################################################################################

    # listado de solicitudes


@login_required
@grupo_usuario("Correspondencia")
def solicitudes_respondidas(request):
    respuestas = recuperar_solicitudes()
    context = datosusuario(request)
    respuestas_dict = {}
    for i, respuesta in enumerate(respuestas):
        doc_binario = recuperar_documento(respuesta.doc_retroalimentacion)
        if respuesta.proyecto_final:

            respuestas_dict[f"respuesta_{i}"] = {
                "respuesta_proyecto_final": respuesta,
                "doc_binario": doc_binario,
            }
        elif respuesta.anteproyecto:

            respuestas_dict[f"respuesta_{i}"] = {
                "respuesta_anteproyecto": respuesta,
                "doc_binario": doc_binario,
            }
    context["respuestas"] = respuestas_dict

    return render(
        request,
        "correspondencia/views_respuestas/list_solicitudes_respondidas.html",
        context,
    )


# vista de la respuesta mas detallada


@login_required
@grupo_usuario("Correspondencia")
def ver_respuesta(request, id):
    context = datosusuario(request)

    if id:

        respuesta = (
            ModelRetroalimentaciones.objects.get(id=id)
            if ModelRetroalimentaciones.objects.filter(id=id).exists()
            else "None"
        )
        if respuesta.anteproyecto:
            integrantes = (
                respuesta.anteproyecto.nombre_integrante1,
                respuesta.anteproyecto.nombre_integrante2,
                respuesta.anteproyecto.director,
                respuesta.anteproyecto.codirector,
            )
        elif respuesta.proyecto_final:
            integrantes = (
                respuesta.proyecto_final.anteproyecto.nombre_integrante1,
                respuesta.proyecto_final.anteproyecto.nombre_integrante2,
                respuesta.proyecto_final.anteproyecto.director,
                respuesta.proyecto_final.anteproyecto.codirector,
            )

        if respuesta:
            datos_integrantes = {}
            for i, integrante in enumerate(integrantes, start=1):
                if integrante:
                    datos_integrantes[f"integrante_{i}"] = recuperar_datos_integrantes(
                        integrante
                    )
            context["datos_integrantes"] = datos_integrantes

            doc_binario = respuesta.doc_retroalimentacion

            documento_respuesta = recuperar_documento(doc_binario)
            context["documento_respuesta"] = documento_respuesta
            context["respuesta"] = respuesta

            return render(
                request,
                "correspondencia/views_respuestas/visualizacion_respuesta.html",
                context,
            )
    return render(
        request, "correspondencia/views_respuestas/visualizacion_respuesta.html"
    )


########################################################################################################################
# vista de documentos cargados por los estudiantes
# def documentos_cargados(request):
#     return render(request, 'correspondencia/list_documentos_cargados.html')
########################################################################################################################


############################################################################


@login_required
@grupo_usuario("Correspondencia")
def formatos_documentos(request):
    context = datosusuario(request)
    if request.method == "POST":
        form_cargar_docs = FormDocumentos(request.POST, request.FILES)
        if form_cargar_docs.is_valid():
            cargar_documentos = form_cargar_docs.save(commit=False)
            cargar_documentos.fecha_cargue = fecha_actual()
            cargar_documentos.save()
            return redirect("correspondencia:formatos_documentos")
        else:
            return HttpResponse(f"Error: {form_cargar_docs.errors}")
    else:
        form_cargar_docs = FormDocumentos
        context["formatos"] = recuperar_formatos()
        context["form_cargar_docs"] = form_cargar_docs

    return render(
        request, "correspondencia/views_formatos/documentos_comite.html", context
    )


# funcion para eliminar un formato cargado
def eliminar_formato(request, id):
    formato_id = id
    formato = ModelDocumentos.objects.get(id=formato_id)
    formato.delete()
    return redirect("correspondencia:formatos_documentos")


# funcion para editar un formato
def editar_formato(request, id):
    context = datosusuario(request)
    formato = ModelDocumentos.objects.get(id=id)

    if request.method == "POST":
        form_cargar_docs = FormDocumentos(request.POST, request.FILES, instance=formato)
        if form_cargar_docs.is_valid():
            form_cargar_docs.save()
            return redirect("correspondencia:formatos_documentos")

            # return redirect('nombre_de_tu_vista_de_exito')  # Redirige a una vista de éxito
    else:
        form_cargar_docs = FormDocumentos(instance=formato)

    doc_convert = formato.documento
    documento = recuperar_documento(doc_convert)
    context = {
        "form_edit": form_cargar_docs,
        "documento": documento,
    }
    return render(request, "correspondencia/views_formatos/formato.html", context)


#####################################################################################################################
# apartado de la lista de proyectos


@login_required
@grupo_usuario("Correspondencia")
def proyectos(request):
    context = datosusuario(request)
    num_proyectos_terminados = recuperar_num_proyectos_terminados()
    num_proyectos_actuales = recuperar_num_proyectos_pendientes()
    context["num_proyectos_actuales"] = num_proyectos_actuales
    context["num_proyectos_terminados"] = num_proyectos_terminados
    return render(request, "correspondencia/views_proyectos/proyectos.html", context)


@login_required
@grupo_usuario("Correspondencia")
def proyectos_finalizados(request):
    context = datosusuario(request)
    list_proyectos_finalizados = recuperar_proyectos_finalizados()
    dic_proyectos = {}
    if list_proyectos_finalizados:

        for i, proyecto in enumerate(list_proyectos_finalizados):
            documento_convert = proyecto.proyecto_final.proyecto_final
            documento = recuperar_documento(documento_convert)

            dic_proyectos[f"proyecto{i}"] = {
                "proyecto": proyecto,
                "documento_convert": documento,
            }
        context["proyectos"] = dic_proyectos
    return render(
        request,
        "correspondencia/views_proyectos/list_proyectos_finalizados.html",
        context,
    )


@login_required
@grupo_usuario("Correspondencia")
def proyectos_actuales(request):
    context = datosusuario(request)
    proyectos_actuales = recuperar_proyectos_pendientes()
    dic_proyectos = {}
    if proyectos_actuales:
        for i, proyecto in enumerate(proyectos_actuales):
            fechas_proyectos = (
                ModelFechasProyecto.objects.get(proyecto_final=proyecto)
                if ModelFechasProyecto.objects.filter(proyecto_final=proyecto).exists()
                else None
            )
            dic_proyectos[f"proyecto{i}"] = {
                "proyecto": proyecto,
                "fecha_inicio": fechas_proyectos.fecha_inicio,
                "fecha_finalizacion": fecha_culminacion_anteproyecto(
                    fechas_proyectos.fecha_inicio
                ),
            }
        context["proyectos"] = dic_proyectos
    return render(
        request, "correspondencia/views_proyectos/list_proyectos_actuales.html", context
    )


@login_required
@grupo_usuario("Correspondencia")
def proyecto_final(request, id):
    context = datosusuario(request)

    proyecto = (
        ModelInformacionEntregaFinal.objects.get(id=id)
        if ModelInformacionEntregaFinal.objects.filter(id=id).exists()
        else None
    )
    documento_cedido = recuperar_documento(proyecto.doc_proyecto_final_cedido)
    if documento_cedido:
        context["documento_cedido"] = documento_cedido
    integrantes = (
        proyecto.anteproyecto.nombre_integrante1,
        proyecto.anteproyecto.nombre_integrante2,
        proyecto.anteproyecto.director,
        proyecto.anteproyecto.codirector,
    )
    datos_integrantes = {}
    for i, integrante in enumerate(integrantes, start=1):
        if integrante:
            datos_integrantes[f"integrante_{i}"] = recuperar_datos_integrantes(
                integrante
            )
        context["datos_integrantes"] = datos_integrantes
    context["proyecto"] = proyecto
    carta_convert = recuperar_documento(proyecto.anteproyecto.carta_presentacion)
    ante_convert = recuperar_documento(proyecto.anteproyecto.anteproyecto)
    carta_final_convert = recuperar_documento(
        proyecto.proyecto_final.carta_presentacion_final
    )
    proyecto__final_convert = recuperar_documento(
        proyecto.proyecto_final.proyecto_final
    )

    retroalimentaciones = recuperar_solicitudes_anteproyecto()
    retroalimentaciones_proyecto_final = recuperar_retroalimentaciones_proyecto_final(
        proyecto.proyecto_final
    )
    if retroalimentaciones_proyecto_final:
        context["retroalimentaciones_proyecto_final"] = (
            retroalimentaciones_proyecto_final
        )
    if retroalimentaciones:
        dic_retroalimentaciones = {}
        for i, retroalimentacion in enumerate(retroalimentaciones):

            dic_retroalimentaciones[f"retroalimentacion{i}"] = {
                "doc_retroalimentacion": recuperar_documento(
                    retroalimentacion.doc_retroalimentacion
                ),
                "fecha_retroalimentacion": retroalimentacion.fecha_retroalimentacion,
                "respuesta": retroalimentacion.retroalimentacion,
            }

            context["retroalimentaciones"] = dic_retroalimentaciones

        context["formatos"] = {
            "anteproyecto": ante_convert,
            "carta_presentacion": carta_convert,
            "anteproyecto": ante_convert,
            "proyecto__final_convert": carta_final_convert,
        }

    solicitudes_especiales = recuperar_solicitudes_especiales_proyecto(
        proyecto.proyecto_final, proyecto.anteproyecto
    )
    dict_solicitudes = {}
    if solicitudes_especiales:
        for i, solicitud_especial in enumerate(solicitudes_especiales):
            dict_solicitudes[f"solicitud{i}"] = {
                "doc_solicitudes": solicitud_especial.documento_soporte,
                "fecha_envio": solicitud_especial.fecha_envio,
            }
        context["solicitudes"] = dict_solicitudes
    return render(
        request, "correspondencia/views_proyectos/proyecto_finalizado.html", context
    )


@login_required
@grupo_usuario("Correspondencia")
def proyecto_actual(request, id):
    context = datosusuario(request)
    proyecto = recuperar_proyecto_actual(id)
    fechas_proyecto = (
        ModelFechasProyecto.objects.get(proyecto_final=proyecto)
        if ModelFechasProyecto.objects.filter(proyecto_final=proyecto).exists()
        else None
    )
    if fechas_proyecto:
        context["fechas"] = fechas_proyecto
        context["fecha_finalizacion"] = fecha_culminacion_anteproyecto(
            fechas_proyecto.fecha_inicio
        )
    integrantes = (
        proyecto.anteproyecto.nombre_integrante1,
        proyecto.anteproyecto.nombre_integrante2,
        proyecto.anteproyecto.director,
        proyecto.anteproyecto.codirector,
    )
    retroalimentaciones_proyecto_final = recuperar_retroalimentaciones_proyecto_final(
        proyecto
    )
    print(retroalimentaciones_proyecto_final)
    if retroalimentaciones_proyecto_final:
        context["retroalimentaciones_proyecto_final"] = (
            retroalimentaciones_proyecto_final
        )
    datos_integrantes = {}
    for i, integrante in enumerate(integrantes, start=1):
        if integrante:
            datos_integrantes[f"integrante_{i}"] = recuperar_datos_integrantes(
                integrante
            )
        context["datos_integrantes"] = datos_integrantes
    context["proyecto"] = proyecto
    carta_convert = recuperar_documento(proyecto.anteproyecto.carta_presentacion)
    ante_convert = recuperar_documento(proyecto.anteproyecto.anteproyecto)
    radicado_convert = recuperar_documento(proyecto.anteproyecto.documento_radicado)
    concepto_convert = recuperar_documento(proyecto.anteproyecto.documento_concepto)

    retroalimentaciones = recuperar_solicitudes_anteproyecto()

    if retroalimentaciones:
        dic_retroalimentaciones = {}
        for i, retroalimentacion in enumerate(retroalimentaciones):

            dic_retroalimentaciones[f"retroalimentacion{i}"] = {
                "doc_retroalimentacion": recuperar_documento(
                    retroalimentacion.doc_retroalimentacion
                ),
                "fecha_retroalimentacion": retroalimentacion.fecha_retroalimentacion,
                "respuesta": retroalimentacion.retroalimentacion,
            }

            context["retroalimentaciones"] = dic_retroalimentaciones

        context["formatos"] = {
            "anteproyecto": ante_convert,
            "carta_presentacion": carta_convert,
            "radicado_convert": radicado_convert,
            "concepto_convert": concepto_convert,
        }
    return render(
        request, "correspondencia/views_proyectos/proyecto_actual.html", context
    )


#####################################################################################################################


def recuperar_directores_usuario():
    directores = Usuarios.objects.filter(groups__name="Directores")
    if directores:
        return directores
    else:
        directores = None
        return directores


def num_solicitudes_ante():
    numero = ModelAnteproyecto.objects.filter(Q(solicitud_enviada=True) & Q(estado=False)).count()
    return numero


def num_solicitudes_final():
    numero = ModelProyectoFinal.objects.filter(Q(solicitud_enviada=True) & Q(estado=False)).count()
    return numero


def num_solicitudes_esp():
    numero = ModelSolicitudes.objects.filter(estado=True).count()
    return numero


def num_proyectos_curso():
    numero = ModelProyectoFinal.objects.filter(estado=False).count()
    return numero


def num_proyectos_terminados():
    numero = ModelInformacionEntregaFinal.objects.all().count()
    return numero


@login_required
@grupo_usuario("Correspondencia")
def carga(request):
    context = datosusuario(request)
    directores = recuperar_directores_usuario()
    context["num_solicitudes_ante"] = num_solicitudes_ante()
    context["num_solicitudes_final"] = num_solicitudes_final()
    context["num_solicitudes_esp"] = num_solicitudes_esp()
    context["num_proyectos_curso"] = num_proyectos_curso()
    context["num_proyectos_terminados"] = num_proyectos_terminados()

    if directores:
        dic_informacion_carga_directores = {}
        for i, director in enumerate(directores):
            usuario = director
            evaluaciones_anteproyecto_pendientes = (
                num_evaluaciones_anteproyecto_pendientes_director(usuario)
            )
            print(
                "Evaluaciones de anteproyecto pendientes:",
                evaluaciones_anteproyecto_pendientes,
            )

            evaluaciones_proyecto_final_pendientes = (
                num_evaluaciones_proyecto_final_pendientes_director(usuario)
            )
            print(
                "Evaluaciones de proyecto final pendientes:",
                evaluaciones_proyecto_final_pendientes,
            )
            num_anteproyectos_pendientes = num_anteproyecto_pendientes_director(usuario)
            print("Número de anteproyectos pendientes:", num_anteproyectos_pendientes)
            num_proyectos_pendientes = num_proyecto_final_pendientes_director(usuario)
            print("Número de proyectos pendientes:", num_proyectos_pendientes)

            nombre = director.nombre_completo
            dic_informacion_carga_directores[f"director_{i}"] = {
                "nombre_completo": nombre,
                "evaluaciones_anteproyecto_pendientes": evaluaciones_anteproyecto_pendientes,
                "evaluaciones_proyecto_final_pendientes": evaluaciones_proyecto_final_pendientes,
                "num_anteproyectos_pendientes": num_anteproyectos_pendientes,
                "num_proyectos_pendientes": num_proyectos_pendientes,
            }
        context["carga_directores"] = dic_informacion_carga_directores

    return render(request, "correspondencia/info_carga/carga.html", context)
