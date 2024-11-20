# get_object_or_404 para el manejo de errores si no se encuentra un modelo con los siguientes datos
from datetime import datetime, date
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from dateutil.relativedelta import relativedelta


from django.contrib.auth.decorators import login_required

# formularios
from correspondencia.forms import FormSolicitudes
from .forms import (
    FormAnteproyecto,
    FormProyectoFinal,
    FormObjetivoGeneral,
    FormObjetivosEspecificos,
    FormActividades,
)

# modelos
from login.models import Usuarios
from .models import (
    ModelAnteproyecto,
    ModelProyectoFinal,
    ModelObjetivoGeneral,
    ModelObjetivosEspecificos,
    ModelActividades,
    ModelFechasProyecto,
)
import base64

# modelo de correspondencia
from correspondencia.models import (
    ModelInformacionEntregaFinal,
    ModelRetroalimentaciones,
    ModelSolicitudes,
)

# importacion de modelos del director
from director.models import ModelEvaluacionAnteproyecto, ModelEvaluacionProyectoFinal

# importacion de la vista del login que permite cambiar la informacion de ususario
from login.views import editar_usuario

# importacion del formulario para editar el usuario
from login.forms import FormEditarUsuario

# importacion de las funcionalidaes
from plataform_CIGAP.utils.decoradores import grupo_usuario
from plataform_CIGAP.utils.funcionalidades_fechas import (
    fecha_actual,
    fecha_maxima_respuesta,
    fecha_culminacion_anteproyecto,
)

# importacion de recuperaciones
from plataform_CIGAP.utils.recuperaciones import (
    recuperar_fechas_comite,
    recuperar_formatos,
    datosusuario,
)

# Create your views here.

# vista de funcionamiento respecto a la url de la aplicacion
# def funcionando(request):
#     return HttpResponse('app_ estudiante funcionando.')

# recuperar proyecto final por usuario, integrante 1 o 2


def recuperar_proyecto_final_id(id):
    proyecto_final = ModelProyectoFinal.objects.get(id=id)
    return proyecto_final


def recuperar_proyecto_final_usuario(user):
    proyecto = (
        ModelProyectoFinal.objects.get(
            Q(user=user)
            | Q(anteproyecto__nombre_integrante1=user.nombre_completo)
            | Q(anteproyecto__nombre_integrante2=user.nombre_completo)
        )
        if ModelProyectoFinal.objects.filter(
            Q(user=user)
            | Q(anteproyecto__nombre_integrante1=user.nombre_completo)
            | Q(anteproyecto__nombre_integrante2=user.nombre_completo)
        ).exists()
        else None
    )
    return proyecto


# recuperar retralimentacion por anteproyecto


def recuperar_directores():
    directores = list(
        Usuarios.objects.filter(groups__name="Directores").values(
            "id", "nombre_completo", "email"
        )
    )
    return directores


def recuperar_retroalimentacion_anteproyecto(anteproyecto):
    retroalimentacion = ModelRetroalimentaciones.objects.filter(
        Q(anteproyecto=anteproyecto) & Q(estado="Aprobado")
    ).first()
    if not retroalimentacion:
        return None
    return retroalimentacion


def recuperar_retroalimentacion_proyecto_final(proyecto):
    retroalimentaciones = ModelRetroalimentaciones.objects.filter(
        Q(proyecto_final=proyecto)
    )
    if not retroalimentaciones:
        return None
    return retroalimentaciones


# recuperar anteproyecto por id
def recuperar_anteproyecto_id(id):
    anteproyecto = ModelAnteproyecto.objects.get(id=id)
    if not anteproyecto:
        return None
    return anteproyecto


# recuperacion de las observaciones de anteproyecto


def recuperar_observaciones_anteproyecto(anteproyecto):
    observaciones = ModelRetroalimentaciones.objects.filter(anteproyecto=anteproyecto)
    if not observaciones:
        return None
    return observaciones


# recuperacion de las observaciones de proyecto


def recuperar_observaciones_proyecto_final(proyecto):
    observaciones = ModelEvaluacionAnteproyecto.objects.filter(proyecto_final=proyecto)
    if not observaciones:
        return None
    return observaciones


# funcion para devolver documentos o imagenes
def devolver_documento_imagen(documento_binario):
    documento = (
        base64.b64encode(documento_binario).decode("utf-8")
        if documento_binario
        else None
    )
    return documento


def recuperar_proyecto_perteneciente(nombre):
    anteproyecto = (
        ModelAnteproyecto.objects.get(
            Q(nombre_integrante1=nombre) | Q(nombre_integrante2=nombre)
        )
        if ModelAnteproyecto.objects.filter(
            Q(nombre_integrante1=nombre) | Q(nombre_integrante2=nombre)
        ).exists()
        else None
    )
    return anteproyecto


