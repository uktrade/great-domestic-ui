from django.views.generic import TemplateView

from ukef.mixins import UKEFPagesFeatureFlagMixin


class HomeView(UKEFPagesFeatureFlagMixin, TemplateView):
    template_name = 'ukef/home_page.html'


class LandingView(UKEFPagesFeatureFlagMixin, TemplateView):
    template_name = 'ukef/landing_page.html'
