Author: Adam Cupiał
www: webdesign-log.pl

# Ajax Tools

## DESCRIPTION
Set of ajax tools for django

 * render_to_json decorator - decorates view, returns json

## INSTALLATION

 * copy 'ajax_tools' directory from 'ajax_tools/media' to your media directory
 * in your template head section add appropriate media:

## USAGE

###  render_to_json

just decorate your view with it:

    @render_to_json()
    def get_json_response(request):
        ...
        ...
        return {'super':super }
