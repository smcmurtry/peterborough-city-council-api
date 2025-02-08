from .votes import votes_bp
from .councillors import councillors_bp
from .meetings import meetings_bp
from .base import base_bp

# Export the blueprints directly
__all__ = ['councillors_bp', 'votes_bp', 'meetings_bp', 'base_bp']
