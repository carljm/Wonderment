import floppyforms.__future__ as forms


class RatingWidget(forms.RadioSelect):
    template_name = 'fall2015eval/rating_widget.html'

    def __init__(self, low_desc, high_desc):
        self.low_desc = low_desc
        self.high_desc = high_desc
        super(RatingWidget, self).__init__()

    def get_context_data(self):
        return {
            'low_desc': self.low_desc,
            'high_desc': self.high_desc,
        }


class RadioSelect(forms.RadioSelect):
    template_name = 'fall2015eval/radio.html'
