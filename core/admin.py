from django.contrib import admin
from .models import (
    Club,
    Terrain,
    Reservation,
    Equipement,
    ProjetSportif,
    Demande
)


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('nom', 'sport', 'ville', 'date_creation')
    search_fields = ('nom', 'sport', 'ville')


@admin.register(Terrain)
class TerrainAdmin(admin.ModelAdmin):
    list_display = ('nom', 'sport', 'ville', 'disponible')
    search_fields = ('nom', 'sport', 'ville')


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):

    list_display = (
        'utilisateur',
        'terrain',
        'date',
        'heure_debut',
        'heure_fin',
        'statut'
    )

    search_fields = (
        'utilisateur__username',
        'terrain__nom'
    )

@admin.register(Equipement)
class EquipementAdmin(admin.ModelAdmin):
    list_display = ('nom', 'categorie', 'quantite', 'disponible')
    search_fields = ('nom', 'categorie')


@admin.register(ProjetSportif)
class ProjetSportifAdmin(admin.ModelAdmin):
    list_display = ('nom', 'sport', 'date_debut', 'date_fin')
    search_fields = ('nom', 'sport')


@admin.register(Demande)
class DemandeAdmin(admin.ModelAdmin):
    list_display = ('sujet', 'utilisateur', 'statut', 'date_creation')
    search_fields = ('sujet', 'utilisateur__username')