@login_required
def datosusuario(request):
    nombre_usuario = request.user.nombre_completo
    anteproyecto = recuperar_proyecto_perteneciente(nombre_usuario)
    usuario = request.user
    imagen = usuario.imagen
    imagen_convertida = base64.b64encode(imagen).decode("utf-8") if imagen else ""
    form_editar_usuario = FormEditarUsuario(instance=usuario)
    form_solicitud = FormAnteproyecto
    fechas_comite = recuperar_fechas_comite()
    ano_actual = datetime.now().year
    if anteproyecto:
        context = {
            "ano_actual": ano_actual,
            "fechas_comite": fechas_comite,
            "form_anteproyecto": form_solicitud,
            "form_config": form_editar_usuario,
            "usuario": usuario,
            "user_img": imagen_convertida,
            "nombre_anteproyecto": anteproyecto.nombre_anteproyecto,
        }

    else:
        context = {
            "ano_actual": ano_actual,
            "fechas_comite": fechas_comite,
            "form_anteproyecto": form_solicitud,
            "form_config": form_editar_usuario,
            "usuario": usuario,
            "user_img": imagen_convertida,
            "nombre_anteproyecto": None,
        }
    return context


# funcion para devolver un diccionario con los datos del proyecto
@login_required
@grupo_usuario("Estudiantes")
def contenido_anteproyecto(request):

    try:
        fechas_comite = recuperar_fechas_comite()
        ano_actual = datetime.now().year
        content_anteproyecto = (
            ModelAnteproyecto.objects.get(user=request.user)
            if ModelAnteproyecto.objects.filter(user=request.user).exists()
            else None
        )
        if content_anteproyecto == None:
            usuario = request.user
            imagen = usuario.imagen
            imagen_convertida = (
                base64.b64encode(imagen).decode("utf-8") if imagen else ""
            )
            form_editar_usuario = FormEditarUsuario(instance=request.user)
            context_anteproyecto = {
                "ano_actual": ano_actual,
                "fechas_comite": fechas_comite,
                "usuario": usuario,
                "user_img": imagen_convertida,
                "form_config": form_editar_usuario,
            }
            return context_anteproyecto

        else:
            usuario = request.user
            imagen = usuario.imagen
            imagen_convertida = (
                base64.b64encode(imagen).decode("utf-8") if imagen else ""
            )
            carta_presentacion_binario = content_anteproyecto.carta_presentacion
            anteproyecto_binario = content_anteproyecto.anteproyecto
            carta_presentacion = devolver_documento_imagen(carta_presentacion_binario)
            anteproyecto = devolver_documento_imagen(anteproyecto_binario)
            form_editar_usuario = FormEditarUsuario(instance=request.user)
            context_anteproyecto = {
                "ano_actual": ano_actual,
                "fechas_comite": fechas_comite,
                "usuario": usuario,
                "user_img": imagen_convertida,
                "form_config": form_editar_usuario,
                "nombre_anteproyecto": content_anteproyecto.nombre_anteproyecto,
                "integrante1": content_anteproyecto.nombre_integrante1,
                "integrante2": content_anteproyecto.nombre_integrante2,
                "director": content_anteproyecto.director,
                "descripcion": content_anteproyecto.descripcion,
                "carta": carta_presentacion,
                "fecha_envio": content_anteproyecto.fecha_envio,
                "anteproyecto": anteproyecto,
                "solicitud_enviada": content_anteproyecto.solicitud_enviada,
                "codirector": content_anteproyecto.codirector,
            }

    except ObjectDoesNotExist:
        context_anteproyecto = {
            "solicitud_enviada": False,
        }
    except Exception as e:
        print(f"Error: {e}")
        context_anteproyecto = {
            "solicitud_enviada": False,
        }

    return context_anteproyecto


# funcion para recuperar las retroalimentaciones de correspondencia
def recuperar_retroalimentacion(anteproyecto_):
    retroalimentaciones = (
        ModelRetroalimentaciones.objects.filter(
            anteproyecto=anteproyecto_,
            estado__in=["Aprobado", "Aprobado_con_correciones"],
        ).first()
        if ModelRetroalimentaciones.objects.filter(anteproyecto=anteproyecto_).exists()
        else None
    )
    if retroalimentaciones:
        doc_convert = devolver_documento_imagen(
            retroalimentaciones.doc_retroalimentacion
        )
        return {"respuesta": retroalimentaciones, "doc_retroalimentacion": doc_convert}
    else:
        return None


def recuperar_retroalimentaciones(anteproyecto_):

    retroalimentaciones = ModelRetroalimentaciones.objects.filter(
        anteproyecto=anteproyecto_
    )
    respuestas = {}
    if retroalimentaciones.exists():
        for i, retroalimentacion in enumerate(retroalimentaciones):
            doc_convert = devolver_documento_imagen(
                retroalimentacion.doc_retroalimentacion
            )
            respuestas[f"retroalimentacion_{i}"] = {
                "respuesta": retroalimentacion,
                "doc_retroalimentacion": doc_convert,
            }
    return respuestas if respuestas else None


def recuperar_retroalimentaciones_proyecto_final(proyecto_final):

    retroalimentaciones = ModelRetroalimentaciones.objects.filter(
        proyecto_final=proyecto_final
    )
    respuestas = {}
    if retroalimentaciones.exists():
        for i, retroalimentacion in enumerate(retroalimentaciones):
            doc_convert = devolver_documento_imagen(
                retroalimentacion.doc_retroalimentacion
            )
            respuestas[f"retroalimentacion_{i}"] = {
                "respuesta": retroalimentacion,
                "doc_retroalimentacion": doc_convert,
            }
    return respuestas if respuestas else None


# funcion parea recuperar el anteproyecto


