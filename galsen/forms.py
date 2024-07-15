import re
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    langue = forms.ChoiceField(choices=get_user_model().LANGUE, initial='français', widget=forms.Select(attrs={'autocomplete': 'off'}))
    rôle = forms.ChoiceField(choices=get_user_model().ROLES, initial='personnel', widget=forms.Select(attrs={'autocomplete': 'off'}))
    genre = forms.ChoiceField(choices=get_user_model().GENRE, widget=forms.Select(attrs={'autocomplete': 'off'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    etablissement = forms.CharField(widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'autocomplete': 'off'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'off'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'off'}))
    
    class Meta:
        model = get_user_model()
        fields = ('langue', 'rôle', 'genre', 'username', 'etablissement', 'email', 'password1', 'password2')
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        # Validate username length
        if len(username) > 150:
            self.add_error('username', "Le nom d'utilisateur ne peut pas dépasser 150 caractères.")
        
        # Validate email uniqueness
        if get_user_model().objects.filter(email=email).exists():
            self.add_error('email', "Un compte avec cette adresse e-mail existe déjà.")
        
        # Validate passwords match
        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Les mots de passe ne correspondent pas.")
    
        return cleaned_data

class ShareForm(forms.Form):
    body = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows': '3',
            'placeholder': 'Say Something...'
            }))

class EmailChangeForm(forms.ModelForm):
    password = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(attrs={'placeholder': 'Mot de Passe pour valider'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Votre nouvelle adresse mail'})
    )

    class Meta:
        model = get_user_model()
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super(EmailChangeForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'Votre nouvelle adresse mail'

    def clean_password(self):
        password = self.cleaned_data['password']
        user = self.instance

        if not user.check_password(password):
            raise forms.ValidationError("Mot de passe incorrect.")
        return password
    
class NameChangeForm(forms.ModelForm):
    password = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(attrs={'placeholder': 'Mot de Passe pour valider'})
    )

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(NameChangeForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Votre Nouveau Prénom'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Votre Nouveau Nom'})

    def clean_password(self):
        password = self.cleaned_data['password']
        user = self.instance

        if not user.check_password(password):
            raise forms.ValidationError("Mot de passe incorrect.")
        return password


class RoleChangeForm(forms.ModelForm):
    password = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(attrs={'placeholder': 'Mot de Passe pour valider'})
    )
    rôle = forms.ChoiceField(choices=get_user_model().ROLES, widget=forms.Select(attrs={'autocomplete': 'off'}))

    class Meta:
        model = get_user_model()
        fields = ['rôle']

    def clean_password(self):
        password = self.cleaned_data['password']
        user = self.instance

        if not user.check_password(password):
            raise forms.ValidationError("Mot de passe incorrect.")
        return password
    
class AccountDeleteForm(forms.Form):
    password = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(attrs={'placeholder': 'Mot de Passe pour valider'})
    )

    def clean_password(self):
        password = self.cleaned_data['password']
        # Logique de validation du mot de passe ici
        
        return password
    
class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({
            'autocomplete': 'current-password',
            'placeholder': 'Ancien mot de passe'
        })
        self.fields['new_password1'].widget.attrs.update({
            'autocomplete': 'new-password',
            'placeholder': 'Nouveau mot de passe'
        })
        self.fields['new_password2'].widget.attrs.update({
            'autocomplete': 'new-password',
            'placeholder': 'Confirmer le nouveau mot de passe'
        })

    class Meta:
        model = get_user_model()
        fields = ('old_password', 'new_password1', 'new_password2')