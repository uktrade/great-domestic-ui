from django.views.generic import TemplateView

from casestudy import casestudies
from core.helpers import build_social_links
from core.views import SetEtagMixin
from core.mixins import SetGA360ValuesMixin


class BaseCaseStudyView(SetGA360ValuesMixin, TemplateView):
    page_type = 'CaseStudyPage'

    def get_context_data(self, *args, **kwargs):
        social_links = build_social_links(
            request=self.request, title=self.casestudy.title
        )
        return super().get_context_data(
            *args, **kwargs,
            social_links=social_links,
            casestudy=self.casestudy,
        )


class CasestudyHelloBabyView(SetEtagMixin, BaseCaseStudyView):
    template_name = 'casestudy/hello-baby.html'
    casestudy = casestudies.HELLO_BABY


class CasestudyMarketplaceView(SetEtagMixin, BaseCaseStudyView):
    template_name = 'casestudy/marketplace.html'
    casestudy = casestudies.MARKETPLACE


class CasestudyYorkBagView(SetEtagMixin, BaseCaseStudyView):
    template_name = 'casestudy/york-bag.html'
    casestudy = casestudies.YORK
