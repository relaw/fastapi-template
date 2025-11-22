"""
CEIDG Data Model

Stores business data fetched from CEIDG API (Polish business registry).
"""

from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from config.database import Base


class CEIDGData(Base):
    """
    Business data from CEIDG (Centralna Ewidencja i Informacja o Działalności Gospodarczej).
    
    Cached data about the business entity registered in Polish business registry.
    """
    __tablename__ = "ceidg_data"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign Key to Order
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    
    # Business Identity
    nip = Column(String(10), nullable=False, index=True)
    regon = Column(String(14), nullable=True)
    nazwa_firmy = Column(String(500), nullable=False)  # Business name
    
    # Owner Information
    imie = Column(String(100), nullable=True)
    nazwisko = Column(String(100), nullable=True)
    
    # Address
    adres_ulica = Column(String(255), nullable=True)
    adres_numer_budynku = Column(String(20), nullable=True)
    adres_numer_lokalu = Column(String(20), nullable=True)
    adres_kod_pocztowy = Column(String(10), nullable=True)
    adres_miejscowosc = Column(String(255), nullable=True)
    adres_gmina = Column(String(255), nullable=True)
    adres_powiat = Column(String(255), nullable=True)
    adres_wojewodztwo = Column(String(255), nullable=True)
    
    # Business Activity
    pkd_glowny = Column(String(10), nullable=True)  # Main PKD code
    pkd_glowny_nazwa = Column(String(500), nullable=True)  # Main PKD name
    pkd_pozostale = Column(JSON, nullable=True)  # List of additional PKD codes and names
    
    # Dates
    data_rozpoczecia_dzialalnosci = Column(String(20), nullable=True)  # Start date (YYYY-MM-DD)
    data_zakonczenia_dzialalnosci = Column(String(20), nullable=True)  # End date if closed
    
    # Status
    status_wpisu = Column(String(50), nullable=True)  # Entry status (e.g., "Aktywny")
    
    # Raw Response (for debugging and future fields)
    raw_response = Column(JSON, nullable=True)  # Full JSON response from CEIDG API
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    fetched_at = Column(DateTime(timezone=True), server_default=func.now())  # When data was fetched from CEIDG
    
    # Relationship
    order = relationship("Order", back_populates="ceidg_data")
    
    def __repr__(self):
        return f"<CEIDGData(nip={self.nip}, nazwa_firmy={self.nazwa_firmy})>"
    
    @property
    def full_address(self) -> str:
        """Format full address as string"""
        parts = [
            self.adres_ulica,
            self.adres_numer_budynku,
            self.adres_numer_lokalu,
            self.adres_kod_pocztowy,
            self.adres_miejscowosc
        ]
        return ", ".join(filter(None, parts))

