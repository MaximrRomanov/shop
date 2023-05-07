class DataMixin:
    def get_context_data(self, *, object_list=None, **kwargs):
        context = kwargs
