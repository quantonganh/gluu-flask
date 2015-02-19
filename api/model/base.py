class BaseModel(object):
    """Base class for model.

    This class should not be used directly.
    """
    resource_fields = {}

    def as_dict(self):
        fields = tuple(self.resource_fields.keys())
        return {
            k: v for k, v in self.__dict__.items()
            if k in fields
        }
