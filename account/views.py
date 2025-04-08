from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, reverse

from voting.models import Voter
from .email_backend import EmailBackend
from django.contrib import messages
from .forms import CustomUserForm
from voting.forms import VoterForm
from django.contrib.auth import login, logout
# Create your views here.
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login
# Import the Voter model
import cv2
import os
from django.conf import settings


def account_login(request):
    if request.user.is_authenticated:
        if request.user.user_type == '1':  # Admin user type
            return redirect(reverse("adminDashboard"))
        else:
            return redirect(reverse("voterDashboard"))  # Voter user type

    context = {}
    if request.method == 'POST':
        smartid = request.POST.get('smartid')
        # password = request.POST.get('password')
        iris_image = request.FILES.get('iris_image')  # Capture the uploaded Iris image if provided
        if not smartid or not iris_image:
            messages.error(request, "Both Smart ID and Iris Image are required.")
            return redirect("/")
        print(smartid)
        # Authenticate the user with email and password
        user = EmailBackend().authenticate(request, smartid=smartid)
        print(user)
        if user is not None:
            if user.user_type == '1':  # Admin user type
                login(request, user)
                return redirect(reverse("adminDashboard"))
            elif user.user_type == '2':  # Voter user type
                if iris_image:  # If an Iris image is provided, verify it
                    if verify_iris_image(iris_image, user):  # Replace this function with actual Iris verification logic
                        login(request, user)
                        return redirect(reverse("voterDashboard"))
                    else:
                        messages.error(request, "Iris image verification failed.")
                        return redirect("/")
                else:
                    # If no Iris image is provided, fall back to password login
                    login(request, user)
                    return redirect(reverse("voterDashboard"))
        else:
            messages.error(request, "Invalid login credentials or access restricted to voters only.")
            return redirect("/")

    return render(request, "voting/login.html", context)


# def account_login(request):
#     if request.user.is_authenticated:
#         if request.user.user_type == '1':  # Admin user type
#             return redirect(reverse("adminDashboard"))
#         else:
#             return redirect(reverse("voterDashboard"))  # Voter user type
#
#     context = {}
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         iris_image = request.FILES.get('iris_image')  # Capture the uploaded Iris image if provided
#
#         # Authenticate the user with email and password
#         user = EmailBackend.authenticate(request, username=email, password=password)
#
#         if user is not None:
#             if user.user_type == '1':  # Admin user type
#                 login(request, user)
#                 return redirect(reverse("adminDashboard"))
#             elif user.user_type == '2':  # Voter user type
#                 if iris_image:  # If an Iris image is provided, verify it
#                     if verify_iris_image(iris_image, user):  # Replace this function with actual Iris verification logic
#                         login(request, user)
#                         return redirect(reverse("voterDashboard"))
#                     else:
#                         messages.error(request, "Iris image verification failed.")
#                         return redirect("/")
#                 else:
#                     # If no Iris image is provided, fall back to password login
#                     login(request, user)
#                     return redirect(reverse("voterDashboard"))
#         else:
#             messages.error(request, "Invalid login credentials or access restricted to voters only.")
#             return redirect("/")
#
#     return render(request, "voting/login.html", context)



def verify_iris_image(iris_image, user):
    """
    Function to verify the Iris image by comparing it with the registered Iris image.
    This implementation assumes that the Iris image is stored in a specific location in the Voter model.
    """
    fs = FileSystemStorage()
    filename = fs.save(iris_image.name, iris_image)  # Save the uploaded Iris image temporarily
    uploaded_image_path = fs.url(filename)  # URL path (relative)

    # Normalize the path separators (for cross-platform compatibility)
    uploaded_image_abs_path = os.path.join("E:\\e-voting\\", uploaded_image_path.lstrip('/'))
    uploaded_image_abs_path = os.path.normpath(uploaded_image_abs_path)  # Normalize path separators

    print(f"Uploaded image path: {uploaded_image_abs_path}")  # Debug: Print the uploaded image path

    # Step 1: Read the uploaded Iris image with OpenCV (convert to grayscale if needed)
    uploaded_image = cv2.imread(uploaded_image_abs_path, cv2.IMREAD_GRAYSCALE)

    if uploaded_image is None:
        print("Error: Unable to load the uploaded image.")
        # Delete the temporary uploaded image
        os.remove(uploaded_image_abs_path)
        return False

    # Step 2: Get the registered image path from the Voter model
    try:
        voter = Voter.objects.get(admin=user)  # Get the Voter record associated with the user
        registered_image_path = os.path.join("E:\\e-voting\\", voter.iris_image.url.lstrip('/'))  # Path to the registered Iris image
    except Voter.DoesNotExist:
        print("Error: Voter not found for the user.")
        os.remove(uploaded_image_abs_path)
        return False

    # Normalize the registered image path (same as uploaded image)
    registered_image_path = os.path.normpath(registered_image_path)  # Normalize path separators

    print(f"Registered image path: {registered_image_path}")  # Debug: Print the registered image path

    # Step 3: Load the registered image (convert to grayscale if needed)
    registered_image = cv2.imread(registered_image_path, cv2.IMREAD_GRAYSCALE)

    if registered_image is None:
        print("Error: Unable to load the registered image.")
        os.remove(uploaded_image_abs_path)
        return False

    # Step 4: Resize both images to the same size
    uploaded_image_resized = cv2.resize(uploaded_image, (registered_image.shape[1], registered_image.shape[0]))

    # Step 5: Compare the uploaded and registered images (using absolute difference for simplicity)
    diff = cv2.absdiff(uploaded_image_resized, registered_image)
    non_zero_diff = cv2.countNonZero(diff)

    print(f"Non-zero difference: {non_zero_diff}")  # Debug: Print the pixel difference

    # Delete the temporary uploaded image after comparison
    os.remove(uploaded_image_abs_path)

    # Threshold the difference to consider it as a valid match
    if non_zero_diff < 1000:  # This threshold is an example; you can adjust it based on the images
        return True  # Iris image verified successfully
    else:
        return False  # Iris image verification failed





def account_register(request):
    userForm = CustomUserForm(request.POST or None)
    voterForm = VoterForm(request.POST, request.FILES or None)  # Handle file uploads
    context = {
        'form1': userForm,
        'form2': voterForm
    }
    if request.method == 'POST':
        if userForm.is_valid() and voterForm.is_valid():
            user = userForm.save(commit=False)
            voter = voterForm.save(commit=False)

            # Associate the voter with the user
            voter.admin = user

            # Save the user and voter objects
            user.save()
            voter.save()

            messages.success(request, "Account created. You can login now!")
            return redirect(reverse('account_login'))
        else:
            messages.error(request, "Provided data failed validation")

    return render(request, "voting/reg.html", context)


def account_logout(request):
    user = request.user
    if user.is_authenticated:
        logout(request)
        messages.success(request, "Thank you for visiting us!")
    else:
        messages.error(
            request, "You need to be logged in to perform this action")

    return redirect(reverse("account_login"))
