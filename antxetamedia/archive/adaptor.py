from watson import search


class SearchAdapter(search.SearchAdapter):
    def get_description(self, obj):
        if hasattr(obj, 'description'):
            return obj.description
        return super(SearchAdapter, self).get_description(obj)

    def get_meta(self, obj):
        meta = super(SearchAdapter, self).get_meta(obj)
        if hasattr(obj, 'image'):
            meta['image'] = None
            if obj.image:
                meta['image'] = obj.image.url
        return meta


def register(model):
    search.register(model, adapter_cls=SearchAdapter)
