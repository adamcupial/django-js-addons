Author: Adam Cupiał
www: webdesign-log.pl

# Ajax Tools

## DESCRIPTION
Set of ajax tools for django

 * render_to_json decorator - decorates view, returns json
 * ajaxify - js script with jquery, submit's any form via ajax, and triggers appropriate event

## INSTALLATION

 * copy 'ajax_tools' directory from 'ajax_tools/media' to your media directory
 * in your template head section add appropriate media
 * using ajaxify add jQuery library (1.4+) before

## USAGE

### decorators

####  render_to_json

just decorate your view with it, it will json_dump the result:

	from js_addons.ajax_tools.decorators import render_to_json

    @render_to_json()
    def get_json_response(request):
        ...
        ...
        return {'super':super }


####  ajax_required

just decorate your view with it, for not-ajax request you get 404:

	from js_addons.ajax_tools.decorators import ajax_required

    @ajax_required()
    def my_ajax_only_view(request):
    	...

#### ajax_messages

best ussed in urls, you decorate your view with it and pass appropriate messages

	from js_addons.ajax_tools.decorators import ajax_messages
	...
	url('/path', ajax_messages(my_view, success_message='OK', error_message='Not-Ok'))
	...


### Views
	There are only 3 of them:
	
		* ajax_only_object_detail
		* ajax_only_object_list
		* ajax_only_direct_to_template

	which are just your basic django generic views, with added ajax_required decorator. For convenience only.

### Scripts

#### ajaxify

1. add script to your head

2. on form tag add class 'ajaxify' and add two hidden fields 'eventSuccess',
'eventError', which in value should have names (space separated) of events you wish to trigger :

    <form class="ajaxify" action="my url" method="post" >
        <input type="hidden" name="eventSuccess" value="mySuperSuccessEvent myOtherSuccessEvent" />
        <input type="hidden" name="eventError" value="mySuperFailureEvent" />
        ....
    </form>
    
if there are no fields two generic events are propagated: GenericSuccess and GenericError

3. on submit of the form it will be:

  * send to the url specified in the form 'action'
  * using the method specified in the form 'method'
  * on success it starts event(s) of name specified on *eventSuccess* field,
  * on error it starts event(s) of name specified on *eventError* field
  * all events will have message property - which contains response, and form_data property - which contains sent forms data

you can then catch the event higher in the DOM:

    jQuery(document).ready(function(){

        //we'll catch events on document:

        jQuery(document).bind('mySuperSuccessEvent',function(event){
        	var form=event.target;
        	var message = event.message;
        	var form_data = event.form_data;

            alert(message);
        });

    });
