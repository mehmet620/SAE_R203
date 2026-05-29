from django.contrib import admin
from .models import ServerType, Server, User, Service, Application, ResourceUsage


@admin.register(ServerType)
class ServerTypeAdmin(admin.ModelAdmin):
    list_display  = ['type', 'description']
    search_fields = ['type']


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display  = ['name', 'server_type', 'cpu_count', 'memory_capacity_gb', 'storage_capacity_gb']
    list_filter   = ['server_type']
    search_fields = ['name']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display  = ['last_name', 'first_name', 'email']
    search_fields = ['email', 'last_name', 'first_name']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display  = ['name', 'launch_server', 'used_memory_gb', 'required_ram_gb', 'launch_date']
    list_filter   = ['launch_server']
    search_fields = ['name']


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display  = ['name', 'user']
    search_fields = ['name']


@admin.register(ResourceUsage)
class ResourceUsageAdmin(admin.ModelAdmin):
    list_display  = ['application', 'service']
    list_filter   = ['application', 'service']
