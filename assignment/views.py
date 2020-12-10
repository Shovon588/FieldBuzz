import json
import requests
import uuid
from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render

from .forms import LoginForm, InfoForm
from .utils import upload_resume

LOGIN_URL = "https://recruitment.fisdev.com/api/login/"
INFO_URL = "https://recruitment.fisdev.com/api/v1/recruiting-entities/"
FILE_UPLOAD_URL = "https://recruitment.fisdev.com/api/file-object/"
TSYNC_INFO = str(uuid.uuid1())
TSYNC_RESUME = str(uuid.uuid1())


INFO_FIELDS = ['name', 'email', 'phone', 'full_address',
               'name_of_university', 'graduation_year', 'cgpa',
               'experience_in_months', 'current_work_place_name',
               'applying_in', 'expected_salary', 'field_buzz_reference', 'github_project_url']

OPTIONAL_FIELDS = ['full_address', 'experience_in_months',
                   'current_work_place_name', 'field_buzz_reference']


def login(request):
    """
    Renders a login form
    Collects data upon post request
    Calls field buzz login api and fetch the token.
    """
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            payload = {
                'username': username,
                'password': password,
            }

            response = requests.post(LOGIN_URL, payload)
            if response.status_code == 200:
                token = response.json()["token"]
                request.session['token'] = token
                return redirect('info')

            message = response.json()['message']
            messages.warning(request, message)

    return render(request, 'login.html', {'form': form})


def info(request):
    """
    Renders a detailed information form
    Receives data upon post request
    Calls info update api with relevent payload
    Upon successfull submission fetch file token id
    Calls the file upload api and uploads resume
    """
    form = InfoForm
    if request.method == "POST":
        form = InfoForm(request.POST, request.FILES)
        if form.is_valid():
            token = request.session['token']
            resume = form.cleaned_data['cv_file']

            payload = {
                "tsync_id": TSYNC_INFO,
                "cv_file": {
                    "tsync_id": TSYNC_RESUME,
                }
            }

            for field in INFO_FIELDS:
                payload[field] = form.cleaned_data[field]

            for field in OPTIONAL_FIELDS:
                if not payload[field]:
                    payload.pop(field)

            headers = {
                'Authorization': 'Token ' + token,
                'Content-Type': 'application/json'
            }

            payload = json.dumps(payload)

            response = requests.post(INFO_URL, data=payload, headers=headers)
            if response.status_code == 201:
                file_token_id = response.json()['cv_file']['id']
                url = FILE_UPLOAD_URL + str(file_token_id) + "/"

                response = upload_resume(resume, url, token)

                if response.status_code == 200:
                    return redirect("success")
                else:
                    messages.info(request, "Resume upload failed. Try again.")
            else:
                messages.info(
                    request, "Couldn't send informations. Try again.")

    if 'token' in request.session:
        token = request.session['token']
    else:
        token = ""

    context = {
        'form': form,
        'token': token,
    }
    return render(request, 'info.html', context=context)


def success(request):
    """
    Congratulate user upon successful submission
    """
    return render(request, 'success.html')
