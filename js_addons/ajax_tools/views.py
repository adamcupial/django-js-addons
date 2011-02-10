from decorators import ajax_required
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.simple import direct_to_template


@ajax_required
def ajax_only_object_detail(request, object_id=None, slug=None,
        extra_context=None, template_name=None, template_name_field=None,
        template_loader=None, context_processors=None,
        template_object_name=None, queryset=None, paginate_by=None):
    """standard django generic object_detail, only for ajax_requests """

    return object_detail(request, object_id=None, slug=None,
            extra_context=None, template_name=None, template_name_field=None,
            template_loader=None, context_processors=None,
            template_object_name=None, queryset=None, paginate_by=None)


@ajax_required
def ajax_only_object_list(request, extra_context=None, template_name=None,
    queryset=None, paginate_by=None, page=None, template_loader=None,
    allow_empty=None, context_processors=None, template_object_name=None,
    mimetype=None):
    """standard django generic object_list, only for ajax requests """

    return object_list(request, extra_context=None, template_name=None,
        queryset=None, paginate_by=None, page=None, template_loader=None,
        allow_empty=None, context_processors=None, template_object_name=None,
        mimetype=None)


@ajax_required
def xhr_direct_to_template(request, template, extra_context=None,
        mimetype=None, **kwargs):
    """standard django direct_to_template, only for ajax requests """

    return direct_to_template(request, template, extra_context=None,
            mimetype=None, **kwargs)
