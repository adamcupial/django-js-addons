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

###  render_to_json

just decorate your view with it:

    @render_to_json()
    def get_json_response(request):
        ...
        ...
        return {'super':super }

### ajaxify

1. add script to your head

2. on form tag add class 'ajaxify' and add two hidden fields 'eventSuccess',
'eventError':

    <form class="ajaxify" action="my url" method="post" >
        <input type="hidden" name="eventSuccess" value="mySuperSuccessEvent" />
        <input type="hidden" name="eventError" value="mySuperFailureEvent" />
        ....
    </form>

3. on submit of the form it will be:

  * send to the url specified in the form 'action'
  * using the method specified in the form 'method'
  * on success it starts event of name specified on *eventSuccess* field
  * on error it starts event of name specified on *eventError* field

you can then catch the event higher in the DOM:

  jQuery(document).ready(function(){

    //we'll catch events on body:

    jQuery(body).bind('mySuperSuccessEvent',function(event){
        // do whatever you wish
    });
    
  });
