from django.db import models
from account.models import CustomUser
# Create your models here.
import uuid
from django.db import models
from django.core.mail import send_mail
from django.conf import settings


class Voter(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone = models.CharField(max_length=11, unique=True)  # Used for OTP
    otp = models.CharField(max_length=10, null=True)
    verified = models.BooleanField(default=False)
    voted = models.BooleanField(default=False)
    otp_sent = models.IntegerField(default=0)  # Control how many OTPs are sent
    aadhaar_card = models.CharField(max_length=12, unique=True)  # Aadhaar card number
    iris_image = models.ImageField(upload_to='iris_images/', null=True, blank=True)  # Upload directory
    smartid = models.CharField(max_length=8, unique=True, blank=True, null=True)  # New field for unique ID

    def save(self, *args, **kwargs):
        if not self.smartid:  # Only generate if smartid is not already set
            self.smartid = f"v{str(uuid.uuid4().int)[:7]}"  # Generate a unique smartid starting with 'v'

        # Send the smartid to the user's email after it's created
        if not self.pk:  # This checks if the object is being created (not updated)
            self.send_smartid_email()

        super(Voter, self).save(*args, **kwargs)

    def send_smartid_email(self):
        """
        Send the smartid to the user via email after the voter is created.
        """
        subject = 'Welcome to the Indian Election Commission Online Voting System'
        subject = 'Welcome to the Indian Election Commission Online Voting System'

        # Crafting the welcome message with the updated format
        message = f"Dear {self.admin.first_name},\n\n" \
                  f"Welcome to the Indian Election Commission Online Voting System!\n\n" \
                  f"Your unique SmartID for voting is: {self.smartid}\n\n" \
                  f"Best regards,\nE-Voting System"

        recipient_list = [self.admin.email]
        # Send email using Django's send_mail function
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)

    def __str__(self):
        return f"{self.admin.last_name}, {self.admin.first_name}"


class Position(models.Model):
    name = models.CharField(max_length=50, unique=True)
    max_vote = models.IntegerField()
    priority = models.IntegerField()

    def __str__(self):
        return self.name


class Candidate(models.Model):
    fullname = models.CharField(max_length=50)
    photo = models.ImageField(upload_to="candidates")
    bio = models.TextField()
    position = models.ForeignKey(Position, on_delete=models.CASCADE)

    def __str__(self):
        return self.fullname


class Votes(models.Model):
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
