/* ================= Ajaxify a form, any form ===================
 *
 * Ok, the reason behind this script is quite simple - I send so many forms via ajax, and then processed a response that I made a script to automatize it.
 *
 * It's quite easy to use, just add a class "ajaxify" to form you wish to send via ajax (to url in action attribute, via method in method attributes),
 * add two hidden inputs to the form with names:
 *  - eventSuccess : in value give the list on events names (space separated) which should be triggered on 'success response'
 *  - eventError : in value give the list on events names (space separated) which should be triggered on 'error response'
 *
 * Thanks to event bubbling you can quite easy catch the events at 'document' level:
 *  - all the form data is passed in event, as property form_data
 *  - server response is passed as message property in event
 *  - since event is triggered by form element, you can easily get to the form via events 'target' param.
 */

jQuery(document).ready(function(){

	jQuery('form.ajaxify').live('submit',function(event){

		var form = jQuery(this);
		var i;
		var data = form.serializeArray();
		var url = form.attr('action');
		var type = form.attr('method');
		var eventSuccessName = form.find('input[name="eventSuccess"]').val().split(' ');
		var eventErrorName = form.find('input[name="eventError"]').val().split(' ');
	
		if(eventSuccessName === undefined){
			eventSuccessName = 'GenericSuccess';
		}

		if(eventErrorName === undefined){
			eventErrorName = 'GenericError';
		}

		var eventSuccess = [];
		for(i = 0; i < eventSuccessName.length; i++){
			e = eventSuccessName[i];
			a = new jQuery.Event(e);
			a.form_data = data;
			eventSuccess.push(a);
		}

		var eventError = [];
		for(i = 0; i < eventErrorName.length; i++){
			e = eventErrorName[i];
			a = new jQuery.Event(e);
			a.form_data = data;
			eventError.push(a);
		}

		jQuery.ajax({
			url: url,
			type:type,
			data:data,
			success: function(data){
				for (var i = 0; i < eventSuccess.length; i++){
					ev = eventSuccess[i];
					ev.message = data;
					form.trigger(ev);
				}
			},
			error: function(data){
				for (var i = 0; i < eventError.length; i++){
					ev = eventError[i];
					ev.message = data.responseText;
					form.trigger(ev);
				}
			}
		});

		event.preventDefault();
	});

});
