from django.db import models


class ServerType(models.Model):
    type        = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['type']

    def __str__(self):
        return self.type


class Server(models.Model):
    name                 = models.CharField(max_length=150, unique=True)
    server_type          = models.ForeignKey(
                               ServerType,
                               on_delete=models.PROTECT,
                               related_name='servers'
                           )
    cpu_count            = models.PositiveIntegerField()
    memory_capacity_gb   = models.FloatField()
    storage_capacity_gb  = models.FloatField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def used_memory_gb(self):
        return sum(s.used_memory_gb for s in self.services.all())

    def free_memory_gb(self):
        return self.memory_capacity_gb - self.used_memory_gb()

    def memory_utilization_pct(self):
        if self.memory_capacity_gb == 0:
            return 0
        return round((self.used_memory_gb() / self.memory_capacity_gb) * 100, 2)


class User(models.Model):
    last_name  = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    email      = models.EmailField(unique=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Service(models.Model):
    name            = models.CharField(max_length=150, unique=True)
    launch_date     = models.DateField()
    used_memory_gb  = models.FloatField()
    required_ram_gb = models.FloatField()
    launch_server   = models.ForeignKey(
                          Server,
                          on_delete=models.PROTECT,
                          related_name='services'
                      )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Application(models.Model):
    name = models.CharField(max_length=150, unique=True)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    user = models.ForeignKey(
               User,
               on_delete=models.PROTECT,
               related_name='applications'
           )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class ResourceUsage(models.Model):
    application = models.ForeignKey(
                      Application,
                      on_delete=models.CASCADE,
                      related_name='resource_usages'
                  )
    service     = models.ForeignKey(
                      Service,
                      on_delete=models.CASCADE,
                      related_name='resource_usages'
                  )

    class Meta:
        unique_together = [('application', 'service')]

    def __str__(self):
        return f"{self.application} -> {self.service}"
