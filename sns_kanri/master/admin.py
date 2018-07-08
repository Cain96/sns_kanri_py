from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from sns_kanri.master.models import User


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "password")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(user.password)
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'is_active', 'groups',)

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        return self.initial["password"]

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class BaseUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'is_staff']
    list_filter = ['is_active']
    search_fields = ['username', 'email']

    fieldsets = (
        (None, {'fields': ('username', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'groups',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password', 'email'),
        }),
    )

    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = None


admin.site.register(User, BaseUserAdmin)
