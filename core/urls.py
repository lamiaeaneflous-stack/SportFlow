from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='homa'),

    path('login/', views.login_view, name='login'),
    path('inscription/', views.inscription, name='inscription'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),

    path('clubs/', views.clubs, name='clubs'),
    path('terrains/', views.terrains, name='terrains'),

    path(
        'reserver/<int:terrain_id>/',
        views.reserver_terrain,
        name='reserver_terrain'
    ),

    path('reservations/', views.reservations, name='reservations'),

    path(
        'reservation/<int:reservation_id>/accepter/',
        views.accepter_reservation,
        name='accepter_reservation'
    ),

    path(
        'reservation/<int:reservation_id>/refuser/',
        views.refuser_reservation,
        name='refuser_reservation'
    ),

    path('equipements/', views.equipements, name='equipements'),
    path('projets/', views.projets, name='projets'),
    path('demandes/', views.demandes, name='demandes'),

    path(
        'demande/<int:demande_id>/accepter/',
        views.accepter_demande,
        name='accepter_demande'
    ),

    path(
        'demande/<int:demande_id>/refuser/',
        views.refuser_demande,
        name='refuser_demande'
    ),

    path('statistiques/', views.statistiques, name='statistiques'),
    path('services/', views.services, name='services'),
]