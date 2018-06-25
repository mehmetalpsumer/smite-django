from . import models

from smite_wrapper import client


def update_gods(client):
    gods = client.loop.run_until_complete(client.get_characters())
    for god in gods:


        new_god = models.God()
        new_god.save()
    print()
