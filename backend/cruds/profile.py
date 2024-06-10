import hashlib

from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.models import Igrac, Vlasnik, Korisnik, RecenzijaIgraca, RecenzijaVlasnika
from backend.schemas import UserUpdateIgrac, UserUpdateVlasnik, RecenzijaIgracaSchema, RecenzijaVlasnikaSchema, \
    UploadPicture


def get_all_profiles(db: Session):
    all_profiles = {
        'svi_korisnici': get_igraci(db),
        'svi_vlasnici': get_vlasnici(db)
    }
    return all_profiles

def get_all_users(db: Session):
    all_users = {
        'svi_korisnici': get_igraci(db),
        'svi_vlasnici': get_vlasnici(db)
    }
    return all_users

def get_all_profiles_username(username: str, db: Session):
    all_profiles = {
        'svi_korisnici': get_igraci(db, {'username': username}),
        'svi_vlasnici': get_vlasnici(db, {'username': username})
    }
    return all_profiles


def get_igraci(db: Session, options: dict = None):
    igraci = db.query(Igrac).join(Korisnik)

    if options is not None:
        if 'id_igraca' in options:
            igraci = igraci.filter(Igrac.id_igraca == options['id_igraca'])
        if 'username' in options:
            igraci = igraci.filter(Korisnik.korisnicko_ime.like(options['username']))
        if 'first' in options:
            igraci = igraci.first()
        if 'limit' in options:
            igraci = igraci.limit(options['limit'])
    else:
        igraci = igraci.all()

    return igraci


def update_igrac(db: Session, igrac_info: UserUpdateIgrac, id_igraca: int):
    db.query(Igrac).filter(Igrac.id_igraca == id_igraca).update({
        Igrac.ime_igraca: igrac_info.ime_igraca,
        Igrac.srednje_ime: igrac_info.srednje_ime,
        Igrac.prezime_igraca: igrac_info.prezime_igraca,
        Igrac.datum_rodjenja: igrac_info.datum_rodjenja,
        Igrac.spol: igrac_info.spol,
        Igrac.tezina: igrac_info.tezina,
        Igrac.visina: igrac_info.visina,
        Igrac.max_dozvoljena_udaljenost: igrac_info.max_dozvoljena_udaljenost
    })
    db.commit()

    updated_igrac = db.query(Igrac).join(Korisnik).filter(Igrac.id_igraca == id_igraca).first()

    return updated_igrac


def rate_igrac(db: Session, rating: RecenzijaIgracaSchema, id_igraca: int):
    user_rating = RecenzijaIgraca(id_igraca=id_igraca, komentar=rating.komentar, ocjena=rating.ocjena)
    db.add(user_rating)
    db.commit()

    new_rating = db.query(func.avg(RecenzijaIgraca.ocjena)).filter(RecenzijaIgraca.id_igraca == id_igraca).all()
    db.query(Igrac).filter(Igrac.id_igraca == id_igraca).update({
        Igrac.recenzija: new_rating[0][0]
    })
    db.commit()

    rated_igrac = db.query(Igrac).join(Korisnik).filter(Igrac.id_igraca == id_igraca).first()

    return rated_igrac


def upload_picture_igrac(db: Session, img_data: UploadPicture):
    db.query(Igrac).filter(Igrac.id_igraca == img_data.id).update({
        Igrac.picture_data: img_data.picture_data,
        Igrac.picture_name: hashlib.md5(img_data.picture_name.encode('utf-8')).hexdigest()
    })
    db.commit()

    igrac = db.query(Igrac).join(Korisnik).filter(Igrac.id_igraca == img_data.id).first()

    return igrac


def get_vlasnici(db: Session, options: dict = None):
    vlasnici = db.query(Vlasnik).join(Korisnik)

    if options is not None:
        if 'id_vlasnika' in options:
            vlasnici = vlasnici.filter(Vlasnik.id_vlasnika == options['id_vlasnika'])
        if 'username' in options:
            vlasnici = vlasnici.filter(Korisnik.korisnicko_ime.like(options['username']))
        if 'first' in options:
            vlasnici = vlasnici.first()
        if 'limit' in options:
            vlasnici = vlasnici.limit(options['limit'])
    else:
        vlasnici = vlasnici.all()

    return vlasnici


def update_vlasnik(db: Session, vlasnik_info: UserUpdateVlasnik, id_vlasnika: int):
    db.query(Vlasnik).filter(Vlasnik.id_vlasnika == id_vlasnika).update({
        Vlasnik.ime_vlasnika: vlasnik_info.ime_vlasnika,
        Vlasnik.srednje_ime: vlasnik_info.srednje_ime,
        Vlasnik.prezime_vlasnika: vlasnik_info.prezime_vlasnika,
        Vlasnik.datum_rodjenja: vlasnik_info.datum_rodjenja,
        Vlasnik.spol: vlasnik_info.spol
    })
    db.commit()

    updated_vlasnik = db.query(Vlasnik).join(Korisnik).filter(Vlasnik.id_vlasnika == id_vlasnika).first()

    return updated_vlasnik


def rate_vlasnik(db: Session, rating: RecenzijaVlasnikaSchema, id_vlasnika: int):
    user_rating = RecenzijaVlasnika(id_vlasnika=id_vlasnika, komentar=rating.komentar, ocjena=rating.ocjena)
    db.add(user_rating)
    db.commit()

    new_rating = db.query(func.avg(RecenzijaVlasnika.ocjena)).filter(RecenzijaVlasnika.id_vlasnika == id_vlasnika).all()
    db.query(Vlasnik).filter(Vlasnik.id_vlasnika == id_vlasnika).update({
        Vlasnik.recenzija: new_rating[0][0]
    })
    db.commit()

    rated_vlasnik = db.query(Vlasnik).join(Korisnik).filter(Vlasnik.id_vlasnika == id_vlasnika).first()

    return rated_vlasnik


def upload_picture_vlasnik(db: Session, img_data: UploadPicture):
    db.query(Vlasnik).filter(Vlasnik.id_vlasnika == img_data.id).update({
        Vlasnik.picture_data: img_data.picture_data,
        Vlasnik.picture_name: hashlib.md5(img_data.picture_name.encode('utf-8')).hexdigest()
    })
    db.commit()

    vlasnik = db.query(Vlasnik).join(Korisnik).filter(Vlasnik.id_vlasnika == img_data.id).first()

    return vlasnik
