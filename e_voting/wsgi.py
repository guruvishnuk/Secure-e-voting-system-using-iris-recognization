"""
WSGI config for e_voting project.
"""

import os
import sys
from pathlib import Path

# Add project root directory to sys.path so Django can locate account, voting, administrator apps
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'e_voting.settings')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
app = application
