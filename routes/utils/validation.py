from typing import Dict, Any, Optional
from flask import request
import re

def validate_product_data(data: Dict[str, Any]) -> Optional[str]:
    """Validate product form data."""
    required_fields = ['name', 'category', 'description']
    for field in required_fields:
        if not data.get(field):
            return f"Missing required field: {field}"
    return None

def validate_gallery_data(data: Dict[str, Any]) -> Optional[str]:
    """Validate gallery project form data."""
    required_fields = ['title', 'description', 'category', 'industry_served', 'size_category']
    for field in required_fields:
        if not data.get(field):
            return f"Missing required field: {field}"
    return None

def validate_testimonial_data(data: Dict[str, Any]) -> Optional[str]:
    """Validate testimonial form data."""
    if not data.get('client_name'):
        return "Client name is required"
    if not data.get('content'):
        return "Testimonial content is required"
    try:
        rating = int(data.get('rating', 0))
        if not 1 <= rating <= 5:
            return "Rating must be between 1 and 5"
    except ValueError:
        return "Invalid rating value"
    return None

def validate_email(email: str) -> bool:
    """Validate email format."""
    email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    return bool(email_pattern.match(email))

def validate_team_member_data(data):
    """Validate team member form data."""
    if not data.get('name'):
        return "Name is required"
    if not data.get('role'):
        return "Role is required"
    if not data.get('bio'):
        return "Biography is required"
    try:
        order = int(data.get('order', 0))
        if order < 0:
            return "Order must be a non-negative number"
    except ValueError:
        return "Invalid order value"
    return None