@login_required
@grupo_usuario("Estudiantes")
def recuperar_anteproyecto(request):
    anteproyecto = (
        ModelAnteproyecto.objects.get(
            Q(user=request.user)
            | Q(nombre_integrante1=request.user.nombre_completo)
            | Q(nombre_integrante2=request.user.nombre_completo)
        )
        if ModelAnteproyecto.objects.filter(
            Q(user=request.user)
            | Q(nombre_integrante1=request.user.nombre_completo)
            | Q(nombre_integrante2=request.user.nombre_completo)
        ).exists()
        else None
    )
    if not anteproyecto:
        return None
    return anteproyecto


# funcion para recuperar el proyecto final


def recuperar_proyecto_final(anteproyecto):
    proyecto_final = (
        ModelProyectoFinal.objects.get(anteproyecto=anteproyecto)
        if ModelProyectoFinal.objects.filter(anteproyecto=anteproyecto).exists()
        else None
    )
    return proyecto_final


@login_required
@grupo_usuario("Estudiantes")
def principal_estudiante(request):

    if request.method == "POST":
        editar_usuario(request)
    else:
        context = datosusuario(request)
        anteproyecto = recuperar_anteproyecto(request)
        if anteproyecto:
            context["anteproyecto"] = anteproyecto
        retroalimentacion_anteproyecto = recuperar_retroalimentacion_anteproyecto(
            anteproyecto
        )
        if retroalimentacion_anteproyecto:
            context["retroalimentacion_anteproyecto"] = retroalimentacion_anteproyecto
            context["fecha_culminacion_anteproyecto"] = fecha_culminacion_anteproyecto(
                retroalimentacion_anteproyecto.fecha_retroalimentacion
            )

        proyecto_final = recuperar_proyecto_final(anteproyecto)
        if proyecto_final:
            context["proyecto_final"] = proyecto_final
            context["nombre_anteproyecto"] = (
                anteproyecto.nombre_anteproyecto
                if anteproyecto
                else "No hay anteproyecto"
            )

    return render(request, "estudiante/base_estudiante.html", context)


def recuperar_solicitud_especifica_aceptada(anteproyecto):
    solicitudes_especificas = ModelSolicitudes.objects.filter(
        Q(anteproyecto=anteproyecto) & Q(estado=True)
    ).order_by("-id")

    return solicitudes_especificas.first() if solicitudes_especificas.exists() else None


