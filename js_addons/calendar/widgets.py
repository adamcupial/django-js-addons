from django.utils.encoding import force_unicode
from django.conf import settings
from django import forms
import datetime, time
from django.utils.safestring import mark_safe

calbtn = u"""<img src="%scalendar/cal.gif" alt="kalendarz" id="%s_btn" style="cursor: pointer; float:left;position:relative;top:2px;" title="Kalendarz"
            onmouseover="this.style.background='#444444';" onmouseout="this.style.background=''" class="calendar-button"/>
<script type="text/javascript">
    Calendar.setup({
        inputField     :    "%s",
        dateFormat       :    "%s",
        trigger :  "%s_btn",
        showTime  :    false,
        titleFormat : "%s",
        min:%s,
        max:%s
    });
</script>"""

class CalendarWidget(forms.widgets.TextInput):
    """
    @Author: Adam Cupial
    @Date: 12/10/2010

    Short description
    ----------------------------

      Django calendar widget, requires js and css files, uses Dynarch Calendar

    Settings
    ----------------------------

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

        cal = calbtn % (settings.MEDIA_URL, id, id, self.date_format, id, self.title_format, self.min_date, self.max_date)
        a = u'<input%s class="calendar-input"/>%s' % (forms.util.flatatt(final_attrs), cal)
        return mark_safe(a)

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
