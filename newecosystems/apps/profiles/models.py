from django.db import models
from django.utils.translation import ugettext_lazy as _
from userena.models import UserenaLanguageBaseProfile
from userena.utils import user_model_label

class Profile(UserenaLanguageBaseProfile):
    user = models.OneToOneField(user_model_label,
                                unique=True,
                                verbose_name=_('user'),
                                related_name='profile')

