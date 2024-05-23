from datetime import date
from random import randint

from elections.models import Election, Post, PostElection, VotingSystem
from people.dummy_models import DummyCandidacy, DummyPerson


class DummyPostElection(PostElection):
    party_ballot_count = 5
    display_as_party_list = False
    locked = True
    voting_system_id = "FPTP"
    ballot_paper_id = "local.faketown.made-up-ward.2024-07-04"
    cancelled = False
    show_polling_card = True
    contested = True
    requires_voter_id = "EA-2022"
    registration_deadline = date(2024, 6, 13)

    election = Election(
        name="Llantalbot local election",
        election_date=date(2024, 7, 4),
        any_non_by_elections=True,
        slug="local.faketown.2024-07-04",
        voting_system=VotingSystem(slug="FPTP"),
        current=True,
    )

    post = Post(label="Made-Up-Ward")
    post.territory = "ENG"
    pk = randint(1, 100000)

    class Meta:
        proxy = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ballot_paper_id = "local.faketown.made-up-ward.2024-07-04"
        self.election.get_absolute_url = self.election_get_absolute_url

    def election_get_absolute_url(self):
        return ""

    def people(self):
        return [
            DummyCandidacy(
                person=DummyPerson(
                    name="Jimmy Jordan", favourite_biscuit="Jaffa cake"
                ),
                election=self.election,
                party_name="Yellow Party",
                deselected=True,
                deselected_source="www.google.com",
            ),
            DummyCandidacy(
                person=DummyPerson(
                    name="Rhuanedd Llewelyn",
                    favourite_biscuit="Chocolate digestive",
                ),
                election=self.election,
                party_name="Independent",
            ),
            DummyCandidacy(
                person=DummyPerson(
                    name="Ryan Evans", favourite_biscuit="Party ring"
                ),
                election=self.election,
                party_name="Lilac Party",
            ),
            DummyCandidacy(
                person=DummyPerson(
                    name="Sarah Jarman", favourite_biscuit="Hobnob"
                ),
                election=self.election,
                party_name="Purple Party",
            ),
            DummyCandidacy(
                person=DummyPerson(
                    name="Sofia Williamson",
                    favourite_biscuit="Custard cream",
                ),
                election=self.election,
                party_name="Independent",
            ),
        ]
