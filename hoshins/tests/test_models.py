# from django.test import TestCase
#
# from hoshins import models, utils
#
#
# class ObjectModelTestCase(TestCase):
#     fixtures = ['initial.json']
#
#     def setUp(self):
#         self.team = models.Team.objects.first()
#         self.user = models.User.objects.first()
#
#     def test_add_object(self):
#         obj = models.Object.objects.create(belongs_to=self.team, owner=self.user)
#         obj.save()
#
#
# class HoshinModelTestCase(TestCase):
#     fixtures = ['hoshin.json']
#
#     def setUp(self):
#         self.team = models.Team.objects.first()
#         self.user = models.User.objects.first()
#         self.hoshin = models.Hoshin.objects.first()
#
#     def test_add(self):
#         obj = models.Object.objects.create(belongs_to=self.team, owner=self.user)
#         obj.save()
#
#         h = models.Hoshin.objects.create(object_ptr=obj, name='newOne')
#         h.save()
#
#     def test_cascade_deletion(self):
#         sub_object_exists = models.Item.objects.filter(parent=self.hoshin).exists()
#         self.assertTrue(sub_object_exists)
#
#         self.hoshin.delete()
#
#         sub_object_exists = models.Item.objects.filter(parent=self.hoshin).exists()
#         self.assertFalse(sub_object_exists)
#
#
# class ItemModelTestCase(TestCase):
#     fixtures = ['hoshin.json']
#
#     def setUp(self):
#         self.team = models.Team.objects.first()
#         self.user = models.User.objects.first()
#         self.hoshin = models.Hoshin.objects.first()
#         self.item = models.Item.objects.first()
#
#     def test_save_item_user_undefined(self):
#         obj = models.Object.objects.create(belongs_to=self.team, owner=self.user)
#         obj.save()
#
#         nb_items = self.hoshin.nb_items
#         nb_participants = self.hoshin.nb_participants
#
#         item = models.Item.objects.create(object_ptr=obj,
#                                           parent=self.hoshin,
#                                           target='test',
#                                           name='test',
#                                           leader="John John")
#         item.save()
#
#         self.assertNotEqual(nb_items, self.hoshin.nb_items)
#         self.assertEqual(nb_participants, self.hoshin.nb_participants)
#
#     def test_cascade_deletion(self):
#         sub_object_exists = models.ImplementationPriority.objects.filter(parent=self.item).exists()
#         self.assertTrue(sub_object_exists)
#
#         self.item.delete()
#
#         sub_object_exists = models.Item.objects.filter(parent=self.hoshin).exists()
#         self.assertFalse(sub_object_exists)
#
#
# class ImplementationPriorityModelTestCase(TestCase):
#     fixtures = ['hoshin.json']
#
#     def setUp(self):
#         self.team = models.Team.objects.first()
#         self.user = models.User.objects.first()
#         self.hoshin = models.Hoshin.objects.first()
#         self.item = models.Item.objects.first()
#
#     def test_save_implem_user_undefined(self):
#         obj = models.Object.objects.create(belongs_to=self.team, owner=self.user)
#         obj.save()
#         self.assertIsNotNone(obj)
#
#         item = models.ImplementationPriority.objects.create(object_ptr=obj,
#                                                             parent=self.item,
#                                                             target='test',
#                                                             name='test',
#                                                             leader="John John")
#         item.save()
#         self.assertIsNotNone(item)
#
#
# class CommentModelTestCase(TestCase):
#     fixtures = ['hoshin.json']
#
#     def setUp(self):
#         self.team = models.Team.objects.first()
#         self.user = models.User.objects.first()
#         self.hoshin = models.Hoshin.objects.first()
#         self.item = models.Item.objects.first()
#
#     def test_add_comment(self):
#         obj = models.Object.objects.create(belongs_to=self.team, owner=self.user)
#         obj.save()
#         self.assertIsNotNone(obj)
#
#         comment = models.Comment.objects.create(text='y',
#                                                 object_ptr=obj,
#                                                 parent=self.item.object_ptr)
#         comment.save()
#
#         self.assertIsNotNone(comment)
#         self.assertEqual(1, self.hoshin.nb_comments)
#         self.assertEqual(1, self.hoshin.nb_commentators)
#         self.assertEqual(0, self.hoshin.nb_chatty_commentators)
#
#     def test_add_two_comments(self):
#         for i in range(2):
#             obj = models.Object.objects.create(belongs_to=self.team, owner=self.user)
#             obj.save()
#             self.assertIsNotNone(obj)
#
#             comment = models.Comment.objects.create(text='y',
#                                                     object_ptr=obj,
#                                                     parent=self.hoshin.object_ptr)
#             comment.save()
#             self.assertIsNotNone(comment)
#
#         self.assertEqual(2, self.hoshin.nb_comments)
#         self.assertEqual(0, self.hoshin.nb_commentators)
#         self.assertEqual(1, self.hoshin.nb_chatty_commentators)
#
#     def remove_one_comment(self):
#         self.test_add_comment()
#         models.Comment.objects.delete()
#         self.assertEqual(0, self.hoshin.nb_comments)
#         self.assertEqual(0, self.hoshin.nb_commentators)
#
#     def remove_two_comments(self):
#         self.test_add_two_comments()
#         models.Comment.objects.delete()
#         self.assertEqual(0, self.hoshin.nb_comments)
#         self.assertEqual(0, self.hoshin.nb_chatty_commentators)
#
#     def remove_one_comment_cascade(self):
#         self.test_add_comment()
#         models.Item.objects.delete()
#         self.assertFalse(models.Comment.objects.exists())
#         self.assertEqual(0, self.hoshin.nb_comments)
