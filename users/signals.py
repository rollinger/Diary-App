from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.utils.translation import gettext_lazy as _

User = get_user_model()

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
	if created:
		Token.objects.create(user=instance)

# USER CREATION (post save)
@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
	if created:
		# Add to is_staff to access admin
		instance.is_staff = True
		# Add User to normal User group
		normal_user_group = Group.objects.get(name='Normal User') 
		normal_user_group.user_set.add(instance)
		instance.save()

# USER DELETION (post save)
@receiver(pre_delete, sender=User)
def user_before_delete(sender, instance, **kwargs):
	# Cleanup Code 
	# Currently Stub
    pass