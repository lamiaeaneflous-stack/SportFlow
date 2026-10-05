from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from datetime import datetime, timedelta

from .models import (
    Club,
    Terrain,
    Reservation,
    Equipement,
    ProjetSportif,
    Demande
)


def home(request):
    return render(request, 'core/homa.html')


def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('dashboard')

        return render(
            request,
            'core/login.html',
            {
                'error': 'Nom utilisateur ou mot de passe incorrect.'
            }
        )

    return render(request, 'core/login.html')


def inscription(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:

            return render(
                request,
                'core/inscription.html',
                {
                    'error': 'Les mots de passe ne correspondent pas.'
                }
            )

        if User.objects.filter(username=username).exists():

            return render(
                request,
                'core/inscription.html',
                {
                    'error': 'Ce nom utilisateur existe déjà.'
                }
            )

        if User.objects.filter(email=email).exists():

            return render(
                request,
                'core/inscription.html',
                {
                    'error': 'Cet email existe déjà.'
                }
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)

        return redirect('dashboard')

    return render(request, 'core/inscription.html')


def dashboard(request):

    if not request.user.is_authenticated:
        return redirect('login')

    return render(
        request,
        'core/dashboard.html'
    )


def logout_view(request):

    logout(request)

    return redirect('homa')


def clubs(request):

    clubs = Club.objects.all()

    return render(
        request,
        'core/clubs.html',
        {
            'clubs': clubs
        }
    )


def terrains(request):

    terrains = Terrain.objects.all()

    return render(
        request,
        'core/terrains.html',
        {
            'terrains': terrains
        }
    )


def reserver_terrain(request, terrain_id):

    if not request.user.is_authenticated:
        return redirect('login')

    terrain = Terrain.objects.get(id=terrain_id)

    if not terrain.disponible:
        return render(
            request,
            'core/reserver.html',
            {
                'terrain': terrain,
                'error': 'Ce terrain est indisponible.'
            }
        )

    if request.method == 'POST':

        date = request.POST.get('date')
        heure_debut = request.POST.get('heure_debut')
        duree = request.POST.get('duree')

        if not date or not heure_debut or not duree:

            return render(
                request,
                'core/reserver.html',
                {
                    'terrain': terrain,
                    'error': 'Veuillez remplir tous les champs.'
                }
            )

        duree = int(duree)

        debut = datetime.strptime(
            heure_debut,
            '%H:%M'
        )

        fin = debut + timedelta(hours=duree)

        heure_fin = fin.time()

        reservations = Reservation.objects.filter(
            terrain=terrain,
            date=date
        )

        for reservation in reservations:

            if reservation.heure_fin is None:
                continue

            ancienne_debut = reservation.heure_debut
            ancienne_fin = reservation.heure_fin

            nouvelle_debut = debut.time()
            nouvelle_fin = heure_fin

            if (
                nouvelle_debut < ancienne_fin
                and nouvelle_fin > ancienne_debut
            ):

                return render(
                    request,
                    'core/reserver.html',
                    {
                        'terrain': terrain,
                        'error': 'Ce créneau est déjà réservé.'
                    }
                )

        Reservation.objects.create(
            utilisateur=request.user,
            terrain=terrain,
            date=date,
            heure_debut=debut.time(),
            heure_fin=heure_fin,
            statut='En attente'
        )

        return redirect('reservations')

    return render(
        request,
        'core/reserver.html',
        {
            'terrain': terrain
        }
    )

def reservations(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.is_staff:
        reservations = Reservation.objects.all().order_by(
            '-date',
            '-heure_debut'
        )
    else:
        reservations = Reservation.objects.filter(
            utilisateur=request.user
        ).order_by(
            '-date',
            '-heure_debut'
        )

    return render(
        request,
        'core/reservations.html',
        {
            'reservations': reservations
        }
    )


def equipements(request):

    equipements = Equipement.objects.all()

    return render(
        request,
        'core/equipements.html',
        {
            'equipements': equipements
        }
    )


def projets(request):

    projets = ProjetSportif.objects.all()

    return render(
        request,
        'core/projets.html',
        {
            'projets': projets
        }
    )


def demandes(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.is_staff:
        demandes = Demande.objects.all().order_by(
            '-date_creation'
        )
    else:
        demandes = Demande.objects.filter(
            utilisateur=request.user
        ).order_by(
            '-date_creation'
        )

    return render(
        request,
        'core/demandes.html',
        {
            'demandes': demandes
        }
    )


def statistiques(request):

    nombre_clubs = Club.objects.count()
    nombre_terrains = Terrain.objects.count()
    nombre_equipements = Equipement.objects.count()
    nombre_projets = ProjetSportif.objects.count()

    context = {
        'nombre_clubs': nombre_clubs,
        'nombre_terrains': nombre_terrains,
        'nombre_equipements': nombre_equipements,
        'nombre_projets': nombre_projets,
    }

    return render(
        request,
        'core/statistiques.html',
        context
    )


def services(request):

    return render(
        request,
        'core/services.html'
    )
def accepter_demande(request, demande_id):

    if not request.user.is_authenticated:
        return redirect('login')

    if not request.user.is_staff:
        return redirect('demandes')

    demande = Demande.objects.get(id=demande_id)

    demande.statut = "Acceptée"
    demande.save()

    return redirect('demandes')


def refuser_demande(request, demande_id):

    if not request.user.is_authenticated:
        return redirect('login')

    if not request.user.is_staff:
        return redirect('demandes')

    demande = Demande.objects.get(id=demande_id)

    demande.statut = "Refusée"
    demande.save()

    return redirect('demandes')
def accepter_reservation(request, reservation_id):

    if not request.user.is_authenticated:
        return redirect('login')

    if not request.user.is_staff:
        return redirect('reservations')

    reservation = Reservation.objects.get(id=reservation_id)

    reservation.statut = "Acceptée"
    reservation.save()

    return redirect('reservations')


def refuser_reservation(request, reservation_id):

    if not request.user.is_authenticated:
        return redirect('login')

    if not request.user.is_staff:
        return redirect('reservations')

    reservation = Reservation.objects.get(id=reservation_id)

    reservation.statut = "Refusée"
    reservation.save()

    return redirect('reservations')