from models.fields import RelatedField


class QuerySet:
    def __init__(self, model_cls, data):
        self.model_cls = model_cls
        self._instances = [model_cls(**item) for item in data]

    def filter(self, **kwargs):
        filtered_instances = [
            instance
            for instance in self._instances
            if all(getattr(instance, key) == value for key, value in kwargs.items())
        ]
        return QuerySet(
            self.model_cls, [instance.__dict__ for instance in filtered_instances]
        )

    def map(self, func):
        return [func(instance) for instance in self._instances]

    def all(self, load_related=False):
        if load_related:
            self.load_related()
        return self._instances

    def load_related(self):
        for i in self._instances:
            for field_name, field_value in i._fields.items():
                if isinstance(field_value, RelatedField):
                    setattr(
                        i,
                        f"{field_name}_obj",
                        field_value.model.all().get(id=getattr(i, field_name)),
                    )

    def get(self, **kwargs):
        res = self.filter(**kwargs).all()
        if len(res) > 1:
            raise Exception("More than 1 record found")
        if len(res) == 0:
            raise Exception("No record found")
        return res[0]
