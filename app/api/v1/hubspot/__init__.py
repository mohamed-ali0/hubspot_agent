"""
HubSpot API package - organized by object type
"""

from .contacts import bp as contacts_bp
from .companies import bp as companies_bp
from .deals import bp as deals_bp
from .notes import bp as notes_bp
from .tasks import bp as tasks_bp
from .activities import bp as activities_bp
from .associations import bp as associations_bp
from .leads import bp as leads_bp

__all__ = [
    'contacts_bp',
    'companies_bp', 
    'deals_bp',
    'notes_bp',
    'tasks_bp',
    'activities_bp',
    'associations_bp',
    'leads_bp'
]
