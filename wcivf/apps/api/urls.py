from api import views
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()

router.register(
    r"candidates_for_postcode",
    views.CandidatesAndElectionsForPostcodeViewSet,
    basename="candidates-for-postcode",
)
router.register(
    r"candidates_for_ballots",
    views.CandidatesAndElectionsForBallots,
    basename="candidates-for-ballots",
)


urlpatterns = [
    path(r"", include(router.urls)),
    path(
        "last-updated-timestamps/",
        views.LastUpdatedView.as_view(),
        name="last-updated-timestamps",
    ),
]
