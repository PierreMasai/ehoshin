import django
django.setup()

from hoshins.models import *


for h in Hoshin.objects.all():

    nb1 = 0
    nb2 = 0
    nb3 = 0

    for user in User.objects.all():
        nb_cmt = h.get_nb_cmt(user)
        nb3 += nb_cmt
        if nb_cmt > 1:
            nb2 += 1
        elif nb_cmt == 1:
            nb1 += 1

    h.nb_chatty_commentators = nb2
    h.nb_commentators = nb1
    h.nb_comments = nb3
    h.save()