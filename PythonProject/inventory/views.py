import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction

from .models import TypeServeur, Serveur, Utilisateur, Service, Application, UsageRessource
from .forms import TypeServeurForm, ServeurForm, UtilisateurForm, ServiceForm, ApplicationForm, UsageRessourceForm, JSONImportForm


# ── Accueil ───────────────────────────────────────────────────────────────────

def home(request):
    return render(request, 'inventory/home.html', {
        'server_count':      Serveur.objects.count(),
        'service_count':     Service.objects.count(),
        'application_count': Application.objects.count(),
        'user_count':        Utilisateur.objects.count(),
    })


# ── TypeServeur ───────────────────────────────────────────────────────────────

def servertype_list(request):
    return render(request, 'inventory/servertype/list.html', {'servertypes': TypeServeur.objects.all()})

def servertype_create(request):
    form = TypeServeurForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Type créé.")
        return redirect('inventory:servertype-list')
    return render(request, 'inventory/servertype/form.html', {'form': form, 'title': 'Nouveau type de serveur'})

def servertype_update(request, pk):
    obj = get_object_or_404(TypeServeur, pk=pk)
    form = TypeServeurForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, "Type modifié.")
        return redirect('inventory:servertype-list')
    return render(request, 'inventory/servertype/form.html', {'form': form, 'title': f'Modifier {obj}'})

def servertype_delete(request, pk):
    obj = get_object_or_404(TypeServeur, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, "Type supprimé.")
        return redirect('inventory:servertype-list')
    return render(request, 'inventory/servertype/confirm_delete.html', {'object': obj})


# ── Serveur ───────────────────────────────────────────────────────────────────

def server_list(request):
    return render(request, 'inventory/server/list.html', {'servers': Serveur.objects.select_related('type_serveur').prefetch_related('services')})

def server_detail(request, pk):
    server = get_object_or_404(Serveur, pk=pk)
    return render(request, 'inventory/server/detail.html', {'server': server})

def server_create(request):
    form = ServeurForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Serveur créé.")
        return redirect('inventory:server-list')
    return render(request, 'inventory/server/form.html', {'form': form, 'title': 'Nouveau serveur'})

def server_update(request, pk):
    obj = get_object_or_404(Serveur, pk=pk)
    form = ServeurForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, "Serveur modifié.")
        return redirect('inventory:server-list')
    return render(request, 'inventory/server/form.html', {'form': form, 'title': f'Modifier {obj}'})

def server_delete(request, pk):
    obj = get_object_or_404(Serveur, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, "Serveur supprimé.")
        return redirect('inventory:server-list')
    return render(request, 'inventory/server/confirm_delete.html', {'object': obj})


# ── Utilisateur ───────────────────────────────────────────────────────────────

def user_list(request):
    return render(request, 'inventory/user/list.html', {'users': Utilisateur.objects.all()})

def user_create(request):
    form = UtilisateurForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Utilisateur créé.")
        return redirect('inventory:user-list')
    return render(request, 'inventory/user/form.html', {'form': form, 'title': 'Nouvel utilisateur'})

def user_update(request, pk):
    obj = get_object_or_404(Utilisateur, pk=pk)
    form = UtilisateurForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, "Utilisateur modifié.")
        return redirect('inventory:user-list')
    return render(request, 'inventory/user/form.html', {'form': form, 'title': f'Modifier {obj}'})

def user_delete(request, pk):
    obj = get_object_or_404(Utilisateur, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, "Utilisateur supprimé.")
        return redirect('inventory:user-list')
    return render(request, 'inventory/user/confirm_delete.html', {'object': obj})


# ── Service ───────────────────────────────────────────────────────────────────

def service_list(request):
    return render(request, 'inventory/service/list.html', {'services': Service.objects.select_related('serveur')})

def service_create(request):
    form = ServiceForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Service créé.")
        return redirect('inventory:service-list')
    return render(request, 'inventory/service/form.html', {'form': form, 'title': 'Nouveau service'})

def service_update(request, pk):
    obj = get_object_or_404(Service, pk=pk)
    form = ServiceForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, "Service modifié.")
        return redirect('inventory:service-list')
    return render(request, 'inventory/service/form.html', {'form': form, 'title': f'Modifier {obj}'})

def service_delete(request, pk):
    obj = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, "Service supprimé.")
        return redirect('inventory:service-list')
    return render(request, 'inventory/service/confirm_delete.html', {'object': obj})


# ── Application ───────────────────────────────────────────────────────────────

def application_list(request):
    return render(request, 'inventory/application/list.html', {'applications': Application.objects.select_related('utilisateur')})

def application_detail(request, pk):
    app = get_object_or_404(Application, pk=pk)
    return render(request, 'inventory/application/detail.html', {'application': app})

def application_create(request):
    form = ApplicationForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Application créée.")
        return redirect('inventory:application-list')
    return render(request, 'inventory/application/form.html', {'form': form, 'title': 'Nouvelle application'})

