from django.views.generic import TemplateView

from core.mixins import UKEFPagesFeatureFlagMixin


class HomeView(UKEFPagesFeatureFlagMixin, TemplateView):
    template_name = 'ukef/home_page.html'
