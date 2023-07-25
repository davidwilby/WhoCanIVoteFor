from urllib.parse import urlencode
from django.db.models import BLANK_CHOICE_DASH
from django.utils.encoding import force_str
from django.utils.safestring import mark_safe
from django_filters.widgets import LinkWidget

import django_filters

from parties.models import Party


def party_register_choices():
    return [
        ("GB", "Great Britain"),
        ("NI", "Northern Ireland"),
    ]


def party_status_choices():
    return [("Registered", "Registered"), ("Deregistered", "Deregistered")]


class DSLinkWidget(LinkWidget):
    """
    The LinkWidget doesn't allow iterating over choices in the template layer
    to change the HTML wrapping the widget.

    This breaks the way that Django *should* work, so we have to subclass
    and alter the HTML in Python :/

    https://github.com/carltongibson/django-filter/issues/880
    """

    def render(self, name, value, attrs=None, choices=(), renderer=None):
        if not hasattr(self, "data"):
            self.data = {}
        if value is None:
            value = ""
        self.build_attrs(self.attrs, extra_attrs=attrs)
        output = []
        options = self.render_options(choices, [value], name)
        if options:
            output.append(options)
        # output.append('</ul>')
        return mark_safe("\n".join(output))

    def render_option(self, name, selected_choices, option_value, option_label):
        option_value = force_str(option_value)
        if option_label == BLANK_CHOICE_DASH[0][1]:
            option_label = "All"
        data = self.data.copy()
        data[name] = option_value
        selected = data == self.data or option_value in selected_choices
        try:
            url = data.urlencode()
        except AttributeError:
            url = urlencode(data)
        return self.option_string() % {
            "attrs": selected and ' aria-current="true"' or "",
            "query_string": url,
            "label": force_str(option_label),
        }


class PartyRegisterFilter(django_filters.FilterSet):
    def party_register_filter(self, queryset, name, value):
        return queryset.filter(register=value)

    def party_status_filter(self, queryset, name, value):
        return queryset.filter(status=value)

    def party_nations_filter(self, queryset, name, value):
        return queryset.filter(nations__contains=[value])

    register = django_filters.ChoiceFilter(
        widget=DSLinkWidget,
        method="party_register_filter",
        choices=party_register_choices,
        label="Party Register",
    )

    status = django_filters.ChoiceFilter(
        widget=DSLinkWidget,
        method="party_status_filter",
        choices=party_status_choices,
        label="Party Status",
    )

    nations = django_filters.ChoiceFilter(
        widget=DSLinkWidget,
        method="party_nations_filter",
        choices=[("ENG", "England"), ("WAL", "Wales"), ("SCO", "Scotland")],
        label="Nation",
    )

    class Meta:
        model = Party
        fields = ["register", "status", "nations"]

    @property
    def shortcuts(self):
        """
        Returns filter shorcuts
        """
        shortcut_list = [
            {
                "name": "gb_parties",
                "label": "Registered in Great Britain",
                "query": {"register": ["GB"], "status": ["Registered"]},
            },
            {
                "name": "ni_parties",
                "label": "Registered in Northern Ireland",
                "query": {"register": ["NI"], "status": ["Registered"]},
            },
            {
                "name": "gb_dereg_parties",
                "label": "Deregistered in Great Britain",
                "query": {"register": ["GB"], "status": ["Deregistered"]},
            },
            {
                "name": "ni_dereg_parties",
                "label": "Deregistered in Northern Ireland",
                "query": {"register": ["NI"], "status": ["Deregistered"]},
            },
        ]

        query = dict(self.request.GET)
        shortcuts = {"list": shortcut_list}
        for shortcut in shortcuts["list"]:
            shortcut["querystring"] = urlencode(shortcut["query"], doseq=True)
            if shortcut["query"] == query:
                shortcut["active"] = True
                shortcuts["active"] = shortcut
        return shortcuts
