from django import forms
from django.core.exceptions import ValidationError
from .models import ServerType, Server, User, Service, Application, ResourceUsage


class ServerTypeForm(forms.ModelForm):
    class Meta:
        model  = ServerType
        fields = ['type', 'description']


class ServerForm(forms.ModelForm):
    class Meta:
        model  = Server
        fields = ['name', 'server_type', 'cpu_count', 'memory_capacity_gb', 'storage_capacity_gb']


class UserForm(forms.ModelForm):
    class Meta:
        model  = User
        fields = ['last_name', 'first_name', 'email']


class ApplicationForm(forms.ModelForm):
    class Meta:
        model  = Application
        fields = ['name', 'logo', 'user']


class ServiceForm(forms.ModelForm):
    class Meta:
        model  = Service
        fields = ['name', 'launch_date', 'used_memory_gb', 'required_ram_gb', 'launch_server']
        widgets = {'launch_date': forms.DateInput(attrs={'type': 'date'})}

    def clean(self):
        cleaned = super().clean()
        server  = cleaned.get('launch_server')
        used    = cleaned.get('used_memory_gb')
        ram     = cleaned.get('required_ram_gb')

        if server and used is not None and ram is not None:
            # exclure l'instance en cours de modification
            used_deja = sum(
                s.used_memory_gb for s in server.services.all()
                if self.instance.pk is None or s.pk != self.instance.pk
            )
            libre = server.memory_capacity_gb - used_deja

            if used > libre:
                raise ValidationError(f"Mémoire insuffisante : {libre:.1f} Go libres, {used} Go demandés.")
            if ram > libre:
                raise ValidationError(f"RAM insuffisante : {libre:.1f} Go libres, {ram} Go requis.")

        return cleaned


class ResourceUsageForm(forms.ModelForm):
    class Meta:
        model  = ResourceUsage
        fields = ['application', 'service']


class JSONImportForm(forms.Form):
    json_file = forms.FileField(label='Fichier JSON (.json)')

    def clean_json_file(self):
        f = self.cleaned_data['json_file']
        if not f.name.endswith('.json'):
            raise ValidationError("Le fichier doit avoir l'extension .json")
        return f
