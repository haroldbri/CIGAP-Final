import os
import resend

from estudiante.models import ModelFechasProyecto, ModelProyectoFinal


resend.api_key = os.environ.get("RESEND_KEY")


def correo_anteproyecto_aprobado(usuario, retroalimentacion):

    anteproyecto = retroalimentacion.anteproyecto
    proyecto_final = (
        ModelProyectoFinal.objects.get(anteproyecto=anteproyecto)
        if ModelProyectoFinal.objects.filter(anteproyecto=anteproyecto).exists()
        else None
    )
    fechas_proyecto = (
        ModelFechasProyecto.objects.get(proyecto_final=proyecto_final)
        if ModelFechasProyecto.objects.filter(proyecto_final=proyecto_final).exists()
        else None
    )
    params: resend.Emails.SendParams = {
        "from": "Acme <onboarding@resend.dev>",
        "to": "plataformacigapubate@outlook.com",
        "subject": "Anteproyecto Aprobado",
        "html": f"""
    <div
    style="font-family: 'Saira', sans-serif; border-radius: 10px; padding: 20px; background-color: #002412; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1); max-width: 600px; margin: 0 auto;">
    <div style="background: #ffffff; border-radius: 12px;">
        <header
            style="width: 100%; display: flex; background: #ffffff; padding: 0; border-radius: 10px 10px 0 0; align-items: center; justify-content: center;">
        </header>
        <h1
            style="width: 100%; background-color: #002412; margin: 0; padding: 12px 0; text-align: center; color: #ffffff; margin-bottom: 20px;">
            Recordatorio de Entrega de Proyecto
        </h1>
        <h2 style="color: #000000; padding: 0 12px;">Estimado/a <span style="font-weight: bold;">{usuario.nombre_completo}</span>
        </h2>
        <p style="padding: 0 12px; color: #666666;">
            Nos complace informarle que su solicitud de anteproyecto para el proyecto
            <strong>{anteproyecto.nombre_anteproyecto}</strong> ha sido <strong>aprobada.</strong>
        </p>
        <p style="padding: 0 12px; color: #666666;">
            A continuación, se presenta un recordatorio de las fechas importantes para la entrega de su proyecto final
            en la plataforma CIGAP:
        </p>
        <ul style="padding: 0 12px; color: #666666; list-style-type: none;">
            <li style="margin-bottom: 10px;">
                <strong>Fecha de aprobación del Anteproyecto:</strong> {retroalimentacion.fecha_retroalimentacion}
            </li>
            
            <li style="margin-bottom: 10px;">
                <strong>Etapa 1:</strong> {fechas_proyecto.fecha_etapa_uno}
            </li>
            <li style="margin-bottom: 10px;">
                <strong>Etapa 2:</strong> {fechas_proyecto.fecha_etapa_dos}
            </li>
            <li style="margin-bottom: 10px;">
                <strong>Etapa 3:</strong> {fechas_proyecto.fecha_etapa_tres}
            </li>
            <li style="margin-bottom: 10px;">
                <strong>Etapa 4:</strong> {fechas_proyecto.fecha_etapa_cuatro}
            </li>
            <li style="margin-bottom: 10px;">
                <strong>Etapa 5:</strong> {fechas_proyecto.fecha_etapa_cinco}
            </li>
            <li style="margin-bottom: 10px;">
                <strong>Etapa 6:</strong> {fechas_proyecto.fecha_etapa_seis}
            </li>
        </ul>
        <p style="padding: 0 12px; color: #666666;">
            Recuerde que la fecha de inicio se establece una vez aprobado el anteproyecto.
        </p>
        <p style="padding: 0 12px; color: #666666;">
            Le recomendamos avanzar en el desarrollo de su proyecto para garantizar su entrega dentro de la fecha
            estimada de finalización.
        </p>
        <p style="padding: 0 12px; color: #666666;">
            <strong>Dispone de 6 meses para ello.</strong>
        </p>
        <h3 style="padding: 0 12px; color: #000000;">Estamos a su disposición para apoyarle en cada etapa del proceso.
        </h3>
        <div style="width: 100%; background: #3C3C3B; padding: 0; border-radius: 0 0 10px 10px;">
            <div style="padding: 8px;">
                <h2 style="color: #fff; margin-bottom: 5px; font-weight: 600; text-align: center;">Notificación
                    automática de la plataforma CIGAP</h2>
                <p style="color: #fff; margin-top: 5px; text-align: center; font-size: 12px;">Por favor, no responda a
                    este correo.</p>
            </div>
        </div>
    </div>
</div>
    """,
    }
    email = resend.Emails.send(params)
    print(email)