@login_required
@grupo_usuario("Estudiantes")
def solicitud(request):
    context = datosusuario(request)
    directores = recuperar_directores()
    context["directores"] = directores
    if request.method == "POST":

        nombre_integrante2 = request.POST.get("nombre_integrante2")

        if nombre_integrante2:
            usuario = Usuarios.objects.filter(nombre_completo=nombre_integrante2)
            if not usuario:
                messages.error(
                    request,
                    f"El estudiante {nombre_integrante2} no está registrado en la plataforma. Por favor, infórmalo para proceder con su registro y continuar con el proceso.",
                )
                return redirect("estudiante:solicitud")
            existing_anteproyecto = ModelAnteproyecto.objects.filter(
                Q(nombre_integrante2=nombre_integrante2)
                | Q(nombre_integrante1=nombre_integrante2)
            )
            if existing_anteproyecto:
                messages.error(
                    request,
                    f"El estudiante {nombre_integrante2} actualmente ya esta vinculado a otro anteproyecto.",
                )
                return redirect("estudiante:info_proyect")
        # Verificamos si el estudiante ya tiene un anteproyecto.
        try:
            # Buscamos un anteproyecto donde el usuario sea el creador o uno de los integrantes
            existing_anteproyecto = ModelAnteproyecto.objects.get(user=request.user)
            messages.warning(
                request,
                "Ya tienes un anteproyecto creado. No puedes crear otro hasta que el actual sea evaluado.",
            )
            return redirect("estudiante:info_proyect")
        except ModelAnteproyecto.DoesNotExist:
            try:
                existing_anteproyecto1 = ModelAnteproyecto.objects.get(
                    nombre_integrante1=request.user.nombre_completo
                )
                messages.warning(
                    request,
                    "Ya tienes un anteproyecto creado. No puedes crear otro hasta que el actual sea evaluado.",
                )
                return redirect("estudiante:info_proyect")
            except ModelAnteproyecto.DoesNotExist:
                try:
                    existing_anteproyecto2 = ModelAnteproyecto.objects.get(
                        nombre_integrante2=request.user.nombre_completo
                    )
                    messages.warning(
                        request,
                        "Ya tienes un anteproyecto creado. No puedes crear otro hasta que el actual sea evaluado.",
                    )
                    return redirect("estudiante:info_proyect")
                except ModelAnteproyecto.DoesNotExist:

                    # Obtener valores del POST y FILES
                    director = request.POST.get("director")
                    codirector = request.POST.get("codirector")

                    # Validaciones previas a guardar el nuevo anteproyecto
                    if not director or director.strip() == "":
                        messages.error(request, "Debe seleccionar un director.")
                        return redirect("estudiante:solicitud")

                    if director == codirector:
                        messages.error(
                            request,
                            "El director y el codirector no pueden ser la misma persona.",
                        )
                        return redirect("estudiante:solicitud")

                    # Crear nuevo anteproyecto solo si las validaciones anteriores pasan
                    new_anteproyecto = ModelAnteproyecto(
                        user=request.user,
                        nombre_anteproyecto=request.POST.get("nombre_anteproyecto"),
                        nombre_integrante1=request.POST.get("nombre_integrante1"),
                        nombre_integrante2=request.POST.get("nombre_integrante2"),
                        descripcion=request.POST.get("descripcion"),
                        carta_presentacion=(
                            request.FILES.get("carta_presentacion_convert").read()
                            if request.FILES.get("carta_presentacion_convert")
                            else None
                        ),
                        anteproyecto=(
                            request.FILES.get("anteproyecto_convert").read()
                            if request.FILES.get("anteproyecto_convert")
                            else None
                        ),
                        director=director,
                        codirector=codirector,
                        fecha_envio=fecha_actual(),
                    )

                    # Guardar el anteproyecto si todo está correcto
                    new_anteproyecto.save()

                    messages.success(
                        request,
                        f"El proyecto '{new_anteproyecto.nombre_anteproyecto}' ha sido enviado al director y codirector para las retroalimentaciones pertinentes.",
                    )
                    return redirect("estudiante:info_proyect")

                    # # Mensaje de error si el formulario no es válido
                    # messages.error(
                    #     request, "Hubo un problema al enviar el formulario. Por favor, verifica los campos y vuelve a intentarlo.")

    # Si el método es GET, buscamos el anteproyecto del usuario actual.
    else:
        try:
            anteproyecto = recuperar_anteproyecto(request)
            if anteproyecto:

                solicitud_especifica_pendiente = (
                    ModelSolicitudes.objects.get(
                        Q(anteproyecto=anteproyecto) & Q(estado=False)
                    )
                    if ModelSolicitudes.objects.filter(
                        Q(anteproyecto=anteproyecto) & Q(estado=False)
                    ).exists()
                    else None
                )
                if solicitud_especifica_pendiente:
                    context["solicitud_especifica_pendiente"] = (
                        solicitud_especifica_pendiente
                    )
                solicitd_especifica = recuperar_solicitud_especifica_aceptada(
                    anteproyecto
                )
                if solicitd_especifica:
                    context["solicitud_especifica"] = solicitd_especifica
                context["anteproyecto"] = anteproyecto

                if anteproyecto.fecha_envio:
                    context["fecha_respuesta_maxima"] = fecha_maxima_respuesta(
                        anteproyecto.fecha_envio
                    )
                observaciones_anteproyecto = recuperar_observaciones_anteproyecto(
                    anteproyecto
                )
                if observaciones_anteproyecto:
                    dict_observaciones = {}
                    for i, observacion in enumerate(observaciones_anteproyecto):
                        # Crea un nuevo diccionario para cada observación
                        dict_observaciones[f"observacion{i}"] = {
                            "observacion": observacion,
                            "doc_evaluacion_anteproyecto": devolver_documento_imagen(
                                observacion.doc_retroalimentacion
                            ),
                        }
                        context["observaciones"] = dict_observaciones
            proyecto_final = recuperar_proyecto_final(anteproyecto)
            if proyecto_final:
                fechas_proyecto = (
                    ModelFechasProyecto.objects.get(proyecto_final=proyecto_final)
                    if ModelFechasProyecto.objects.filter(
                        proyecto_final=proyecto_final
                    ).exists()
                    else None
                )
                if fechas_proyecto:
                    context["fechas_proyecto"] = fechas_proyecto
                    fechas_estimada_finalizacion = (
                        fechas_proyecto.fecha_inicio + relativedelta(months=6)
                    )
                    context["fecha_finalizacion"] = fechas_estimada_finalizacion
            content_anteproyecto = ModelAnteproyecto.objects.get(user=request.user)
        except ModelAnteproyecto.DoesNotExist:
            content_anteproyecto = None
            messages.warning(
                request, "No se encontró ningún anteproyecto asociado a tu cuenta."
            )

        if content_anteproyecto:
            estado = content_anteproyecto.solicitud_enviada
            existe_solicitud = content_anteproyecto.solicitud_enviada
            nombre_anteproyecto = content_anteproyecto.nombre_anteproyecto
            form_anteproyecto = FormAnteproyecto(instance=content_anteproyecto)
            context["form_anteproyecto"] = form_anteproyecto

            if existe_solicitud:
                context["existe_solicitud"] = existe_solicitud
                context["nombre_anteproyecto"] = nombre_anteproyecto
                context["fecha_envio"] = content_anteproyecto.fecha_envio
                messages.info(
                    request,
                    f"La solicitud para el proyecto '{nombre_anteproyecto}' ya fue enviada anteriormente.",
                )

        # lógica para saber si el proyecto fue aceptado
        context["respuesta"] = recuperar_retroalimentacion(content_anteproyecto)

        form_proyecto_final = FormProyectoFinal
        context["form_proyecto_final"] = form_proyecto_final
        form_solicitudes = FormSolicitudes
        context["form_solicitudes"] = form_solicitudes
        if proyecto_final:
            context["proyecto_final"] = proyecto_final

        return render(request, "estudiante/solicitud.html", context)


