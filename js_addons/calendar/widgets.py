from django.utils.encoding import force_unicode
from django.conf import settings
from django import forms
import datetime, time
from django.utils.safestring import mark_safe

calbtn = u"""<img src="%(media_url)scalendar/cal.gif" alt="kalendarz" id="%(field_id)s_btn" style="cursor: pointer; float:left;position:relative;top:2px;" title="Kalendarz"
            onmouseover="this.style.background='#444444';" onmouseout="this.style.background=''" class="calendar-button"/>
<script type="text/javascript">
    Calendar.setup({
        inputField     :    "%(field_id)s",
        dateFormat       :    "%(date_format)s",
        trigger :  "%(field_id)s_btn",
        showTime  :    false,
        titleFormat : "%(title_format)s",
        min:%(min_date)s,
        max:%(max_date)s
    });
</script>"""

calbtn_always_visible = u"""<div id="%(field_id)s_container" title="Kalendarz" />
<script type="text/javascript">
    Calendar.setup({
        cont     :    "%(field_id)s_container",
        dateFormat       :    "%(date_format)s",
        showTime  :    false,
        titleFormat : "%(title_format)s",
        min:%(min_date)s,
        max:%(max_date)s,
        onSelect:function(){
            var date = this.selection.get();
            date = Calendar.intToDate(date);
            date = Calendar.printDate(date,"%(date_format)s");
            var input = document.getElementById('%(field_id)s');
            input.value = date;
        }
    });
</script>"""


class CalendarWidget(forms.widgets.TextInput):
    """
    @Author: Adam Cupial
    @Date: 12/10/2010

    Short description
    ------------------

      Django calendar widget, requires js and css files, uses Dynarch Calendar

    Settings
    ------------------

      date_format (default: '%Y-%m-%d'),
      title_format (default: '%b %Y')

    """
    def __init__(self, attrs=None, date_format='%Y-%m-%d',title_format='%b %Y',min_date=None, max_date=None):
        self.date_format = date_format
        self.title_format = title_format
        if min_date:
            self.min_date = min_date.strftime("%Y%m%d")
        else:
            self.min_date = 'null'
        if max_date:
            self.max_date = max_date.strftime("%Y%m%d")
        else:
            self.max_date = 'null'
        super(CalendarWidget, self).__init__(attrs)

    def _media(self):
        return forms.Media(css={
            'all': (settings.MEDIA_URL+'calendar/css/cal.css',)
                },
                        js=(settings.MEDIA_URL+'calendar/js/jscal2.js',
                            settings.MEDIA_URL+'calendar/js/lang/pl.js')
                        )

    media = property(_media)

    def render(self, name, value, attrs=None):
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            try:
                final_attrs['value'] = \
                                   force_unicode(value.strftime(self.date_format))
            except:
                final_attrs['value'] = \
                                   force_unicode(value)

        if not final_attrs.has_key('id'):
            final_attrs['id'] = u'%s_id' % (name)
        id = final_attrs['id']

        cal = self.get_js() % {
                'media_url':settings.MEDIA_URL,
                'field_id':id,
                'date_format':self.date_format,
                'title_format':self.title_format,
                'min_date':self.min_date, 
                'max_date':self.max_date
                }
        a = u'<input%s class="calendar-input"/>%s' % (forms.util.flatatt(final_attrs), cal)
        return mark_safe(a)
    
    def get_js(self):
        return calbtn

    def value_from_datadict(self, data, files, name):
        dtf = forms.fields.DEFAULT_DATETIME_INPUT_FORMATS
        empty_values = forms.fields.EMPTY_VALUES

        value = data.get(name, None)
        if value in empty_values:
            return None
        if isinstance(value, datetime.datetime):
            return value
        if isinstance(value, datetime.date):
            return datetime.datetime(value.year, value.month, value.day)
        for format in dtf:
            try:
                return datetime.datetime(*time.strptime(value, format)[:6])
            except ValueError:
                continue
        return None

class CalendarOnlyWidget(CalendarWidget):
    input_type='hidden'
    is_hidden = True

    def get_js(self):
        return calbtn_always_visible
