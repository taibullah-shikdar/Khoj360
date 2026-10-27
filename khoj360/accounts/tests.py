from django.test import TestCase

# Create your tests here.


from django.contrib.auth.models import User
from django.http import Http404
from django.test import RequestFactory

from .models import Profile, VolunteerApplication, compatible_blood_groups, find_available_donors
from .views import toggle_availability, withdraw_application


class DonorMatchingTests(TestCase):
    def make_profile(self, username, blood_group, area="Dhanmondi", **flags):
        user = User.objects.create_user(username=username, password="pass12345")
        return Profile.objects.create(user=user, full_name=username, blood_group=blood_group, area=area, **flags)

    def test_compatible_blood_groups(self):
        self.assertEqual(compatible_blood_groups("O-"), ["O-"])
        self.assertEqual(len(compatible_blood_groups("AB+")), 8)
        self.assertEqual(compatible_blood_groups("X"), [])

    def test_find_available_donors(self):
        donor = self.make_profile("donor", "O-", is_donor=True)
        self.make_profile("busy", "O-", is_donor=True, is_available=False)
        self.make_profile("not_donor", "O-")
        self.make_profile("far", "O-", area="Mirpur", is_donor=True)
        self.assertEqual(list(find_available_donors("A+", "dhanmondi")), [donor])


class ProfileActionTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="user", password="pass12345")

    def post(self, view, *args):
        request = self.factory.post("/")
        request.user = self.user
        return view(request, *args)

    def test_toggle_availability(self):
        self.post(toggle_availability)
        self.assertFalse(Profile.objects.get(user=self.user).is_available)

    def test_withdraw_only_pending_application(self):
        pending = VolunteerApplication.objects.create(user=self.user, role=VolunteerApplication.ROLE_DONOR)
        self.post(withdraw_application, pending.pk)
        self.assertFalse(VolunteerApplication.objects.filter(pk=pending.pk).exists())
        approved = VolunteerApplication.objects.create(
            user=self.user, role=VolunteerApplication.ROLE_DONOR, status=VolunteerApplication.STATUS_APPROVED
        )
        with self.assertRaises(Http404):
            self.post(withdraw_application, approved.pk)
