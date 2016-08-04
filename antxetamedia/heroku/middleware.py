from django.utils.deprecation import MiddlewareMixin

from raygun_dot_io.middleware import RaygunDotIOMiddleware


class RaygunLoggingMiddleware(MiddlewareMixin, RaygunDotIOMiddleware):
    pass
