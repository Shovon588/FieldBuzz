from django import forms


class LoginForm(forms.Form):
    username = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)

    # Attributes to the input field
    username.widget.attrs = {'placeholder': 'Enter your username'}
    password.widget.attrs = {'placeholder': 'Enter your password'}


class InfoForm(forms.Form):
    name = forms.CharField(max_length=256)
    email = forms.EmailField(max_length=256)
    phone = forms.CharField(max_length=14)
    full_address = forms.CharField(max_length=512, required=False)
    name_of_university = forms.CharField(max_length=512)
    graduation_year = forms.IntegerField(min_value=2015, max_value=2020)
    cgpa = forms.FloatField(min_value=2.0, max_value=4.0, required=False)
    experience_in_months = forms.IntegerField(
        min_value=0, max_value=100, required=False)
    current_work_place_name = forms.CharField(max_length=256, required=False)
    CHOICES = (
        ('Backend', 'Backend'),
        ('Frontend', 'Frontend')
    )
    applying_in = forms.ChoiceField(choices=CHOICES)
    expected_salary = forms.IntegerField(min_value=15000, max_value=60000)
    field_buzz_reference = forms.CharField(max_length=256, required=False)
    github_project_url = forms.URLField(max_length=512)
    cv_file = forms.FileField()

    # Attributes to the input field
    name.widget.attrs = {'placeholder': 'Full name'}
    email.widget.attrs = {'placeholder': 'Personal email address'}
    phone.widget.attrs = {'placeholder': 'Personal phone number'}
    full_address.widget.attrs = {'placeholder': 'Address'}
    name_of_university.widget.attrs = {'placeholder': 'University name'}
    graduation_year.widget.attrs = {'placeholder': 'Graduation year'}
    cgpa.widget.attrs = {'placeholder': 'Obtained cgpa', 'step': '0.01'}
    experience_in_months.widget.attrs = {
        'placeholder': 'Work experience'}
    current_work_place_name.widget.attrs = {
        'placeholder': 'Current work place name'}
    expected_salary.widget.attrs = {'placeholder': 'Expected salary'}
    field_buzz_reference.widget.attrs = {'placeholder': 'Field Buzz reference'}
    github_project_url.widget.attrs = {'placeholder': 'Github project url'}
    cv_file.widget.attrs = {'accept': '.pdf'}