def application_update(request, pk):
    obj = get_object_or_404(Application, pk=pk)
    form = ApplicationForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, "Application modifiée.")
        return redirect('inventory:application-list')
    return render(request, 'inventory/application/form.html', {'form': form, 'title': f'Modifier {obj}'})

def application_delete(request, pk):
    obj = get_object_or_404(Application, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, "Application supprimée.")
        return redirect('inventory:application-list')
    return render(request, 'inventory/application/confirm_delete.html', {'object': obj})


# ── UsageRessource ────────────────────────────────────────────────────────────

def resourceusage_list(request):
    return render(request, 'inventory/resourceusage/list.html', {'usages': UsageRessource.objects.select_related('application', 'service__serveur')})

def resourceusage_create(request):
    form = UsageRessourceForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Lien créé.")
        return redirect('inventory:resourceusage-list')
    return render(request, 'inventory/resourceusage/form.html', {'form': form, 'title': 'Lier une application à un service'})

def resourceusage_delete(request, pk):
    obj = get_object_or_404(UsageRessource, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, "Lien supprimé.")
        return redirect('inventory:resourceusage-list')
    return render(request, 'inventory/resourceusage/confirm_delete.html', {'object': obj})


# ── Rapport ───────────────────────────────────────────────────────────────────

def report_index(request):
    pk = request.GET.get('server')
    if pk:
        return redirect('inventory:server-report', pk=pk)
    return render(request, 'inventory/report/server_report.html', {'servers': Serveur.objects.all()})

def server_report(request, pk):
    server   = get_object_or_404(Serveur, pk=pk)
    services = server.services.prefetch_related('usages_ressource__application')

    rows = []
    for svc in services:
        rows.append({
            'service':        svc,
            'used_memory_gb': svc.espace_memoire_utilise,
            'applications':   [ru.application for ru in svc.usages_ressource.all()],
        })

    return render(request, 'inventory/report/server_report.html', {
        'server':               server,
        'rows':                 rows,
        'total_used_memory_gb': round(server.used_memory_gb(), 2),
        'total_capacity_gb':    server.capacite_memoire,
        'utilization_pct':      server.memory_utilization_pct(),
        'free_memory_gb':       round(server.free_memory_gb(), 2),
        'servers':              Serveur.objects.all(),
    })


# ── Import JSON ───────────────────────────────────────────────────────────────

def json_import(request):
    form = JSONImportForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        try:
            data = json.load(form.cleaned_data['json_file'])
        except json.JSONDecodeError as e:
            messages.error(request, f"JSON invalide : {e}")
            return render(request, 'inventory/import/import_json.html', {'form': form})

        errors = _do_import(data)
        if errors:
            for e in errors:
                messages.error(request, e)
        else:
            messages.success(request, "Import réussi.")
            return redirect('inventory:application-list')

    return render(request, 'inventory/import/import_json.html', {'form': form})


def _do_import(data):
    errors = []

    user_data = data.get('user', {})
    if not user_data.get('email'):
        return ["user.email est obligatoire."]

    app_name = data.get('application_name')
    if not app_name:
        return ["application_name est obligatoire."]
    if Application.objects.filter(nom_application=app_name).exists():
        return [f"L'application '{app_name}' existe déjà."]

    try:
        with transaction.atomic():
            utilisateur, _ = Utilisateur.objects.get_or_create(
                email=user_data['email'],
                defaults={'prenom': user_data.get('first_name', ''), 'nom': user_data.get('last_name', '')}
            )
            app = Application.objects.create(nom_application=app_name, utilisateur=utilisateur)

            for i, svc_data in enumerate(data.get('services', [])):
                try:
                    serveur = Serveur.objects.get(nom=svc_data['launch_server'])
                except (Serveur.DoesNotExist, KeyError):
                    errors.append(f"Service {i} : serveur '{svc_data.get('launch_server')}' introuvable.")
                    continue

                utilise = svc_data.get('used_memory_gb', 0)
                ram     = svc_data.get('required_ram_gb', 0)
                libre   = serveur.free_memory_gb()

                if utilise > libre or ram > libre:
                    errors.append(f"Service {i} '{svc_data.get('name')}' : mémoire insuffisante sur {serveur.nom} ({libre} Go libres).")
                    continue

                try:
                    svc, _ = Service.objects.get_or_create(
                        nom_service=svc_data['name'],
                        defaults={
                            'date_lancement':          svc_data['launch_date'],
                            'espace_memoire_utilise':  utilise,
                            'memoire_vive_necessaire': ram,
                            'serveur':                 serveur,
                        }
                    )
                    UsageRessource.objects.get_or_create(application=app, service=svc)
                except KeyError as e:
                    errors.append(f"Service {i} : champ manquant {e}.")

            if errors:
                raise Exception("rollback")

    except Exception:
        pass

    return errors
