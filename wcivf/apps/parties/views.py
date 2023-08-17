from django.db.models import Q
from django.views.generic import DetailView, TemplateView

from .filters import PartyRegisterFilter
from .models import Party


class PartiesView(TemplateView):
    template_name = "parties/parties_view.html"
    # "Parties" which are not EC registered but belong on the parties page
    # e.g. Independent, Speaker seeking re-election
    special_parties = ["ynmp-party:2", "ynmp-party:12522"]

    def get_context_data(self, *args, **kwargs):
        context = super(PartiesView, self).get_context_data(*args, **kwargs)
        queryset = (
            Party.objects.exclude(personpost=None)
            .filter(
                ~Q(ec_id__startswith="ynmp") | Q(ec_id__in=self.special_parties)
            )
            .order_by("party_name")
        )
        f = PartyRegisterFilter(
            data=self.request.GET, queryset=queryset, request=self.request
        )
        context["filter"] = f
        context["shortcuts"] = f.shortcuts
        context["queryset"] = f.qs
        return context


class PartyView(DetailView):
    def get_template_names(self):
        party_id = self.object.party_id

        if party_id == "ynmp-party:2":
            return ["parties/independent_candidate.html"]

        if party_id == "ynmp-party:12522":
            return ["parties/speaker_seeking_reelection.html"]

        return ["parties/party_detail.html"]

    queryset = Party.objects.all()
