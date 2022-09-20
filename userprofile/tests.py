from django.test import TestCase
from .models import UserProfile
from django.contrib.auth.models import User
class UserProfileTestCase(TestCase):
    def setUp(self):
        # print('Creating User')
        self.user1 = User.objects.create_user('Testcaser1', 'test')
        self.user2 = User.objects.create_user('Testcaser2', 'test')
        self.user_profile1 = UserProfile.objects.get(user=self.user1)
        self.user_profile2 = UserProfile.objects.get(user__username=self.user2.username)


    def test_user_profile_existance(self):
        self.assertIsNotNone(self.user_profile2)
        with self.assertRaises(UserProfile.DoesNotExist):
            UserProfile.objects.get(user__username='Noname')
        user_profile3 = UserProfile.objects.filter(user__username='Noname')
        self.assertFalse(user_profile3.exists())


    def test_user_profile_reverse_foreign_key(self):
        self.assertIn('user_profile', dir(self.user1))
        self.assertIn('user_profile', dir(self.user2))

    def test_user_profile_created_on_user_signal(self):
        self.assertNotEqual(self.user_profile1, self.user_profile2)
        self.assertEqual(self.user1.user_profile, self.user_profile1)
        self.assertNotEqual(self.user1.user_profile, self.user_profile2)

    def test_user_profile_on_delete_user(self):
        username3 = 'Testcaser3'
        user3 = User.objects.create_user(username3, 'test')
        user_profile3 = UserProfile.objects.get(user__username=username3)
        self.assertEqual(user3.user_profile, user_profile3)

        user3.delete()
        user_profile3_after_del = UserProfile.objects.filter(user__username=username3)
        self.assertFalse(user_profile3_after_del.exists())
