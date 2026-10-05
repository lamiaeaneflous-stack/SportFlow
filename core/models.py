from django.db import models
from django.contrib.auth.models import User


class Club(models.Model):
    nom = models.CharField(max_length=100)
    sport = models.CharField(max_length=100)
    ville = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom


class Terrain(models.Model):
    nom = models.CharField(max_length=100)
    sport = models.CharField(max_length=100)
    ville = models.CharField(max_length=100)
    adresse = models.CharField(max_length=200)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.nom


class Reservation(models.Model):

    utilisateur = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    terrain = models.ForeignKey(
        Terrain,
        on_delete=models.CASCADE
    )

    date = models.DateField()

    heure_debut = models.TimeField()

    heure_fin = models.TimeField(default='00:00')

    statut = models.CharField(
        max_length=50,
        default="En attente"
    )

    def __str__(self):
        return f"{self.utilisateur.username} - {self.terrain.nom}"

class Equipement(models.Model):
    nom = models.CharField(max_length=100)
    categorie = models.CharField(max_length=100)
    quantite = models.IntegerField(default=1)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.nom


class ProjetSportif(models.Model):
    nom = models.CharField(max_length=150)
    sport = models.CharField(max_length=100)
    description = models.TextField()
    date_debut = models.DateField()
    date_fin = models.DateField()

    def __str__(self):
        return self.nom


class Demande(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    sujet = models.CharField(max_length=150)
    description = models.TextField()
    statut = models.CharField(max_length=50, default="En attente")
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sujet