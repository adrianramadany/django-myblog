from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import Group
from .models import UserProfile

class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit=False)
        
        # Assign to Author group by default
        author_group, created = Group.objects.get_or_create(name='Author')
        user.groups.add(author_group)
        
        if commit:
            user.save()
            # Create UserProfile
            UserProfile.objects.get_or_create(user=user)
        
        return user

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        
        # Assign to Author group by default
        author_group, created = Group.objects.get_or_create(name='Author')
        user.groups.add(author_group)
        
        # Create UserProfile
        UserProfile.objects.get_or_create(user=user)
        
        return user 