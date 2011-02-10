from functools import wraps
from django.http import HttpResponse, Http404
from django.utils import simplejson as json


def render_to_json(**jsonargs):
    """ renders given request in json """

    def outer(f):

        @wraps(f)
        def inner_json(request, *args, **kwargs):
            result = f(request, *args, **kwargs)
            r = HttpResponse(mimetype='application/json')
            if result:
                indent = jsonargs.pop('indent', 4)
                r.write(json.dumps(result, indent=indent, **jsonargs))
            else:
                r.write("{}")
            return r
        return inner_json
    return outer


def ajax_messages(fn, success_message='Success', error_message='Error'):
    """ returns given success or error message according to response status_code
    
        be warned, that this decorator changes the response code for "jQuery
        safe" ones - 200 for success, 500 otherwise
    """

    def process(request, *args, **kwargs):
        decorated = fn(request, *args, **kwargs)
        if decorated.status_code in [200, 301, 302, 304, 307]:
            message = success_message
            status_code = 200
        else:
            message = error_message
            status_code = 500
        if request.is_ajax():
            return HttpResponse(content=message, status=status_code)
        else:
            return decorated
    return process


def ajax_required(f):
    """AJAX required view decorator """

    def wrap(request, *args, **kwargs):
            if not request.is_ajax():
                raise Http404
            return f(request, *args, **kwargs)
    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap
