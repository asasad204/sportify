import warnings

from backend.models import Korisnik
from backend.routers.auth import pwd_context
from .seeder import Seeder


def korisnici_seeder():
    class SeederKorisnici(Seeder):
        pass

    options = {
        'model': Korisnik,
        'id_field': 'id_korisnika',
    }

    # Supposed to supress deprecated warning, but it doesn't :/
    warnings.filterwarnings('ignore')
    default_user_password = pwd_context.hash('password')
    warnings.resetwarnings()
    
    data = [
        {
            'email': 'root@mail.com',
            'sifra': default_user_password,
            'korisnicko_ime': 'root',
            'id_uloge': 1
        },
        {
            'email': 'korisnik@mail.com',
            'sifra': default_user_password,
            'korisnicko_ime': 'korisnik',
            'id_uloge': 2
        },
        {
            'email': 'vlasnik@mail.com',
            'sifra': default_user_password,
            'korisnicko_ime': 'vlasnik',
            'id_uloge': 3
        },
        {
            'email': 'nejraalickovic@mail.com',
            'sifra': default_user_password,
            'korisnicko_ime': 'nejra',
            'id_uloge': 1
        },
        {
            'email': 'riadpap@mail.com',
            'sifra': default_user_password,
            'korisnicko_ime': 'riad',
            'id_uloge': 1
        },
        {
            'email': 'eminabesic@mail.com',
            'sifra': default_user_password,
            'korisnicko_ime': 'emina',
            'id_uloge': 1
        },
        {
            'email': 'djenetavelispahic@mail.com',
            'sifra': default_user_password,
            'korisnicko_ime': 'djeneta',
            'id_uloge': 1
        },
        {
            'email': 'matejpanic@mail.com',
            'sifra': default_user_password,
            'korisnicko_ime': 'matej',
            'id_uloge': 1
        }
    ]

    SeederKorisnici(options).seed(data)
