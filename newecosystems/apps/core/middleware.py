"""Add user created_by and modified_by foreign key refs to any model automatically.
   Almost entirely taken from https://github.com/Atomidata/django-audit-log/blob/master/audit_log/middleware.py
   Modified from http://mindlace.wordpress.com/2012/10/19/automatically-associating-users-with-django-models-on-save/"""
from django.db.models import signals
from django.utils.functional import curry
 
class WhoMiddleware(object):
    def process_request(self, request):
    #if not request.method in ('GET', 'HEAD', 'OPTIONS', 'TRACE'):
        if hasattr(request, 'user') and request.user.is_authenticated():
            user = request.user
        else:
            user = None
        mark_whodid = curry(self.mark_whodid, user)
        signals.pre_save.connect(mark_whodid,  dispatch_uid = (self.__class__, request,), weak = False)
 
    def process_response(self, request, response):
        signals.pre_save.disconnect(dispatch_uid =  (self.__class__, request,))
        return response
 
    def mark_whodid(self, user, sender, instance, **kwargs):
        # if not getattr(instance, 'created_by_id', None):
        #     instance.created_by = user
        if hasattr(instance, 'last_user_modified_id'):
            instance.last_user_modified = user
