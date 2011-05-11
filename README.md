Author: Adam Cupiał

www: http://webdesign-log.pl

# django-js-addons

## Description
 Repo with different js addons for django, for details see separate README's,
 now package includes:

### Calendar
  * js calendar form widget, based on Dynarch Calendar 1.8, both in standalone and popup version

### ajax_tools
  * set of ajax tools, now includes:
    * render_to_json decorator (json_dump on response from view)
    * ajax_required decorator (if not ajax, then 404)
    * other_if_ajax decorator - different view when ajax
    * ajax_message decorators (if is ajax, return message - appriopriate to status)
    * ajax-only versions of django generic object_list, object_detail and direct_to_template (named accordingly ajax_only_[NAME])
    * ajax_form view - for ajax forms - validate forms with django, return them with ajax
    * ajaxify script for ajax form submitting
