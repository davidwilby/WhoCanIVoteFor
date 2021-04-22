from dateutil.parser import parse
from django.views.generic import TemplateView, DetailView, RedirectView
from django.http import Http404
from django.shortcuts import get_object_or_404


from django.db.models import Prefetch, Count, Sum, Subquery, IntegerField
from django.apps import apps


from elections.views.mixins import (
    NewSlugsRedirectMixin,
    PostelectionsToPeopleMixin,
)
from elections.models import PostElection, Election
from parties.models import LocalParty, Party
from people.models import PersonPost


class ElectionsView(TemplateView):
    template_name = "elections/elections_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        Election = apps.get_model("elections.Election")
        all_elections = Election.objects.all().order_by(
            "-election_date", "election_type", "name"
        )

        context["past_elections"] = all_elections.past()
        context[
            "current_or_future_elections"
        ] = all_elections.current_or_future()

        return context


class ElectionTypeForDateView(TemplateView):
    template_name = "elections/election_type_for_date.html"

    supported_types = {
        "local": "Local",
        "parl": "UK Parliament",
        "nia": "Northern Ireland Assembly",
        "senedd": "Senedd Cymru",
        "sp": "Scottish Parliament",
        "gla": "Greater London Assembly",
        "pcc": "Police and Crime Commissioner",
        "mayor": "Mayoral",
    }

    def get(self, request, *args, **kwargs):
        self.election_type, self.election_date = self.kwargs.get(
            "election"
        ).split(".")
        if self.election_type not in self.supported_types.keys():
            raise Http404()
        return super().get(request, *args, **kwargs)

    def get_template_names(self):
        return [
            f"elections/{self.election_type}_election_type_for_date.html",
            "elections/generic_election_type_for_date.html",
        ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["election_type"] = self.supported_types[self.election_type]
        context["election_date"] = parse(self.election_date)

        base_elections_qs = Election.objects.filter(
            election_date=self.election_date, election_type=self.election_type
        ).order_by("name")

        aggregate_qs = base_elections_qs.order_by("postelection")
        context["total_candidates"] = aggregate_qs.all().aggregate(
            total_candidates=Count("postelection__personpost", distinct=True)
        )["total_candidates"]

        context["total_seats"] = aggregate_qs.all().aggregate(
            total_seats=Sum("postelection__winner_count")
        )["total_seats"]

        context["total_parties"] = aggregate_qs.all().aggregate(
            total_parties=Count(
                "postelection__personpost__party", distinct=True
            ),
        )["total_parties"]

        context["total_ballots"] = aggregate_qs.all().aggregate(
            total_ballots=Count("postelection__ballot_paper_id", distinct=True),
        )["total_ballots"]

        context["elections"] = base_elections_qs.annotate(
            parties_count=Count(
                "postelection__personpost__party", distinct=True
            ),
            candidates_count=Count("postelection__personpost", distinct=True),
            ballots=Count("postelection", distinct=True),
        ).annotate(
            seats_total=Subquery(
                base_elections_qs.order_by("postelection")
                .annotate(sum_value=Sum("postelection__winner_count"))
                .values("sum_value"),
                output_field=IntegerField(),
            )
        )

        return context


class ElectionView(NewSlugsRedirectMixin, DetailView):
    template_name = "elections/election_view.html"
    model = apps.get_model("elections.Election")
    pk_url_kwarg = "election"

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg)
        PostElection = apps.get_model("elections.PostElection")
        queryset = queryset.filter(slug=pk).prefetch_related(
            Prefetch(
                "postelection_set",
                queryset=PostElection.objects.all()
                .select_related("election", "post")
                .order_by("post__label"),
            )
        )
        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(
                "No %(verbose_name)s found matching the query"
                % {"verbose_name": queryset.model._meta.verbose_name}
            )
        return obj


class RedirectPostView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        PostElection = apps.get_model("elections.PostElection")
        post_id = self.kwargs.get("post_id")
        election_id = self.kwargs.get("election_id")
        model = get_object_or_404(
            PostElection, post__ynr_id=post_id, election__slug=election_id
        )
        url = model.get_absolute_url()
        args = self.request.META.get("QUERY_STRING", "")
        if args and self.query_string:
            url = "%s?%s" % (url, args)
        return url


class PostView(NewSlugsRedirectMixin, PostelectionsToPeopleMixin, DetailView):
    template_name = "elections/post_view.html"
    model = apps.get_model("elections.PostElection")

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        queryset = queryset.filter(
            ballot_paper_id=self.kwargs["election"]
        ).select_related("post", "election")

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(
                "No %(verbose_name)s found matching the query"
                % {"verbose_name": queryset.model._meta.verbose_name}
            )
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["election"] = self.object.election
        self.object.people = self.people_for_ballot(self.object)
        return context


class PartyListVew(TemplateView):
    template_name = "elections/party_list_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ballot"] = PostElection.objects.get(
            ballot_paper_id=self.kwargs["election"]
        )

        context["party"] = Party.objects.get(party_id=self.kwargs["party_id"])

        local_party_qs = LocalParty.objects.select_related("parent").filter(
            post_election=context["ballot"], parent=context["party"]
        )

        if local_party_qs.exists():
            context["local_party"] = local_party_qs.get()
            context["party_name"] = context["local_party"].name
        else:
            context["party_name"] = context["party"].party_name

        manifestos = context["party"].manifesto_set.filter(
            election=context["ballot"].election
        )
        if manifestos.exists():
            context["manifesto"] = manifestos.get()

        context["person_posts"] = PersonPost.objects.filter(
            party=context["party"], post_election=context["ballot"]
        ).order_by("list_position")
        return context
