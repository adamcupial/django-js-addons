from functools import wraps
from django.http import HttpResponse
from django.utils import simplejson as json
from django.http import HttpResponse

def render_to_json(**jsonargs):
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

def ajax_messages(fn,success_message='Success',error_message='Error'):
    def process(request, *args, **kwargs):
        decorated = fn(request, *args, **kwargs)
        if decorated.status_code in [200,301,302,304,307]:
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