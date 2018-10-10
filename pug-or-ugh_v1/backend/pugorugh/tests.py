from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase


from rest_framework.test import APIRequestFactory, force_authenticate


from .models import Dog, UserDog, UserPref
from . import views


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

        self.user_pref = UserPref.objects.create(
            user=self.user,
            age='b,y,a,s',
            gender='m,f',
            size='s,m,l,xl'
        )

        UserDog.objects.create(
            user=self.user,
            dog=self.dog,
            status='u'
        )

    def test_UserRegisterView(self):
        """Ensures users can create profiles and checks for valid passwords"""
        factory = APIRequestFactory()
        request = factory.post(
            reverse('register-user'),
            {'password': 'test_password', 'username': 'seconduser'})
        view = views.UserRegisterView.as_view()

        response = view(request)

        # Their should now be a new user in addition to SetUp
        self.assertEqual(len(UserPref.objects.all()), 2)
        self.assertEqual(response.status_code, 201)

        # This post should be bad because of an invalid password
        request = factory.post(
            reverse('register-user'),
            {'password': 'test password', 'username': 'seconduser'})
        view = views.UserRegisterView.as_view()

        response = view(request)
        self.assertEqual(response.status_code, 400)

    def test_RetrieveDogView(self):
        """Checks to see if the correct Dog is returned"""
        factory = APIRequestFactory()

        # -1 dog_pk should start us with first dog.
        # the following should be using reverse

        request = factory.get(
            reverse(
                'dog_detail',
                kwargs={'dog_pk': '-1', 'status_pk': 'undecided'}))

        force_authenticate(request, user=self.user)
        view = views.RetrieveDogView.as_view()

        response = view(request, dog_pk='-1', status_pk='undecided')

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            response.data,
            {'name': 'Francesca', 'image_filename':
                'pugorugh/static/images/dogs/1.jpg', 'breed': 'Labrador',
                'age': 72, 'gender': 'f', 'size': 'l', 'id': 1})

        # This second test uses the value we retured for 'id' (1) and
        # tries to go to the next dog, but there is not one
        request = factory.get(
            reverse(
                'dog_detail',
                kwargs={'dog_pk': '1', 'status_pk': 'undecided'}))

        force_authenticate(request, user=self.user)
        view = views.RetrieveDogView.as_view()

        response = view(request, dog_pk='1', status_pk='undecided')

        self.assertEqual(response.status_code, 404)

        # This checks to see if we get a 404 if no dogs are found
        request = factory.get(
            reverse(
                'dog_detail',
                kwargs={'dog_pk': '-1', 'status_pk': 'disliked'}))

        force_authenticate(request, user=self.user)
        view = views.RetrieveDogView.as_view()

        response = view(request, dog_pk='-1', status_pk='disliked')

        self.assertEqual(response.status_code, 404)

    def test_UpdateUserDogView(self):
        """Makes sure UpdateUserDogView works properly"""
        factory = APIRequestFactory()

        request = factory.put(
            reverse(
                'UserDog_update',
                kwargs={'dog_pk': 1, 'status_pk': 'liked'}))

        force_authenticate(request, user=self.user)
        view = views.UpdateUserDogView.as_view()

        response = view(request, dog_pk='1', status_pk='liked')

        self.assertEqual(response.status_code, 200)

        # We should get the dog we PUT too back
        self.assertEqual(
            response.data,
            {'name': 'Francesca', 'image_filename':
                'pugorugh/static/images/dogs/1.jpg', 'breed': 'Labrador',
                'age': 72, 'gender': 'f', 'size': 'l', 'id': 1})

        self.assertEqual(UserDog.objects.get(pk=1).status, 'l')

        # Tests a bad PUT Request
        request = factory.put(
            reverse(
                'UserDog_update',
                kwargs={'dog_pk': 100, 'status_pk': 'liked'}))

        force_authenticate(request, user=self.user)
        view = views.UpdateUserDogView.as_view()

        response = view(request, dog_pk='100', status_pk='liked')

        self.assertEqual(response.status_code, 404)

    def test_RetrieveUpdateUserPrefView(self):
        """Makes sure UserPref can be returned and updated"""
        factory = APIRequestFactory()

        # This sections tests a GET request
        request = factory.get(reverse('user_pref_detail'))
        force_authenticate(request, user=self.user)
        view = views.RetrieveUpdateUserPrefView.as_view()

        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data,
            {'age': 'b,y,a,s', 'gender': 'm,f', 'size': 's,m,l,xl'})

        # This section tests a PUT request
        request = factory.put(
            reverse('user_pref_detail'),
            {'age': 'b,y', 'gender': 'f', 'size': 's,m'})
        force_authenticate(request, user=self.user)
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data,
            {'age': 'b,y', 'gender': 'f', 'size': 's,m'})

        preferences = UserPref.objects.get(id=1)
        self.assertEqual(preferences.age, 'b,y')
        self.assertEqual(preferences.gender, 'f')
        self.assertEqual(preferences.size, 's,m')
