import django_filters

# TODO: refactor into core.utils
from elections.filters import DSLinkWidget
from ppc_2024.models import PPCPerson


class PPCFilter(django_filters.FilterSet):
    region = django_filters.AllValuesFilter(
        widget=DSLinkWidget,
        field_name="region_name",
        lookup_expr="contains",
        label="Region",
    )
    party_name = django_filters.AllValuesFilter(
        widget=DSLinkWidget,
        field_name="party__party_name",
        lookup_expr="contains",
        label="Party Name",
    )

    class Meta:
        model = PPCPerson
        fields = ["region"]
