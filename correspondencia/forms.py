from django import forms
from .models import (
    ModelRetroalimentaciones,
    ModelSolicitudes,
    ModelAsignacionJurados,
    ModelDocumentos,
)


class FormRetroalimentacionAnteproyecto(forms.ModelForm):
    doc_retroalimentacion_convert = forms.FileField(
        required=True,
        widget=forms.ClearableFileInput(
            attrs={
                "class": "form-control",
                "id": "doc_retroalimentacion_convert",
                "accept": "application/pdf",
                "name": "doc_retroalimentacion_convert",
            }
        ),
    )

    class Meta:
        model = ModelRetroalimentaciones
        fields = ("retroalimentacion", "doc_retroalimentacion_convert", "estado")

        widgets = {
            "retroalimentacion": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Escribe la retroalimentación del anteproyecto...",
                    "rows": 4,
                }
            ),
            "estado": forms.Select(
                attrs={
                    "class": "form-select",
                    "id": "estado_select",
                }
            ),
        }

    def save(self, commit=True):
        retroalimentacion = super().save(commit=False)
        retroalimentacion.retroalimentacion = self.cleaned_data["retroalimentacion"]
        retroalimentacion.doc_retroalimentacion = self.cleaned_data[
            "doc_retroalimentacion_convert"
        ].read()
        estado = self.cleaned_data["estado"]
        if estado == False:
            solcitud = ModelSolicitudes.objects
        retroalimentacion.estado = self.cleaned_data["estado"]
        if commit:
            retroalimentacion.save()
        return retroalimentacion


class FormObservacionAnteproyecto(forms.ModelForm):
    doc_retroalimentacion_convert = forms.FileField(
        required=True,
        widget=forms.ClearableFileInput(
            attrs={
                "class": "custom-file-input",  # Clase CSS para el estilo
                "id": "doc_retroalimentacion_convert",  # ID específico
                "accept": "application/pdf",  # Aceptar solo PDF
            }
        ),
    )

    class Meta:
        model = ModelRetroalimentaciones
        fields = (
            "retroalimentacion",
            "doc_retroalimentacion_convert",
        )

    def save(self, commit=True):
        retroalimentacion = super().save(commit=False)
        retroalimentacion.retroalimentacion = self.cleaned_data["retroalimentacion"]
        retroalimentacion.doc_retroalimentacion = self.cleaned_data[
            "doc_retroalimentacion_convert"
        ].read()

        if commit:
            retroalimentacion.save()
        return retroalimentacion


class FormRetroalimentacionProyecto(forms.ModelForm):
    doc_retroalimentacion_convert = forms.FileField(
        required=True,
        widget=forms.ClearableFileInput(
            attrs={
                "class": "form-control",
                "placeholder": "Subir documento de retroalimentación",
            }
        ),
    )

    class Meta:
        model = ModelRetroalimentaciones
        fields = ("retroalimentacion", "doc_retroalimentacion_convert", "estado")

        widgets = {
            "retroalimentacion": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Escribe la retroalimentación...",
                    "rows": 4,
                }
            ),
            "estado": forms.CheckboxSelectMultiple(
                attrs={
                    "class": "form-check-input",
                    "id": "element_estado",
                }
            ),
        }

    def save(self, commit=True):
        retroalimentacion = super().save(commit=False)
        retroalimentacion.retroalimentacion = self.cleaned_data["retroalimentacion"]
        retroalimentacion.doc_retroalimentacion = self.cleaned_data[
            "doc_retroalimentacion_convert"
        ].read()
        retroalimentacion.estado = self.cleaned_data["estado"]
        if commit:
            retroalimentacion.save()
        return retroalimentacion


class FormObservacionProyecto(forms.ModelForm):
    doc_retroalimentacion_convert = forms.FileField(required=True)

    class Meta:
        model = ModelRetroalimentaciones
        fields = (
            "retroalimentacion",
            "doc_retroalimentacion_convert",
        )

        estado = forms.ChoiceField(
            widget=forms.CheckboxSelectMultiple(attrs={"id": "element_estado"})
        )

    def save(self, commit=True):
        retroalimentacion = super().save(commit=False)
        retroalimentacion.retroalimentacion = self.cleaned_data["retroalimentacion"]
        retroalimentacion.doc_retroalimentacion = self.cleaned_data[
            "doc_retroalimentacion_convert"
        ].read()

        if commit:
            retroalimentacion.save()
        return retroalimentacion


class FormSolicitudes(forms.ModelForm):
    documento_soporte_convert = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={"class": "form-control", "accept": ".pdf"}),
    )

    class Meta:
        model = ModelSolicitudes
        fields = [
            "tipo_solicitud",
            "motivo_solicitud",
            "documento_soporte_convert",
        ]
        widgets = {
            "tipo_solicitud": forms.Select(attrs={"class": "form-control"}),
            "motivo_solicitud": forms.Textarea(
                attrs={"class": "form-control", "rows": 4}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(FormSolicitudes, self).__init__(*args, **kwargs)
        self.fields["motivo_solicitud"].required = True
        self.fields["documento_soporte_convert"].required = True

    def clean_documento_soporte_convert(self):
        documento = self.cleaned_data.get("documento_soporte_convert")

        # Validar el tipo MIME del archivo
        if documento:
            if not documento.content_type == "application/pdf":
                raise ValidationError("Solo se permiten archivos en formato PDF.")

        return documento

    def save(self, commit=False):
        solicitudes = super().save(commit=True)
        solicitudes.tipo_solicitud = self.cleaned_data["tipo_solicitud"]
        solicitudes.motivo_solicitud = self.cleaned_data["motivo_solicitud"]
        solicitudes.documento_soporte = self.cleaned_data[
            "documento_soporte_convert"
        ].read()
        if commit:
            solicitudes.save()
        return solicitudes


# formulario de asignacion de jurados


class FormJurados(forms.ModelForm):
    nombre_jurado = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = ModelAsignacionJurados
        fields = [
            "nombre_jurado",
        ]

    def save(self, commit=False):
        jurados = super().save(commit=True)
        if commit:
            jurados.save()
        return jurados


# formulario del cargue de documentos


class FormDocumentos(forms.ModelForm):
    documento_convert = forms.FileField(
        required=False, widget=forms.FileInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = ModelDocumentos
        fields = ["nombre_documento", "descripcion", "version", "documento_convert"]
        widgets = {
            "nombre_documento": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "version": forms.TextInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super(FormDocumentos, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["documento_convert"].required = False

    def save(self, commit=True):
        documentos = super().save(commit=False)
        if self.cleaned_data["documento_convert"]:
            documentos.documento = self.cleaned_data["documento_convert"].read()
        if commit:
            documentos.save()
        return documentos
