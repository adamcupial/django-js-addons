jQuery(document).ready(function(){

    jQuery('form.ajaxify [type="submit"]').live('click',function(event){

        var form = jQuery(this).closest('form');
        var data = form.serializeArray();
        var url = form.attr('action');
        var type = form.attr('method');
        var eventSuccess = form.find('input[name="eventSuccess"]').val();
        var eventError = form.find('input[name="eventError"]').val();

        jQuery.ajax({
           url: url,
           type:type,
           data:data,
           success: function(data){
                form.trigger(eventSuccess);
            },
           error: function(data){
                form.trigger(eventError);
            }
        });

        event.preventDefault();
    });

});
