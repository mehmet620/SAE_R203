from django.db import models


class TypeServeur(models.Model):
    type        = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['type']
        db_table = 'type_serveur'

    def __str__(self):
        return self.type


class Serveur(models.Model):
    nom               = models.CharField(max_length=100, unique=True)
    type_serveur      = models.ForeignKey(
                            TypeServeur,
                            on_delete=models.PROTECT,
                            related_name='serveurs'
                        )
    nombre_processeur = models.PositiveIntegerField()
    capacite_memoire  = models.PositiveIntegerField()
    capacite_stockage = models.PositiveIntegerField()

    class Meta:
        ordering = ['nom']
        db_table = 'serveur'

    def __str__(self):
        return self.nom

    def used_memory_gb(self):
        return sum(s.espace_memoire_utilise for s in self.services.all())

    def free_memory_gb(self):
        return self.capacite_memoire - self.used_memory_gb()

    def memory_utilization_pct(self):
        if self.capacite_memoire == 0:
            return 0
        return round((self.used_memory_gb() / self.capacite_memoire) * 100, 2)


class Utilisateur(models.Model):
    nom    = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email  = models.EmailField(unique=True)

    class Meta:
        ordering = ['nom', 'prenom']
        db_table = 'utilisateur'

    def __str__(self):
        return f"{self.prenom} {self.nom}"


class Service(models.Model):
    nom_service             = models.CharField(max_length=100, unique=True)
    date_lancement          = models.DateField()
    espace_memoire_utilise  = models.PositiveIntegerField()
    memoire_vive_necessaire = models.PositiveIntegerField()
    serveur                 = models.ForeignKey(
                                  Serveur,
                                  on_delete=models.PROTECT,
                                  related_name='services'
                              )

    class Meta:
        ordering = ['nom_service']
        db_table = 'service'

    def __str__(self):
        return self.nom_service


class Application(models.Model):
    nom_application = models.CharField(max_length=100, unique=True)
    logo            = models.ImageField(upload_to='logos/', blank=True, null=True)
    utilisateur     = models.ForeignKey(
                          Utilisateur,
                          on_delete=models.PROTECT,
                          related_name='applications'
                      )

    class Meta:
        ordering = ['nom_application']
        db_table = 'application'

    def __str__(self):
        return self.nom_application


class UsageRessource(models.Model):
    application = models.ForeignKey(
                      Application,
                      on_delete=models.CASCADE,
                      related_name='usages_ressource'
                  )
    service     = models.ForeignKey(
                      Service,
                      on_delete=models.CASCADE,
                      related_name='usages_ressource'
                  )

    class Meta:
        unique_together = [('application', 'service')]
        db_table        = 'usage_ressource'

    def __str__(self):
        return f"{self.application} -> {self.service}"
