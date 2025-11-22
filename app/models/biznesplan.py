"""
Biznesplan Model

Stores generated business plans.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from config.database import Base


class Biznesplan(Base):
    """
    Generated business plan document.
    
    Stores final Markdown output and generation metadata.
    """
    __tablename__ = "biznesplans"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign Key to Order
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    
    # Content
    content_markdown = Column(Text, nullable=True)  # Final biznesplan in Markdown format
    
    # Generation Status
    status = Column(String(50), nullable=False, default="draft")  # draft / in_review / approved / rejected
    
    # Iteration Tracking
    iterations = Column(Integer, default=0)  # Number of refinement iterations performed
    current_section_index = Column(Integer, default=0)  # Current section being generated (0-based)
    total_sections = Column(Integer, default=9)  # Total number of sections (outline, 8 sections, finalize)
    
    # LLM API Tracking
    generator_logs = Column(JSON, nullable=True)
    """
    Logs from Generator agent:
    {
        "api_calls": 10,
        "total_input_tokens": 50000,
        "total_output_tokens": 25000,
        "cached_tokens": 40000,
        "total_cost_usd": 0.25,
        "sections": [
            {
                "name": "Pismo przewodnie",
                "input_tokens": 5000,
                "output_tokens": 2000,
                "cost_usd": 0.02,
                "duration_seconds": 15
            }
        ]
    }
    """
    
    reviewer_logs = Column(JSON, nullable=True)
    """
    Logs from Reviewer agent:
    {
        "api_calls": 3,
        "total_input_tokens": 30000,
        "total_output_tokens": 1000,
        "total_cost_usd": 0.05,
        "reviews": [
            {
                "iteration": 1,
                "overall_score": 0.85,
                "issues": [],
                "approved": true,
                "feedback": "High quality, meets all criteria"
            }
        ]
    }
    """
    
    # Quality Metrics
    final_word_count = Column(Integer, nullable=True)
    final_page_count = Column(Integer, nullable=True)  # Estimated A4 pages
    final_quality_score = Column(Integer, nullable=True)  # 0-100 from Reviewer
    
    # Issues & Feedback
    final_issues = Column(JSON, nullable=True)  # List of unresolved issues (if any)
    """
    [
        {
            "section": "SWOT",
            "issue": "Brak źródeł dla niektórych zagrożeń",
            "severity": "minor"
        }
    ]
    """
    
    # Cost Tracking
    total_cost_usd = Column(Integer, nullable=True)  # Total cost in cents (USD)
    cache_hit_rate = Column(Integer, nullable=True)  # Percentage (0-100)
    
    # Generation Duration
    generation_started_at = Column(DateTime(timezone=True), nullable=True)
    generation_completed_at = Column(DateTime(timezone=True), nullable=True)
    generation_duration_seconds = Column(Integer, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    
    # Relationship
    order = relationship("Order", back_populates="biznesplan")
    
    def __repr__(self):
        return f"<Biznesplan(order_id={self.order_id}, status={self.status}, iterations={self.iterations})>"
    
    @property
    def total_cost_usd_formatted(self) -> str:
        """Format cost as USD string"""
        if self.total_cost_usd is None:
            return "$0.00"
        return f"${self.total_cost_usd / 100:.2f}"