def correo_anteproyecto_rechazado(usuario, retroalimentacion):
    anteproyecto = retroalimentacion.anteproyecto

    params: resend.Emails.SendParams = {
        "from": "Acme <onboarding@resend.dev>",
        # activado el dominio se ajusta a f{usuario.email}
        "to": "plataformacigapubate@outlook.com",
        "subject": "Anteproyecto Rechazado",
        "html": f"""
    <div
    style="font-family: 'Saira', sans-serif; border-radius: 10px; padding: 20px; background-color: #002412; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1); max-width: 600px; margin: 0 auto;">
    <div style="background: #ffffff; border-radius: 12px;">
        <header
            style="width: 100%; display: flex; background: #ffffff; padding: 0; border-radius: 10px 10px 0 0; align-items: center; justify-content: center;">
        </header>
        <h1
            style="width: 100%; background-color: #c0392b; margin: 0; padding: 12px 0; text-align: center; color: #ffffff; margin-bottom: 20px;">
            Notificación de Anteproyecto No Aprobado
        </h1>
        <h2 style="color: #000000; padding: 0 12px;">Estimado/a <span style="font-weight: bold;">{usuario.nombre_completo}</span>
        </h2>
        <p style="padding: 0 12px; color: #666666;">
            Lamentamos informarle que su solicitud de anteproyecto para el proyecto
            <strong>{anteproyecto.nombre_anteproyecto}</strong> ha sido <strong>no aprobada.</strong></br>
        </p>
        <p><strong>Retroalimentación: </strong> {retroalimentacion.retroalimentacion}</p>
        <p style="padding: 0 12px; color: #666666;">
            Para avanzar en el proceso, le solicitamos que cargue otra solicitud de anteproyecto a través de la plataforma CIGAP.
        </p>
       <ul>
            <li style="margin-bottom: 10px;">
                <strong>Cargar nueva solicitud:</strong> Acceda a la plataforma y presente un nuevo anteproyecto para su revisión.
            </li>
            <li style="margin-bottom: 10px;">
                <strong>Plazo para nuevas solicitudes:</strong> Recuerde que tiene un plazo de 30 días para presentar su nueva propuesta.
            </li>
        </ul>
        <p style="padding: 0 12px; color: #666666;">
            Si necesita asistencia o tiene preguntas, no dude en comunicarse con nuestro equipo de soporte.
        </p>
        <h3 style="padding: 0 12px; color: #000000;">Estamos aquí para ayudarle en el proceso.</h3>
        <div style="width: 100%; background: #3C3C3B; padding: 0; border-radius: 0 0 10px 10px;">
            <div style="padding: 8px;">
                <h2 style="color: #fff; margin-bottom: 5px; font-weight: 600; text-align: center;">Notificación
                    automática de la plataforma CIGAP</h2>
                <p style="color: #fff; margin-top: 5px; text-align: center; font-size: 12px;">Por favor, no responda a
                    este correo.</p>
            </div>
        </div>
    </div>
</div>

    """,
    }
    email = resend.Emails.send(params)
    print(email)


def correo_proyecto_aprobado(proyecto, txtretroalimentacion):

    params: resend.Emails.SendParams = {
        "from": "Acme <onboarding@resend.dev>",
        # activado el dominio se ajusta a f{proyecto.user.email}
        "to": "plataformacigapubate@outlook.com",
        "subject": "Proyecto Final Aprobado",
        "html": f"""
    <div
    style="font-family: 'Saira', sans-serif; border-radius: 10px; padding: 20px; background-color: #002412; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1); max-width: 600px; margin: 0 auto;">
    <div style="background: #ffffff; border-radius: 12px;">
        <header
            style="width: 100%; display: flex; background: #ffffff; padding: 0; border-radius: 10px 10px 0 0; align-items: center; justify-content: center;">
        </header>
        <h1
            style="width: 100%; background-color: #002412; margin: 0; padding: 12px 0; text-align: center; color: #ffffff; margin-bottom: 20px;">
            Felicitaciones por la Aprobación de su Proyecto Final
        </h1>
        <h2 style="color: #000000; padding: 0 12px;">Estimado/a <span style="font-weight: bold;">{proyecto.user.nombre_completo}</span>
        </h2>
        
        <p style="padding: 0 12px; color: #666666;">
            Retroalimentación: <strong>{txtretroalimentacion}</strong>.
        </p>
        <p style="padding: 0 12px; color: #666666;">
            Nos complace felicitarle por la aprobación de su proyecto final para el proyecto <strong>{proyecto.anteproyecto.nombre_anteproyecto}</strong>.
        </p>
        <p style="padding: 0 12px; color: #666666;">
            Este es un logro significativo que refleja su dedicación y esfuerzo a lo largo del desarrollo del proyecto. Como siguiente paso, le invitamos a cargar el <strong>documento final</strong> del proyecto en la plataforma CIGAP, en el apartado correspondiente de <strong>Proyecto Final</strong>.
        </p>
        <p style="padding: 0 12px; color: #666666;">
            Además, le recordamos que es necesario completar la sección de <strong>Derechos</strong> en este mismo apartado. Asegúrese de que todos los detalles estén correctamente registrados para concluir exitosamente el proceso de entrega.
        </p>
        <p style="padding: 0 12px; color: #666666;">
            Le recordamos cargar de estos documentos en el menor tiempo posible</strong>. ¡No dude en contactarnos si necesita asistencia en cualquier etapa!
        </p>
        <h3 style="padding: 0 12px; color: #000000;">Estamos aquí para acompañarle en este último paso. ¡Felicitaciones nuevamente!</h3>
        <div style="width: 100%; background: #3C3C3B; padding: 0; border-radius: 0 0 10px 10px;">
            <div style="padding: 8px;">
                <h2 style="color: #fff; margin-bottom: 5px; font-weight: 600; text-align: center;">Notificación automática de la plataforma CIGAP</h2>
                <p style="color: #fff; margin-top: 5px; text-align: center; font-size: 12px;">Por favor, no responda a este correo.</p>
            </div>
        </div>
    </div>
</div>


    """,
    }
    email = resend.Emails.send(params)
    print(email)


