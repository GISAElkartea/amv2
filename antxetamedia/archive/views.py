from watson.views import SearchView


class SearchView(SearchView):
    template_name = 'archive/search.html'
    paginate_by = 10