@login_required
@grupo_usuario("Estudiantes")
def actualizar_documentos_anteproyecto(request, id):
    anteproyecto = recuperar_anteproyecto_id(id)

    if anteproyecto:
        if "carta_anteproyecto" in request.FILES:
            anteproyecto.carta_presentacion = request.FILES.get(
                "carta_anteproyecto"
            ).read()
        if "anteproyecto" in request.FILES:
            anteproyecto.anteproyecto = request.FILES.get("anteproyecto").read()
            anteproyecto.save()
            messages.success(
                request, "El documento del anteproyecto se actualizó correctamente."
            )
        else:
            messages.warning(
                request, "No se encontró el archivo del anteproyecto para actualizar."
            )
    else:
        messages.error(
            request, "No se encontró el anteproyecto con el ID proporcionado."
        )

    return redirect("estudiante:solicitud")


# funcion de solicitudes especificas


@login_required
@grupo_usuario("Estudiantes")
def solicitudes_especificas(request):
    if request.method == "POST":
        form = FormSolicitudes(request.POST, request.FILES)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.user = request.user
            solicitud.anteproyecto = recuperar_anteproyecto(request)
            solicitud.fecha_envio = fecha_actual()
            solicitud.estado = False
            solicitud.save()

            messages.success(request, "Solicitud enviada con éxito.")
            return redirect("estudiante:solicitud")
        else:
            # Enviar mensaje de error si el formulario no es válido
            messages.error(
                request,
                "Error en el formulario. Por favor, revisa los datos ingresados.",
            )
            return redirect("estudiante:solicitud")
    else:
        # Enviar mensaje de error si no es un POST
        messages.error(request, "Método de solicitud no permitido.")
        return HttpResponse("Algo ocurrió.")


#####################################################################################################################################
# vista de la informacion del proyecto


@login_required
@grupo_usuario("Estudiantes")
def info_proyect(request):
    context = datosusuario(request)
    if request.method == "POST":
        context = contenido_anteproyecto(request)

        return render(request, "estudiante/Inf_proyect.html", context)
    else:
        context = contenido_anteproyecto(request)
        if context is None:
            context = {}
        anteproyecto = recuperar_anteproyecto(request)
        proyecto_final = recuperar_proyecto_final(anteproyecto)
        retroalimentaciones = recuperar_retroalimentaciones(anteproyecto)
        retroalimentaciones_proyecto_final = (
            recuperar_retroalimentaciones_proyecto_final(proyecto_final)
        )
        if recuperar_retroalimentaciones_proyecto_final:
            context["retroalimentaciones_proyecto_final"] = (
                retroalimentaciones_proyecto_final
            )

        if proyecto_final:
            doc_proyecto_final = devolver_documento_imagen(
                proyecto_final.proyecto_final
            )
            carta_presentacion_final = devolver_documento_imagen(
                proyecto_final.carta_presentacion_final
            )
            context["doc_proyecto_final"] = doc_proyecto_final
            context["carta_presentacion_final"] = carta_presentacion_final
            context["proyecto_final"] = proyecto_final
        if retroalimentaciones:
            context["content_retroalimentacion"] = retroalimentaciones

            return render(request, "estudiante/Inf_proyect.html", context)
        else:
            doc_revisado = None
            context["content_retroalimentacion"] = retroalimentaciones

            return render(request, "estudiante/Inf_proyect.html", context)


@login_required
@grupo_usuario("Estudiantes")
def enviar_solicitud_proyecto(request):

    if request.method == "POST":
        anteproyecto = recuperar_anteproyecto(request)

        form = FormProyectoFinal(request.POST, request.FILES)
        if form.is_valid():
            proyecto_final = form.save(commit=False)
            proyecto_final.user = request.user
            proyecto_final.anteproyecto = anteproyecto
            proyecto_final.descripcion = anteproyecto.descripcion
            proyecto_final.director = anteproyecto.director
            proyecto_final.estado = False
            proyecto_final.codirector = anteproyecto.codirector
            proyecto_final.solicitud_enviada = True
            proyecto_final.fecha_envio = fecha_actual()

            return redirect("estudiante:solicitud")
        else:
            print(f"Errores del formulario: {form.errors}")

    return redirect("estudiante:solicitud")


#####################################################################################################################################
# Avances del proyecto


# def recuperar_objetivo_general_id(id):
#     obj_general = ModelObjetivoGeneral.objects.get(id=id)
#     if not obj_general:
#         return None
#     return obj_general


def recuperar_objetivo_general(proyecto):
    obj_general = (
        ModelObjetivoGeneral.objects.get(proyecto_final=proyecto)
        if ModelObjetivoGeneral.objects.filter(proyecto_final=proyecto).exists()
        else None
    )
    return obj_general


def recuperar_objetivo_especifico(id):
    obj_especifico = ModelObjetivosEspecificos.objects.get(id=id)
    if not obj_especifico:
        return None
    return obj_especifico


def recuperar_objetivos_especificos(objetivo):
    obj_especifico = ModelObjetivosEspecificos.objects.filter(objetivo_general=objetivo)
    if not obj_especifico:
        return None
    return obj_especifico


def recuperar_actividades(objetivo_esp):
    actividades = ModelActividades.objects.filter(objetivos_especificos=objetivo_esp)
    if not actividades:
        return None
    return actividades


