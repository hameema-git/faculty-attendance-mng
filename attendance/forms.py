# from django import forms
# from .models import CustomUser

# class FacultyForm(forms.ModelForm):
#     class Meta:
#         model = CustomUser
#         fields = ['username', 'email', 'password', 'is_faculty']

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data['password'])  # hash password
#         if commit:
#             user.save()
#         return user

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, FacultyProfile

# class FacultyForm(UserCreationForm):
#     email = forms.EmailField(required=True)
#     department = forms.CharField(required=True)
#     joining_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

#     class Meta:
#         model = CustomUser
#         fields = ['username', 'email', 'password1', 'password2']

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.email = self.cleaned_data['email']
#         user.is_faculty = True
#         if commit:
#             user.save()
#             # Create faculty profile
#             FacultyProfile.objects.create(
#                 user=user,
#                 department=self.cleaned_data['department'],
#                 joining_date=self.cleaned_data['joining_date']
#             )
#         return user


class FacultyForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    department = forms.CharField(required=True)
    joining_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    personal_phone = forms.CharField(required=True)
    guardian_phone = forms.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.is_faculty = True
        if commit:
            user.save()
            FacultyProfile.objects.create(
                user=user,
                department=self.cleaned_data['department'],
                joining_date=self.cleaned_data['joining_date'],
                personal_phone=self.cleaned_data['personal_phone'],
                guardian_phone=self.cleaned_data['guardian_phone']
            )
        return user
    
from django import forms
from .models import CustomUser, FacultyProfile,Attendance

class EditFacultyForm(forms.ModelForm):
    department = forms.CharField(required=True)
    joining_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    personal_phone = forms.CharField()
    guardian_phone = forms.CharField()

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email']

# class AttendanceForm(forms.ModelForm):
#     class Meta:
#         model = Attendance
#         fields = ['status', 'hours_worked', 'message']
#         widgets = {
#             'message': forms.Textarea(attrs={'rows': 2}),
#         }
class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['status', 'date', 'hours_worked', 'message', 'approved']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'status': forms.Select(),
            'message': forms.Textarea(attrs={'rows': 2}),
        }

class AttendanceForm1(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['status', 'hours_worked', 'message']  # Removed date and approved
        widgets = {
            'status': forms.Select(),
            'message': forms.Textarea(attrs={'rows': 2}),
        }
