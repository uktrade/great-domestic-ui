from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'ukef/home_page.html'
