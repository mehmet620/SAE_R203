from datetime import date
from django.core.management.base import BaseCommand
from inventory.models import TypeServeur, Serveur, Utilisateur, Service, Application, UsageRessource


class Command(BaseCommand):
    help = "Peuple la base de données avec des données d'exemple."

    def handle(self, *args, **options):
        self.stdout.write("Peuplement de la base de données...")

        # Types de serveur
        rack,    _ = TypeServeur.objects.get_or_create(type='Rack',    defaults={'description': 'Serveur monté en baie'})
        blade,   _ = TypeServeur.objects.get_or_create(type='Blade',   defaults={'description': 'Serveur lame haute densité'})
        tower,   _ = TypeServeur.objects.get_or_create(type='Tower',   defaults={'description': 'Serveur tour de bureau'})
        virtual, _ = TypeServeur.objects.get_or_create(type='Virtual', defaults={'description': 'Machine virtuelle'})

        # Serveurs Cisco
        srv1, _ = Serveur.objects.get_or_create(
            nom='Cisco-UCS-C220',
            defaults={'type_serveur': rack, 'nombre_processeur': 2, 'capacite_memoire': 64, 'capacite_stockage': 1000,
                      }
        )
        srv2, _ = Serveur.objects.get_or_create(
            nom='Cisco-UCS-C240',
            defaults={'type_serveur': rack, 'nombre_processeur': 4, 'capacite_memoire': 128, 'capacite_stockage': 2000,
                      }
        )
        srv3, _ = Serveur.objects.get_or_create(
            nom='Cisco-UCS-B200',
            defaults={'type_serveur': blade, 'nombre_processeur': 2, 'capacite_memoire': 32, 'capacite_stockage': 500,
                      }
        )
        srv4, _ = Serveur.objects.get_or_create(
            nom='Cisco-UCS-E160S',
            defaults={'type_serveur': virtual, 'nombre_processeur': 1, 'capacite_memoire': 16, 'capacite_stockage': 200,
                      }
        )

        # Utilisateurs
        u1, _ = Utilisateur.objects.get_or_create(email='mehmet.ozmen@iut.fr',      defaults={'prenom': 'Mehmet',     'nom': 'Ozmen'})
        u2, _ = Utilisateur.objects.get_or_create(email='leo.gasser@iut.fr',         defaults={'prenom': 'Leo',        'nom': 'Gasser'})
        u3, _ = Utilisateur.objects.get_or_create(email='alessandro.bauer@iut.fr',   defaults={'prenom': 'Alessandro', 'nom': 'Bauer'})
        u4, _ = Utilisateur.objects.get_or_create(email='sicari.bennoune@iut.fr',    defaults={'prenom': 'Sicari',     'nom': 'Bennoune'})
        u5, _ = Utilisateur.objects.get_or_create(email='adam.sebar@iut.fr',         defaults={'prenom': 'Adam',       'nom': 'Sebar'})

        # Services (connus du grand public)
        svc1, _ = Service.objects.get_or_create(
            nom_service='DNS',
            defaults={
                'date_lancement': date(2023, 9, 1),
                'espace_memoire_utilise': 2,
                'memoire_vive_necessaire': 4,
                'serveur': srv1,
            }
        )
        svc2, _ = Service.objects.get_or_create(
            nom_service='DHCP',
            defaults={
                'date_lancement': date(2023, 9, 1),
                'espace_memoire_utilise': 1,
                'memoire_vive_necessaire': 2,
                'serveur': srv1,
            }
        )
        svc3, _ = Service.objects.get_or_create(
            nom_service='Serveur Web (HTTP)',
            defaults={
                'date_lancement': date(2023, 10, 15),
                'espace_memoire_utilise': 8,
                'memoire_vive_necessaire': 16,
                'serveur': srv2,
            }
        )
        svc4, _ = Service.objects.get_or_create(
            nom_service='FTP',
            defaults={
                'date_lancement': date(2023, 11, 1),
                'espace_memoire_utilise': 4,
                'memoire_vive_necessaire': 8,
                'serveur': srv3,
            }
        )
        svc5, _ = Service.objects.get_or_create(
            nom_service='Messagerie (SMTP)',
            defaults={
                'date_lancement': date(2024, 1, 10),
                'espace_memoire_utilise': 6,
                'memoire_vive_necessaire': 12,
                'serveur': srv2,
            }
        )

        # Applications
        app1, _ = Application.objects.get_or_create(nom_application='Réseau local',       defaults={'utilisateur': u1})
        app2, _ = Application.objects.get_or_create(nom_application='Site de l\'école',   defaults={'utilisateur': u2})
        app3, _ = Application.objects.get_or_create(nom_application='Partage de fichiers', defaults={'utilisateur': u3})

        # Usages de ressources
        UsageRessource.objects.get_or_create(application=app1, service=svc1)   # Réseau local → DNS
        UsageRessource.objects.get_or_create(application=app1, service=svc2)   # Réseau local → DHCP
        UsageRessource.objects.get_or_create(application=app2, service=svc3)   # Site école → Web
        UsageRessource.objects.get_or_create(application=app2, service=svc5)   # Site école → Messagerie
        UsageRessource.objects.get_or_create(application=app3, service=svc4)   # Partage fichiers → FTP

        self.stdout.write(self.style.SUCCESS("Base de données peuplée avec succès."))
