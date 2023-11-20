from django.views.generic import ListView, TemplateView
from ppc_2024.filters import PPCFilter
from ppc_2024.models import PPCPerson


# Create your views here.
class PCC2024HomeView(TemplateView):
    template_name = "ppc_2024/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["by_party"] = PPCPerson.objects.by_party()
        context["by_region"] = PPCPerson.objects.by_region()

        return context


class PCC2024DetailView(ListView):
    queryset = PPCPerson.objects.for_details()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)

        ppc_filter = PPCFilter(
            data=self.request.GET, queryset=self.queryset, request=self.request
        )
        context["filter"] = ppc_filter
        context["queryset"] = ppc_filter.qs
        context["csv_url"] = PPCPerson.CSV_URL

        return context
