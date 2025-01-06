from django.forms import ModelForm
from center.models import Center


class CenterForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CenterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"]= "form-control"
    class Meta:
        model = Center
        fields = "__all__"