@login_required
@grupo_usuario("Estudiantes")
def cargar_editar_documento_cedido(request, id):
    if request.method == "POST":
        documento_cedido = request.FILES.get("documento_final")

        if documento_cedido:
            infomacion_final = ModelInformacionEntregaFinal.objects.filter(
                id=id
            ).first()

            if infomacion_final:
                infomacion_final.doc_proyecto_final_cedido = documento_cedido.read()
                infomacion_final.save()
                messages.success(
                    request,
                    "El documento final con cesión de derechos se ha cargado/actualizado correctamente.",
                )
                return redirect("estudiante:avances_proyecto")
            else:
                messages.error(
                    request,
                    "No se encontró la información final para actualizar el documento.",
                )
                return redirect("estudiante:avances_proyecto")
        else:
            messages.error(request, "Por favor, sube un archivo válido.")
            return redirect("estudiante:avances_proyecto")
    else:
        messages.info(request, "No se realizaron cambios en el documento.")
        return redirect("estudiante:avances_proyecto")


@login_required
@grupo_usuario("Estudiantes")
def avances_proyecto(request):
    context = datosusuario(request)
    proyecto_final = recuperar_proyecto_final_usuario(request.user)
    retroalimentaciones = recuperar_retroalimentacion_proyecto_final(proyecto_final)
    informacion_proyecto_final = (
        ModelInformacionEntregaFinal.objects.get(proyecto_final=proyecto_final)
        if ModelInformacionEntregaFinal.objects.filter(
            proyecto_final=proyecto_final
        ).exists()
        else None
    )
    if informacion_proyecto_final:
        context["informacion_proyecto_final"] = informacion_proyecto_final
        doc_final_cedido = devolver_documento_imagen(
            informacion_proyecto_final.doc_proyecto_final_cedido
        )
        if doc_final_cedido:
            context["doc_proyecto_final_cedido"] = doc_final_cedido
    print(retroalimentaciones)
    if retroalimentaciones:
        dict_retroalimentaciones = {}
        for i, retroalimentacion in enumerate(retroalimentaciones):
            dict_retroalimentaciones[f"retroalimentacion_{i}"] = {
                "retroalimentacion": retroalimentacion,
                "doc_retro": devolver_documento_imagen(
                    retroalimentacion.doc_retroalimentacion
                ),
            }
        context["retroalimentaciones"] = dict_retroalimentaciones
    if proyecto_final:
        doc_proyecto_final = proyecto_final.proyecto_final
        doc_carta_final = proyecto_final.carta_presentacion_final
        context["docs_finales"] = {
            "proyecto_final": devolver_documento_imagen(doc_proyecto_final),
            "carta_final": devolver_documento_imagen(doc_carta_final),
        }

        fechas = ModelFechasProyecto.objects.get(proyecto_final=proyecto_final)
        if fechas:
            context["fecha_culminacion_anteproyecto"] = fecha_culminacion_anteproyecto(
                fechas.fecha_inicio
            )

            context["fecha_actual"] = fecha_actual()
            context["fechas"] = fechas
            context["fecha_actual"] = datetime.strptime(
                context["fecha_actual"], "%Y-%m-%d %H:%M:%S"
            ).date()

            print(context["fecha_actual"])
            print(fechas.fecha_etapa_dos)
        if proyecto_final:
            context["proyecto_final"] = proyecto_final

        obj_general = recuperar_objetivo_general(proyecto_final)
        porcentaje = 0
        if obj_general:
            context["obj_general"] = obj_general
            objs_especificos = recuperar_objetivos_especificos(obj_general)

            if objs_especificos:

                context["objs_especificos"] = objs_especificos
                num_especificos = objs_especificos.count()
                num_especificos_aprobados = 0
                dict_actividades = {}
                dict_docs_avances = {}
                actividades_hechas = 0
                num_actividades = 0
                for i, obj_especifico in enumerate(objs_especificos):
                    dict_docs_avances[f"doc_avance_{i}"] = devolver_documento_imagen(
                        obj_especifico.documento_avance
                    )
                    if obj_especifico.estado:
                        num_especificos_aprobados += 1
                    actividades = recuperar_actividades(obj_especifico)
                    if actividades:
                        num_actividades += actividades.count()
                    # print(actividades, "actividades")
                    if actividades:
                        for actividad in actividades:
                            if actividad.estado == True:
                                actividades_hechas += 1

                        dict_actividades[f"actividades_obj_especifico_{i}"] = (
                            actividades
                        )
                if num_especificos == num_especificos_aprobados:
                    messages.success(
                        request,
                        "Todos los objetivos específicos han sido aprobados por el director. Ahora puede cargar la carta de presentación final y el documento del proyecto final.",
                    )
                    context["puede_enviar"] = True
                else:
                    messages.warning(
                        request,
                        "Aún tiene actividades pendientes para cumplir. Por favor, esté atento a las observaciones del director.",
                    )
                if num_actividades != 0:
                    porcentaje = (actividades_hechas / num_actividades) * 100
                # print(actividades_hechas)
                # print(num_actividades)
                # print(porcentaje)

                context["porcentaje"] = int(porcentaje)
                context["actividades"] = dict_actividades
                context["docs_avances"] = dict_docs_avances

    return render(request, "estudiante/avances_proyecto.html", context)


