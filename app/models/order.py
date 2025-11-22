"""
Order Model

Represents business plan orders from Podio.
"""

from sqlalchemy import Column, Integer, String, DateTime, JSON, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from config.database import Base
import enum


class OrderStatus(enum.Enum):
    """Order processing status"""
    PENDING = "pending"  # Order created, not started
    FETCHING_DATA = "fetching_data"  # Fetching CEIDG + research data
    GENERATING = "generating"  # AI generating biznesplan
    REVIEWING = "reviewing"  # Reviewer checking quality
    REFINING = "refining"  # Generator applying feedback
    COMPLETED = "completed"  # Biznesplan ready
    FAILED = "failed"  # Error occurred
    CANCELLED = "cancelled"  # User cancelled


class Order(Base):
    """
    Business plan order from Podio.
    
    Stores client information and tracks generation progress.
    """
    __tablename__ = "orders"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Podio Integration
    podio_item_id = Column(String(50), unique=True, nullable=False, index=True)
    podio_workspace_id = Column(String(50), nullable=True)
    podio_app_id = Column(String(50), nullable=True)
    
    # Client Data (from Podio form)
    nip = Column(String(10), nullable=False, index=True)  # Polish tax ID (10 digits)
    imie_nazwisko = Column(String(255), nullable=False)  # Full name
    email = Column(String(255), nullable=True)
    telefon = Column(String(20), nullable=True)
    
    # Business Information (from Podio)
    uslugi = Column(JSON, nullable=True)  # List of services offered (e.g., ["Software Development", "QA"])
    planowany_dochod_roczny = Column(Integer, nullable=True)  # Expected annual revenue (PLN)
    dodatkowe_informacje = Column(String, nullable=True)  # Additional notes from client
    
    # Processing Status
    status = Column(
        SQLEnum(OrderStatus),
        nullable=False,
        default=OrderStatus.PENDING,
        index=True
    )
    celery_task_id = Column(String(255), nullable=True, index=True)  # Celery task UUID
    
    # Progress Tracking
    current_phase = Column(String(100), nullable=True)  # e.g., "Generating section 3/9"
    progress_percent = Column(Integer, default=0)  # 0-100
    
    # Error Handling
    error_message = Column(String, nullable=True)
    retry_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    started_at = Column(DateTime(timezone=True), nullable=True)  # When generation started
    completed_at = Column(DateTime(timezone=True), nullable=True)  # When generation finished
    
    # Relationships
    ceidg_data = relationship("CEIDGData", back_populates="order", uselist=False, cascade="all, delete-orphan")
    research_result = relationship("ResearchResult", back_populates="order", uselist=False, cascade="all, delete-orphan")
    biznesplan = relationship("Biznesplan", back_populates="order", uselist=False, cascade="all, delete-orphan")
    process_logs = relationship("ProcessLog", back_populates="order", cascade="all, delete-orphan", order_by="ProcessLog.created_at")
    
    def __repr__(self):
        return f"<Order(id={self.id}, nip={self.nip}, status={self.status.value})>"

