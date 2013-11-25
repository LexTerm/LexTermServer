from django.db.models import CharField
import uuid

class UUIDField(CharField):
    """ UUIDField for Django. Generates a random 32-character uuid(v4).
        If you specify short=True it will be truncated to 8 characters.
    """

    def __init__(self, verbose_name=None, name=None, auto=True, short=False, **kwargs):
        kwargs['max_length'] = 32
        self.auto = auto
        self.short = short
        if auto:
            kwargs['blank'] = True
            kwargs['editable'] = kwargs.get('editable', False)
        CharField.__init__(self, verbose_name, name, **kwargs)

    def get_internal_type(self):
        return CharField.__name__

    def create_uuid(self):
        if self.short:
            return uuid.uuid4().hex[:8]
        return uuid.uuid4().hex

    def pre_save(self, model_instance, add):
        value = super(UUIDField, self).pre_save(model_instance, add)
        if not value and self.auto and add:
            value = unicode(self.create_uuid())
            setattr(model_instance, self.attname, value)
        return value

