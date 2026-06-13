from sqlalchemy import Column, Integer, String, Float, JSON, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class ScanRecord(Base):
    """
    Stores the Risk Profile and intent distribution for each PHP file.
    Supports empirical comparison against traditional baselines[cite: 8].
    """
    __tablename__ = "scan_history"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    sha256 = Column(String, index=True) # To identify rapid mutation 
    
    # Core Metrics
    malicious_score = Column(Float)
    confidence = Column(Float)
    
    # Behavioral Taxonomy (Head B)
    # Stores the full probability distribution (RCE, Shell, etc.)
    risk_profile = Column(JSON) 
    
    # Decision Pipeline Metadata (RQ5)
    action_taken = Column(String) # BLOCK, DEFER, WARN
    uncertainty_status = Column(String)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())