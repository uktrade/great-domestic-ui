from article.views import CMSPageView


class UKEFHomeView(CMSPageView):
    template_name = 'ukef/home_page.html'


class UKEFLandingView(CMSPageView):
    template_name = 'ukef/landing_page.html'
