from braces.views import StaffuserRequiredMixin
from django.views.generic import TemplateView


class Dashboard(TemplateView, StaffuserRequiredMixin):
    template_name = 'admin-panel/dashboard.html'
