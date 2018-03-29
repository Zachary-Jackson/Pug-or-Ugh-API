from django.contrib.auth.models import User
from django.test import TestCase


from rest_framework.test import APIRequestFactory, force_authenticate


from .models import Dog, UserPref
from .views import RetrieveUpdateUserPrefView


class PugOrUghViewsTests(TestCase):
    """This tests the views for the pugorugh app"""
    def setUp(self):
        """This creates a User and some Dogs for testing"""
        self.user = User.objects.create_user(
            username='tester',
            email='test@test123.com',
            password='something secret'
        )

        self.dog = Dog.objects.create(
            name='Francesca',
            image_filename='pugorugh/static/images/dogs/1.jpg',
            breed='Labrador',
            age=72,
            gender='f',
            size='l'
        )

    def test_RetrieveUpdateUserPrefView(self):
        factory = APIRequestFactory()
        request = factory.get('/api/user/preferences/')
        force_authenticate(request, user=self.user)
        view = RetrieveUpdateUserPrefView.as_view()

        # Their should be no UserPref in the database
        assert len(UserPref.objects.all()) == 0

        response = view(request)
        self.assertEqual(response.status_code, 200)
        # The view should have created a UserPref for the User
        self.assertEqual(len(UserPref.objects.all()), 1)
        self.assertEqual(
            response.data,
            {'age': 'b,y,a,s', 'gender': 'm,f', 'size': 's,m,l,xl'})

        # This section tests a PUT request
        request = factory.put(
            '/api/user/preferences/',
            {'age': 'b,y', 'gender': 'f', 'size': 's,m'})
        force_authenticate(request, user=self.user)
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data,
            {'age': 'b,y', 'gender': 'f', 'size': 's,m'})

        # The view should not have created a second UserPref object
        self.assertEqual(len(UserPref.objects.all()), 1)

        preferences = UserPref.objects.get(id=1)
        self.assertEqual(preferences.age, 'b,y')
        self.assertEqual(preferences.gender, 'f')
        self.assertEqual(preferences.size, 's,m')
