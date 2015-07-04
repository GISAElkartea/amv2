from .models import Flatpage


def menu_flatpage_list(request):
    return {'menu_flatpage_list': Flatpage.objects.on_menu()}