@login_required
@grupo_usuario("Estudiantes")
def cargar_docs_final(request, id_proyecto):
    proyecto = recuperar_proyecto_final_id(id_proyecto)

    if proyecto:
        if request.method == "POST":
            doc_carta_final = request.FILES.get("cartaPresentacion_final")
            if doc_carta_final:
                if doc_carta_final.content_type == "application/pdf":
                    proyecto.carta_presentacion_final = doc_carta_final.read()
                    messages.success(
                        request, "Carta de presentación final cargada correctamente."
                    )
                else:
                    messages.error(
                        request,
                        "El archivo de la carta de presentación debe ser un PDF.",
                    )
                    return redirect("estudiante:avances_proyecto")
            else:
                messages.warning(
                    request, "No se ha cargado ninguna carta de presentación final."
                )

            doc_proyecto_final = request.FILES.get("documentoProyecto_final")
            if doc_proyecto_final:
                if doc_proyecto_final.content_type == "application/pdf":
                    proyecto.proyecto_final = doc_proyecto_final.read()
                    messages.success(request, "Proyecto final cargado correctamente.")
                else:
                    messages.error(request, "El archivo del proyecto debe ser un PDF.")
                    return redirect("estudiante:avances_proyecto")
            else:
                messages.warning(request, "No se ha cargado ningún proyecto final.")

            proyecto.save()
            return redirect("estudiante:avances_proyecto")

    else:
        messages.error(request, "No se encontró el proyecto con el ID proporcionado.")
        return redirect("estudiante:avances_proyecto")


@login_required
@grupo_usuario("Estudiantes")
def modificar_docs_final(request, id_proyecto):
    proyecto = recuperar_proyecto_final_id(id_proyecto)

    if proyecto:
        # Mensaje de éxito si se encuentra el proyecto
        messages.success(request, "Proyecto encontrado correctamente.")

        # Verifica si se ha subido la carta de presentación final
        doc_carta_final = request.FILES.get("carta_final")
        if doc_carta_final:
            proyecto.carta_presentacion_final = doc_carta_final.read()
            messages.success(
                request, "Carta de presentación final actualizada correctamente."
            )
        else:
            messages.warning(
                request, "No se ha cargado ninguna carta de presentación final."
            )

        # Verifica si se ha subido el proyecto final
        doc_proyecto_final = request.FILES.get("proyecto_final")
        if doc_proyecto_final:
            proyecto.proyecto_final = doc_proyecto_final.read()
            messages.success(request, "Proyecto final actualizado correctamente.")
        else:
            messages.warning(request, "No se ha cargado ningún proyecto final.")

        # Guarda el proyecto con los archivos actualizados
        proyecto.save()

        # Redirige a la página de avances con mensaje de éxito
        return redirect("estudiante:avances_proyecto")
    else:
        # Mensaje de error si no se encuentra el proyecto
        messages.error(request, "No se encontró el proyecto con el ID proporcionado.")
        return redirect("estudiante:avances_proyecto")


@login_required
@grupo_usuario("Estudiantes")
def subir_objetivo_general(request, id):
    if request.method == "POST":
        objetivo_general = ModelObjetivoGeneral(
            proyecto_final=recuperar_proyecto_final_id(id),
            descripcion=request.POST.get("descripcion_objetivo_general"),
        )
        objetivo_general.save()
        messages.success(request, "Objetivo general agregado exitosamente.")
        return redirect("estudiante:avances_proyecto")
    else:

        messages.error(
            request, "Error al agregar el objetivo general. Intente nuevamente."
        )
        return redirect("estudiante:avances_proyecto")


@login_required
@grupo_usuario("Estudiantes")
def editar_objetivo_general(request, id):
    objetivo_general = ModelObjetivoGeneral.objects.filter(id=id).first()
    if objetivo_general:
        edit_objetivo = request.POST.get("editar_objetivo_general")

        if edit_objetivo:
            objetivo_general.descripcion = edit_objetivo
            objetivo_general.save()
            messages.success(
                request, "El objetivo general ha sido actualizado correctamente."
            )
        else:
            messages.warning(
                request,
                "No se ha proporcionado ninguna descripción para el objetivo general.",
            )
    else:
        messages.error(request, "No se ha encontrado el objetivo general especificado.")

    return redirect("estudiante:avances_proyecto")


@login_required
@grupo_usuario("Estudiantes")
def eliminar_objetivo_general(request, id):

    objetivo_general = ModelObjetivoGeneral.objects.filter(id=id).first()
    if objetivo_general:
        objetivo_general.delete()
        messages.success(
            request, "El objetivo general ha sido eliminado correctamente."
        )
    else:
        messages.error(request, "No se ha encontrado el objetivo general especificado.")

    return redirect("estudiante:avances_proyecto")


@login_required
@grupo_usuario("Estudiantes")
def subir_objetivo_especifico(request, id):
    if request.method == "POST":
        proyecto_final = recuperar_proyecto_final_id(id)
        objetivo_especifico = ModelObjetivosEspecificos(
            objetivo_general=recuperar_objetivo_general(proyecto_final),
            descripcion=request.POST.get("descripcion"),
        )
        objetivo_especifico.save()
        # Mensaje de éxito
        messages.success(request, "Objetivo específico agregado exitosamente.")
        return redirect("estudiante:avances_proyecto")
    else:
        # Mensaje de error
        messages.error(
            request, "Error al agregar el objetivo específico. Intente nuevamente."
        )
        return redirect("estudiante:avances_proyecto")


