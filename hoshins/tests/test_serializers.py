# from django.test import TestCase
#
# from hoshins.serializers import *
# from hoshins.models import *
#
# admin = {
#     "username": "admin",
#     "first_name": "Nico",
#     "last_name": "T a",
#     "teams": ["toyota"],
#     "isModerator": True,
#     "isOwner": True,
#     "id": "1",
#     "token": ""
# }
#
#
# team = {
#     'name': 'toyota'
# }
#
#
# class HoshinSerializerTestCase(TestCase):
#     fixtures = ['testdata.json']
#
#     def setUp(self):
#         self.hoshin_data = {
#             "leader": "Nicolas T a",
#             "name": "t",
#             "color": "#ffffff",
#             "belongs_to": team,
#             "owner": admin
#         }
#
#     def test_hoshin_saving_ok(self):
#         serializer = HoshinSerializer(data=self.hoshin_data)
#         self.assertEqual(serializer.is_valid(raise_exception=True), True)
#
#         self.hoshin = serializer.save()
#         self.assertEqual(type(self.hoshin).__name__, 'Hoshin')
#
#     def test_hoshin_saving_nok_owner(self):
#         miss_owner = {
#             "name": "t",
#             "color": "#ffffff",
#             "belongs_to": team,
#         }
#
#         wrong_owner = {
#             "owner": {
#                 "username": "adn123",
#                 "first_name": "",
#                 "last_name": "",
#                 "teams": ["toyota"],
#                 "isModerator": True,
#                 "isOwner": True,
#                 "id": "21342",
#                 "token": ""
#             },
#             "name": "t",
#             "color": "#ffffff",
#             "belongs_to": team,
#         }
#
#         serializer = HoshinSerializer(data=miss_owner)
#         self.assertEqual(serializer.is_valid(), False)
#
#     def test_hoshin_saving_nok_color(self):
#         wrong_colors = ["#fffffff", "#fffffg", "fffff2"]
#
#         miss_color = {
#             "owner": admin,
#             "name": "t",
#             "belongs_to": team,
#         }
#
#         serializer = HoshinSerializer(data=miss_color)
#         self.assertEqual(serializer.is_valid(), False)
#
#         for color in wrong_colors:
#             miss_color['color'] = color
#             serializer = HoshinSerializer(data=miss_color)
#             self.assertEqual(serializer.is_valid(), False)
#
#
# class ItemSerializerTestCase(TestCase):
#     fixtures = ['testdata.json']
#
#     def setUp(self):
#         hoshin = Hoshin.objects.all()[0]
#         self.item_data = {
#             "leader": "Nicolas T a",
#             "name": "t",
#             "target": "hop",
#             "belongs_to": team,
#             "owner": admin,
#             "parent": hoshin.id
#         }
#
#     def test_item_saving_ok(self):
#         serializer = ItemSerializer(data=self.item_data)
#         self.assertEqual(serializer.is_valid(raise_exception=True), True)
#
#
# class PrioritySerializerTestCase(TestCase):
#     fixtures = ['testdata_with_items.json']
#
#     def setUp(self):
#         item = Item.objects.all()[0]
#         self.priority_data = {
#             "leader": "Nicolas T a",
#             "name": "t",
#             "target": "hop",
#             "belongs_to": team,
#             "owner": admin,
#             "parent": item.id
#         }
#
#     def test_priority_saving_ok(self):
#         serializer = ImplementationPrioritySerializer(data=self.priority_data)
#         self.assertEqual(serializer.is_valid(raise_exception=True), True)
#
#
# class CommentTestCase(TestCase):
#     fixtures = ['testdata.json']
#
#     def setUp(self):
#         hoshin = Hoshin.objects.all()[0]
#         self.comment_data = {
#             "text": "t",
#             "belongs_to": team,
#             "owner": admin,
#             "parent": hoshin.id
#         }
#
#     def test_comment_saving_ok(self):
#         serializer = CommentSerializer(data=self.comment_data)
#         self.assertEqual(serializer.is_valid(raise_exception=True), True)
#
# # class IndicatorsAddTestCase(TestCase):
# #     fixtures = ['testdata.json']
# #
# #     def setUp(self):
# #         self.id_hoshin = 5
# #         self.hoshin = Hoshin.objects.get(id=self.id_hoshin)
# #
# #     def test_add_items(self):
# #         args = {
# #             'owner': admin,
# #             'leader': admin,
# #             'name': 'first item',
# #             'target': 'test',
# #             'belongs_to': team,
# #             'parent': self.hoshin.object_ptr.pk
# #         }
# #
# #         self.assertEqual(self.hoshin.nb_items, 0)
# #         self.assertEqual(self.hoshin.nb_participants, 0)
# #
# #         serializer = ItemSerializer(data=args)
# #         serializer.is_valid()
# #         serializer.save()
# #         hoshin = Hoshin.objects.get(id=self.id_hoshin)
# #
# #         self.assertEqual(hoshin.nb_items, 1)
# #         self.assertEqual(hoshin.nb_participants, 1)
# #
# #         serializer = ItemSerializer(data=args)
# #         serializer.is_valid()
# #         serializer.save()
# #         hoshin = Hoshin.objects.get(id=self.id_hoshin)
# #
# #         self.assertEqual(hoshin.nb_items, 2)
# #         self.assertEqual(hoshin.nb_participants, 1)
# #
# #     def test_add_comments(self):
# #         args = {
# #             'owner': admin,
# #             'text': 'first comment',
# #             'belongs_to': team,
# #             'parent': self.hoshin.object_ptr.pk
# #         }
# #
# #         self.assertEqual(self.hoshin.nb_comments, 0)
# #         self.assertEqual(self.hoshin.nb_participants, 0)
# #
# #         serializer = CommentSerializer(data=args)
# #         serializer.is_valid()
# #         serializer.save()
# #         hoshin = Hoshin.objects.get(id=self.id_hoshin)
# #
# #         self.assertEqual(hoshin.nb_comments, 1)
# #         self.assertEqual(hoshin.nb_participants, 1)
# #
# #         serializer = CommentSerializer(data=args)
# #         serializer.is_valid()
# #         serializer.save()
# #         hoshin = Hoshin.objects.get(id=self.id_hoshin)
# #
# #         self.assertEqual(hoshin.nb_comments, 2)
# #         self.assertEqual(hoshin.nb_participants, 1)
# #
# #
# # class IndicatorsRemoveTestCase(TestCase):
# #     fixtures = ['testdata_with_items.json']
# #
# #     def setUp(self):
# #         self.id_hoshin = 8
# #         self.hoshin = Hoshin.objects.get(id=self.id_hoshin)
# #         self.items = Item.objects.all()
# #         self.comments = Comment.objects.all()
# #
# #     def test_remove_item(self):
# #         self.comments[0].delete()
# #         self.comments[0].delete()
# #
# #         self.assertEqual(self.hoshin.nb_items, 2)
# #         self.assertEqual(self.hoshin.nb_participants, 1)
# #
# #         self.items[0].delete()
# #         hoshin = Hoshin.objects.get(id=self.id_hoshin)
# #
# #         self.assertEqual(hoshin.nb_items, 1)
# #         self.assertEqual(hoshin.nb_participants, 1)
# #
# #         self.items[0].delete()
# #         hoshin = Hoshin.objects.get(id=self.id_hoshin)
# #
# #         self.assertEqual(hoshin.nb_items, 0)
# #         self.assertEqual(hoshin.nb_participants, 0)
# #
# #     def test_remove_comment(self):
# #         self.items[0].delete()
# #         self.items[0].delete()
# #
# #         self.assertEqual(self.hoshin.nb_comments, 2)
# #         self.assertEqual(self.hoshin.nb_participants, 1)
# #
# #         self.comments[0].delete()
# #         hoshin = Hoshin.objects.get(id=self.id_hoshin)
# #
# #         self.assertEqual(hoshin.nb_comments, 1)
# #         self.assertEqual(hoshin.nb_participants, 1)
# #
# #         self.comments[0].delete()
# #         hoshin = Hoshin.objects.get(id=self.id_hoshin)
# #
# #         self.assertEqual(hoshin.nb_comments, 0)
# #         self.assertEqual(hoshin.nb_participants, 0)
#
