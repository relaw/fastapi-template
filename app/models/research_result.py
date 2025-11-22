"""
Research Result Model

Stores market research data and SWOT analysis.
"""

from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from config.database import Base


class ResearchResult(Base):
    """
    Market research results and SWOT analysis.
    
    Stores data gathered from web search (Perplexity/Tavily) or AI analysis.
    """
    __tablename__ = "research_results"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign Key to Order
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    
    # Market Research Data
    market_data = Column(JSON, nullable=True)
    """
    Market research findings:
    {
        "industry_overview": "...",
        "market_size_poland": "...",
        "market_growth_rate": "...",
        "trends": ["...", "..."],
        "key_players": ["...", "..."]
    }
    """
    
    # SWOT Analysis
    swot_data = Column(JSON, nullable=True)
    """
    SWOT analysis:
    {
        "strengths": ["...", "..."],
        "weaknesses": ["...", "..."],
        "opportunities": ["...", "..."],
        "threats": ["...", "..."]
    }
    """
    
    # Sources & Citations
    sources = Column(JSON, nullable=True)
    """
    List of sources with citations:
    [
        {
            "title": "Report Title",
            "url": "https://...",
            "organization": "GUS / Statista / etc.",
            "year": 2024,
            "excerpt": "Relevant quote or data point",
            "used_for": "Market size estimate"
        }
    ]
    """
    
    # Research Metadata
    research_method = Column(String(50), nullable=True)  # "perplexity" / "tavily" / "mock" / "claude_web"
    research_queries = Column(JSON, nullable=True)  # List of queries executed
    research_duration_seconds = Column(Integer, nullable=True)  # Time taken to research
    
    # Quality Metrics
    source_count = Column(Integer, default=0)  # Number of sources cited
    source_quality_score = Column(Integer, nullable=True)  # 1-10 rating
    relevance_score = Column(Integer, nullable=True)  # 1-10 how relevant to business
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    researched_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    order = relationship("Order", back_populates="research_result")
    
    def __repr__(self):
        return f"<ResearchResult(order_id={self.order_id}, source_count={self.source_count})>"

