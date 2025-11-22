"""
Process Log Model

Stores detailed logs of biznesplan generation process for real-time tracking.
"""

from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from config.database import Base
import enum


class LogLevel(enum.Enum):
    """Log severity levels"""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class ProcessLog(Base):
    """
    Detailed process logs for real-time progress tracking.
    
    Used for SSE (Server-Sent Events) to show user what's happening during generation.
    """
    __tablename__ = "process_logs"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign Key to Order
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Log Details
    phase = Column(String(100), nullable=False)  # e.g., "fetching_ceidg", "generating_section_3", "reviewing"
    message = Column(String(500), nullable=False)  # Human-readable message
    level = Column(SQLEnum(LogLevel), nullable=False, default=LogLevel.INFO)
    
    # Additional Data
    data = Column(JSON, nullable=True)
    """
    Optional structured data:
    {
        "section_name": "Analiza SWOT",
        "section_index": 3,
        "tokens_used": 2500,
        "duration_seconds": 12,
        "cost_usd": 0.03
    }
    """
    
    # Progress
    progress_current = Column(Integer, nullable=True)  # Current step (e.g., 3)
    progress_total = Column(Integer, nullable=True)  # Total steps (e.g., 9)
    
    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    
    # Relationship
    order = relationship("Order", back_populates="process_logs")
    
    def __repr__(self):
        return f"<ProcessLog(order_id={self.order_id}, phase={self.phase}, level={self.level.value})>"
    
    @property
    def progress_percent(self) -> int:
        """Calculate progress percentage"""
        if self.progress_total and self.progress_current:
            return int((self.progress_current / self.progress_total) * 100)
        return 0

