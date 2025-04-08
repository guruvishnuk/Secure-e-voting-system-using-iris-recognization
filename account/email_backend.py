from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from voting.models import Voter  # Import the Voter model to get the smartid

class EmailBackend(ModelBackend):
    def authenticate(self, request, smartid=None, **kwargs):
        """
        Authenticate a user using smartid.
        """
        if smartid:
            try:
                # Fetch the Voter using the smartid
                voter = Voter.objects.get(smartid=smartid)
                user = voter.admin  # Get the associated CustomUser (admin)
                return user  # Return the authenticated user
            except Voter.DoesNotExist:
                return None  # Return None if no voter is found for the given smartid
        return None  # If no smartid provided, return None for failed authentication
