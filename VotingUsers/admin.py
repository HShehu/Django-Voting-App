from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import VotingUser

# Register your models here.


class LoginForm(forms.Form):
    student_number = forms.CharField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = VotingUser
        fields = ('student_number','password',)



class UserCreationForm(forms.ModelForm):

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = VotingUser
        fields = ('student_number', 'full_name',
                  'login_code', 'password1', 'password2')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = VotingUser
        fields = ('student_number', 'password', 'full_name', 'login_code', 'is_staff',
                  'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class VotingUserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('student_number', 'full_name', 'date_joined',
                    'last_login', 'is_admin', 'is_staff')
    search_fields = ('student number', 'full_name', 'is_admin', 'is_staff')
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('full_name', 'student_number', 'password1', 'password2', 'login_code'),
        }),
    )
    ordering = ('full_name',)


admin.site.register(VotingUser, VotingUserAdmin)
admin.site.unregister(Group)