def correo_proyecto_rechazado(proyecto, txtretroalimentacion):
    params: resend.Emails.SendParams = {
        "from": "Acme <onboarding@resend.dev>",
        # activado el dominio se ajusta a f{proyecto.user.email}
        "to": "plataformacigapubate@outlook.com",
        "subject": "Proyecto Final Rechazado",
        "html": f"""
<div
    style="font-family: 'Saira', sans-serif; border-radius: 10px; padding: 20px; background-color: #002412; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1); max-width: 600px; margin: 0 auto;">
    <div style="background: #ffffff; border-radius: 12px;">
        <header
            style="width: 100%; display: flex; background: #ffffff; padding: 0; border-radius: 10px 10px 0 0; align-items: center; justify-content: center;">
        </header>
        <h1
            style="width: 100%; background-color: #c0392b; margin: 0; padding: 12px 0; text-align: center; color: #ffffff; margin-bottom: 20px;">
            Notificación de Rechazo de Proyecto Final
        </h1>
        <h2 style="color: #000000; padding: 0 12px;">Estimado/a <span style="font-weight: bold;">{proyecto.user.nombre_completo}</span>
        </h2>
        
        <p style="padding: 0 12px; color: #666666;">
            Lamentamos informarle que su proyecto final para el proyecto <strong>{proyecto.anteproyecto.nombre_anteproyecto}</strong> ha sido <strong>rechazado.</strong>
        </p>
        <p style="padding: 0 12px; color: #666666;">
            Retroalimentación: <strong>{txtretroalimentacion}</strong>.
        </p>
        <p style="padding: 0 12px; color: #666666;">
            Apreciamos el esfuerzo que ha puesto en el desarrollo de su proyecto. Para poder avanzar, le solicitamos que revise los comentarios proporcionados y realice las correcciones necesarias.
        </p>
        <p style="padding: 0 12px; color: #666666;">
            Una vez que haya realizado las modificaciones, le invitamos a cargar una nueva versión del proyecto en la plataforma CIGAP, en el apartado correspondiente de <strong>Proyecto Final</strong>.
        </p>
        <p style="padding: 0 12px; color: #666666;">
            Le recomendamos que preste especial atención a los detalles mencionados en la retroalimentación para asegurar que su nueva presentación cumpla con los requisitos establecidos.
        </p>
        <h3 style="padding: 0 12px; color: #000000;">Estamos aquí para ayudarle en este proceso. No dude en contactarnos si necesita asistencia adicional.</h3>
        <div style="width: 100%; background: #3C3C3B; padding: 0; border-radius: 0 0 10px 10px;">
            <div style="padding: 8px;">
                <h2 style="color: #fff; margin-bottom: 5px; font-weight: 600; text-align: center;">Notificación automática de la plataforma CIGAP</h2>
                <p style="color: #fff; margin-top: 5px; text-align: center; font-size: 12px;">Por favor, no responda a este correo.</p>
            </div>
        </div>
    </div>
</div>
    """,
    }
    email = resend.Emails.send(params)
    print(email)
    pass


# correo_anteproyecto_aprobado()
# correo_anteproyecto_rechazado()
# correo_proyecto_aprobado()
# correo_proyecto_rechazado()
