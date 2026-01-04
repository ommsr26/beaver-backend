from sqlalchemy import Column, String, Boolean, DateTime, Integer, ForeignKey, Text, Numeric
from datetime import datetime
import uuid
from sqlalchemy import Float
from sqlalchemy.orm import relationship

from app.database.db import Base


class Account(Base):
    __tablename__ = "accounts"

    id = Column(String(255), primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(Text, nullable=True)  # NULL for backward compatibility, Text for bcrypt hashes
    email_verified = Column(Boolean, default=False, nullable=False)
    balance = Column(Numeric(10, 2), default=0.0, nullable=False)  # Use Numeric for precise decimal handling
    created_at = Column(DateTime(timezone=False), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=False), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    api_keys = relationship("APIKey", back_populates="account", cascade="all, delete-orphan")
    refresh_tokens = relationship("RefreshToken", back_populates="account", cascade="all, delete-orphan")

    @staticmethod
    def generate_id() -> str:
        return f"acc_{uuid.uuid4().hex}"


class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(String(255), primary_key=True, index=True)
    key = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    account_id = Column(String(255), ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False, index=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=False), default=datetime.utcnow, nullable=False)
    
    # Relationships
    account = relationship("Account", back_populates="api_keys")

    @staticmethod
    def generate_key() -> str:
        return f"beaver_{uuid.uuid4().hex}"


class UsageLog(Base):
    __tablename__ = "usage_logs"

    id = Column(String(255), primary_key=True, index=True)
    api_key_id = Column(String(255), index=True, nullable=True)
    account_id = Column(String(255), index=True, nullable=True)
    model_id = Column(String(255), index=True, nullable=True)
    provider = Column(String(50), nullable=True)
    input_tokens = Column(Integer, nullable=True)
    output_tokens = Column(Integer, nullable=True)
    total_cost = Column(Numeric(10, 6), nullable=True)  # Use Numeric for precise cost tracking
    created_at = Column(DateTime(timezone=False), default=datetime.utcnow, nullable=False)


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(String(255), primary_key=True, index=True)
    account_id = Column(String(255), ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False, index=True)
    amount = Column(Numeric(10, 2), nullable=False)  # Use Numeric for precise amounts
    transaction_type = Column(String(50), nullable=False)  # 'topup' or 'deduction'
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=False), default=datetime.utcnow, nullable=False)


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(String(255), primary_key=True, index=True)
    token = Column(Text, unique=True, index=True, nullable=False)  # Text for JWT tokens
    account_id = Column(String(255), ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False, index=True)
    is_revoked = Column(Boolean, default=False, nullable=False)
    expires_at = Column(DateTime(timezone=False), nullable=False)
    created_at = Column(DateTime(timezone=False), default=datetime.utcnow, nullable=False)
    
    # Relationships
    account = relationship("Account", back_populates="refresh_tokens")

    @staticmethod
    def generate_id() -> str:
        return f"rt_{uuid.uuid4().hex}"


class Model(Base):
    __tablename__ = "models"

    id = Column(String(255), primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)  # model_id like "gpt-4o"
    display_name = Column(String(255), nullable=False)  # Human-readable name
    provider = Column(String(50), nullable=False, index=True)  # openai, anthropic, google, etc.
    status = Column(String(20), default="active", nullable=False)  # active, inactive
    
    # Base prices (from provider, per 1M tokens)
    base_input_price = Column(Numeric(10, 4), nullable=False)  # Use Numeric for precise pricing
    base_output_price = Column(Numeric(10, 4), nullable=False)
    
    # Dynamic pricing (calculated by pricing engine)
    category = Column(String(50), index=True, nullable=True)  # ULTRA_BUDGET, BUDGET, MID_RANGE, PREMIUM, ULTRA_PREMIUM
    markup_percent = Column(Numeric(5, 2), nullable=True)  # Markup percentage applied
    beaver_ai_input_price = Column(Numeric(10, 4), nullable=True)  # Final price after markup
    beaver_ai_output_price = Column(Numeric(10, 4), nullable=True)  # Final price after markup
    
    # Metadata
    pricing_updated_at = Column(DateTime(timezone=False), nullable=True)
    created_at = Column(DateTime(timezone=False), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=False), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    @staticmethod
    def generate_id() -> str:
        return f"model_{uuid.uuid4().hex}"