@login_required
@grupo_usuario("Estudiantes")
def editar_objetivo_especifico(request, id):
    objetivo_especifico = ModelObjetivosEspecificos.objects.filter(id=id).first()
    if objetivo_especifico:
        edit_objetivo = request.POST.get("editar_objetivo_especifico")

        if edit_objetivo:
            objetivo_especifico.descripcion = edit_objetivo
            objetivo_especifico.save()
            messages.success(
                request, "El objetivo general ha sido actualizado correctamente."
            )
        else:
            messages.warning(
                request,
                "No se ha proporcionado ninguna descripción para el objetivo general.",
            )
    else:
        messages.error(request, "No se ha encontrado el objetivo general especificado.")

    return redirect("estudiante:avances_proyecto")


@login_required
@grupo_usuario("Estudiantes")
def eliminar_objetivo_especifico(request, id):

    objetivo_especifico = ModelObjetivosEspecificos.objects.filter(id=id).first()
    if objetivo_especifico:
        objetivo_especifico.delete()
        messages.success(
            request, "El objetivo general ha sido eliminado correctamente."
        )
    else:
        messages.error(request, "No se ha encontrado el objetivo general especificado.")

    return redirect("estudiante:avances_proyecto")


@login_required
@grupo_usuario("Estudiantes")
def editar_eliminar_archivo(request, id):
    # Obtener el objetivo específico correspondiente
    objetivo_especifico = ModelObjetivosEspecificos.objects.get(id=id)

    if objetivo_especifico:
        # Acción de eliminar
        if request.POST.get("accion") == "eliminar":
            objetivo_especifico.documento_avance = None
            objetivo_especifico.fecha_envio = None
            objetivo_especifico.save()
            messages.success(request, "El documento ha sido eliminado exitosamente.")

        # Acción de editar
        elif request.POST.get("accion") == "editar":
            nuevo_archivo = request.FILES.get("archivo_nuevo")
            if nuevo_archivo:
                objetivo_especifico.fecha_envio = fecha_actual()
                objetivo_especifico.documento_avance = nuevo_archivo.read()
                objetivo_especifico.save()
                messages.success(
                    request, "El documento ha sido actualizado correctamente."
                )
            else:
                messages.error(
                    request,
                    "No se ha seleccionado ningún archivo. Por favor, seleccione un archivo válido para actualizar.",
                )

        # Redirigir tras la operación
        return redirect("estudiante:avances_proyecto")

    else:
        # En caso de que no se encuentre el objetivo específico
        messages.error(
            request, "El objetivo específico no ha sido encontrado. Intente nuevamente."
        )
        return redirect("estudiante:avances_proyecto")


@login_required
@grupo_usuario("Estudiantes")
def subir_actividad(request, id_proyecto, id_esp):
    if request.method == "POST":
        proyecto_final = recuperar_proyecto_final_id(id_proyecto)
        actividad = ModelActividades(
            objetivo_general=recuperar_objetivo_general(proyecto_final),
            objetivos_especificos=recuperar_objetivo_especifico(id_esp),
            descripcion=request.POST.get("descripcion"),
        )
        actividad.save()
        # Mensaje de éxito
        messages.success(request, "Actividad agregada exitosamente.")
        return redirect("estudiante:avances_proyecto")
    else:
        # Mensaje de error
        messages.error(request, "Error al agregar la actividad. Intente nuevamente.")
        return redirect("estudiante:avances_proyecto")


@login_required
@grupo_usuario("Estudiantes")
def editar_actividad(request, id):
    actividad = ModelActividades.objects.filter(id=id).first()

    if actividad:
        edit_actividad = request.POST.get("editar_actividad")

        if edit_actividad:
            actividad.descripcion = edit_actividad
            actividad.save()
            messages.success(request, "La actividad ha sido actualizada correctamente.")
        else:
            messages.warning(
                request, "No se ha proporcionado ninguna descripción para la actividad."
            )
    else:
        messages.error(request, "No se ha encontrado la actividad especificada.")

    return redirect("estudiante:avances_proyecto")


@login_required
@grupo_usuario("Estudiantes")
def eliminar_actividad(request, id):
    actividad = ModelActividades.objects.filter(id=id).first()

    if actividad:
        actividad.delete()
        messages.success(request, "La actividad ha sido eliminada correctamente.")
    else:
        messages.error(request, "No se ha encontrado la actividad especificada.")

    return redirect("estudiante:avances_proyecto")


@login_required
@grupo_usuario("Estudiantes")
def subir_avance(request, id_esp):

    obj_esp = recuperar_objetivo_especifico(id_esp)

    if obj_esp:
        documento_avance = request.FILES.get("documento_avance")

        if documento_avance:
            obj_esp.fecha_envio = fecha_actual()
            obj_esp.documento_avance = documento_avance.read()
            obj_esp.save()
            messages.success(
                request,
                f'El avance del objetivo "{obj_esp.descripcion}" ha sido subido correctamente.',
            )
        else:
            messages.error(request, "No se ha seleccionado ningún archivo para subir.")
    else:
        messages.error(
            request, "El objetivo específico que intentas actualizar no existe."
        )

    return redirect("estudiante:avances_proyecto")


#####################################################################################################################################
# formatos del comite


@login_required
@grupo_usuario("Estudiantes")
def formatos_documentos(request):
    context = datosusuario(request)
    context["formatos"] = recuperar_formatos()

    return render(request, "estudiante/formatos.html", context)


#####################################################################################################################################
