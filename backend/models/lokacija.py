from sqlalchemy import Column, ForeignKey, Integer, Float, CheckConstraint, String, Text
from sqlalchemy.orm import relationship

from backend.database import Base


class Lokacija(Base):
    __tablename__ = "lokacije"

    id_lokacije = Column(Integer, primary_key=True, autoincrement=True)
    id_vlasnika = Column(Integer, ForeignKey("vlasnici.id_vlasnika"))
    id_adrese = Column(Integer, ForeignKey("adrese.id_adrese"))
    naziv_lokacije = Column(String)
    opis_lokacije = Column(String)
    recenzija = Column(Float, CheckConstraint("recenzija>=1 and recenzija<=5"))
    cijena_po_terminu = Column(Float, CheckConstraint("cijena_po_terminu>0 or cijena_po_terminu is null"), nullable=True)
    kapacitet = Column(Integer)
    longituda=Column(Float)
    latituda=Column(Float)
    naziv_terena=Column(String)
    opis_terena=Column(String)
    picture_data = Column(Text)
    vlasnici = relationship("Vlasnik", back_populates="lokacije")
    adrese = relationship("Adresa", back_populates="lokacije")
    sportovi = relationship("Veza_lokacija_sport", back_populates="lokacije")
    recenzija_terena = relationship("RecenzijaTerena", back_populates="tereni")
    slobodni_termini = relationship("Slobodni_Event", back_populates="lokacije")
    termini_u_pripremi = relationship("Event_u_pripremi", back_populates="lokacije")
    turnir = relationship("Turnir", back_populates="lokacije")
    meet_and_greet_eventi = relationship("MeetAndGreet", back_populates="lokacije")
    lost_and_found_eventi = relationship("LostAndFound", back_populates="lokacije")
