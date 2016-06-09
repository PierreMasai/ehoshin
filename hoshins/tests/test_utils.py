# from django.test import TestCase
#
# from hoshins import models, utils
#
#
# class UtilsTestCase(TestCase):
#     fixtures = ['testdata_with_items.json']
#
#     def setUp(self):
#         self.ip = models.ImplementationPriority.objects.all()[0]
#
#     def test_get_followers(self):
#         users_list, _ = utils.get_infos_to_notify(self.ip)
#
#         self.assertEqual(len(users_list), 2)
