"""
Password hashing utilities using bcrypt
"""
import bcrypt
from typing import Optional


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt with salt.
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password as string (bcrypt format)
    """
    if not password:
        raise ValueError("Password cannot be empty")
    
    # Generate salt and hash password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(password: str, password_hash: str) -> bool:
    """
    Verify a password against its hash.
    
    Args:
        password: Plain text password to verify
        password_hash: Stored password hash
        
    Returns:
        True if password matches, False otherwise
    """
    if not password or not password_hash:
        return False
    
    try:
        return bcrypt.checkpw(
            password.encode('utf-8'),
            password_hash.encode('utf-8')
        )
    except (ValueError, TypeError):
        # Invalid hash format
        return False


def validate_password_strength(password: str) -> tuple[bool, Optional[str]]:
    """
    Validate password strength.
    
    Requirements:
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    
    Args:
        password: Password to validate
        
    Returns:
        (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter"
    
    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter"
    
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one digit"
    
    return True, None

