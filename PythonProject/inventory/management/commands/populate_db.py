from datetime import date
from django.core.management.base import BaseCommand
from inventory.models import ServerType, Server, User, Service, Application, ResourceUsage


class Command(BaseCommand):
    help = "Peuple la base de données avec des données d'exemple."

    def handle(self, *args, **options):
        self.stdout.write("Peuplement de la base de données...")

        # Server Types
        blade, _ = ServerType.objects.get_or_create(
            type='Blade', defaults={'description': 'Serveur lame haute densité'}
        )
        rack, _ = ServerType.objects.get_or_create(
            type='Rack', defaults={'description': 'Serveur monté en baie standard'}
        )
        tower, _ = ServerType.objects.get_or_create(
            type='Tower', defaults={'description': 'Serveur tour autonome'}
        )
        virtual, _ = ServerType.objects.get_or_create(
            type='Virtual', defaults={'description': 'Instance de serveur virtualisé'}
        )

        # Servers
        srv1, _ = Server.objects.get_or_create(
            name='srv-prod-01',
            defaults={
                'server_type': rack,
                'cpu_count': 32,
                'memory_capacity_gb': 256.0,
                'storage_capacity_gb': 4000.0,
            }
        )
        srv2, _ = Server.objects.get_or_create(
            name='srv-prod-02',
            defaults={
                'server_type': rack,
                'cpu_count': 16,
                'memory_capacity_gb': 128.0,
                'storage_capacity_gb': 2000.0,
            }
        )
        srv3, _ = Server.objects.get_or_create(
            name='srv-dev-01',
            defaults={
                'server_type': virtual,
                'cpu_count': 8,
                'memory_capacity_gb': 32.0,
                'storage_capacity_gb': 500.0,
            }
        )
        srv4, _ = Server.objects.get_or_create(
            name='srv-blade-01',
            defaults={
                'server_type': blade,
                'cpu_count': 64,
                'memory_capacity_gb': 512.0,
                'storage_capacity_gb': 8000.0,
            }
        )

        # Users
        u1, _ = User.objects.get_or_create(
            email='alice@example.com',
            defaults={'first_name': 'Alice', 'last_name': 'Dupont'}
        )
        u2, _ = User.objects.get_or_create(
            email='bob@example.com',
            defaults={'first_name': 'Bob', 'last_name': 'Martin'}
        )
        u3, _ = User.objects.get_or_create(
            email='carol@example.com',
            defaults={'first_name': 'Carol', 'last_name': 'Bernard'}
        )

        # Services
        svc1, _ = Service.objects.get_or_create(
            name='nginx',
            defaults={
                'launch_date': date(2023, 6, 1),
                'used_memory_gb': 2.0,
                'required_ram_gb': 4.0,
                'launch_server': srv1,
            }
        )
        svc2, _ = Service.objects.get_or_create(
            name='postgresql',
            defaults={
                'launch_date': date(2023, 6, 1),
                'used_memory_gb': 16.0,
                'required_ram_gb': 32.0,
                'launch_server': srv1,
            }
        )
        svc3, _ = Service.objects.get_or_create(
            name='redis',
            defaults={
                'launch_date': date(2023, 8, 15),
                'used_memory_gb': 4.0,
                'required_ram_gb': 8.0,
                'launch_server': srv2,
            }
        )
        svc4, _ = Service.objects.get_or_create(
            name='rabbitmq',
            defaults={
                'launch_date': date(2023, 9, 1),
                'used_memory_gb': 3.0,
                'required_ram_gb': 6.0,
                'launch_server': srv3,
            }
        )
        svc5, _ = Service.objects.get_or_create(
            name='elasticsearch',
            defaults={
                'launch_date': date(2024, 1, 10),
                'used_memory_gb': 30.0,
                'required_ram_gb': 64.0,
                'launch_server': srv4,
            }
        )

        # Applications
        app1, _ = Application.objects.get_or_create(
            name='WebFrontend', defaults={'user': u1}
        )
        app2, _ = Application.objects.get_or_create(
            name='DataPipeline', defaults={'user': u2}
        )
        app3, _ = Application.objects.get_or_create(
            name='SearchEngine', defaults={'user': u3}
        )

        # ResourceUsage links
        ResourceUsage.objects.get_or_create(application=app1, service=svc1)
        ResourceUsage.objects.get_or_create(application=app1, service=svc2)
        ResourceUsage.objects.get_or_create(application=app2, service=svc2)
        ResourceUsage.objects.get_or_create(application=app2, service=svc3)
        ResourceUsage.objects.get_or_create(application=app2, service=svc4)
        ResourceUsage.objects.get_or_create(application=app3, service=svc5)

        self.stdout.write(self.style.SUCCESS("Base de données peuplée avec succès."))
