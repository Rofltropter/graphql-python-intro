from django.db import models
#We import django settings as we'll need access to the auth user model piece there
from django.conf import settings
# Create your models here.

"""The Link model class defines the various link variables that belong to a Link object"""
class Link(models.Model):
    url = models.URLField()
    description = models.TextField(blank=True)
    #
    posted_by = models.ForeignKey(         #models.ForeignKey creates a many-to-one relationship, ie. many posted_by descriptors to a single auth'd User Model
        settings.AUTH_USER_MODEL,
        null=True,                         #null's ForeignKey on delete
        on_delete=models.CASCADE)          #cascade deletes on delete


"""The Vote model class allows us to define the vote variables for the platform. We contain this within the links package due to its close integration with links"""
class Vote(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    link = models.ForeignKey(
        'links.Link',               #Sets the relation to the original Link object type
        related_name='votes',         #name for relation from related object to this one, also the default val for related_query_name
        on_delete=models.CASCADE)
