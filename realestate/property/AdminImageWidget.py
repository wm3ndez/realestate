from django.contrib.admin.widgets import AdminFileWidget
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from sorl.thumbnail.shortcuts import get_thumbnail

class AdminImageWidget(AdminFileWidget):
    """
    A FileField Widget that displays an image instead of a file path
    if the current file is an image.
    """

    def render(self, name, value, attrs=None):
        output = []
        import pdb;

        pdb.set_trace()
        image = get_thumbnail(object.imagen, '75x50', crop='center', quality=99)
        output.append(
            '<a target="_blank" href="%s"><img src="%s"/></a><br />%s ' % (
                image.picture, image.url, _('Change:')))

        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))