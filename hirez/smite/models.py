from django.db import models
from django.utils.text import slugify


class Ability(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.TextField()
    icon_url = models.URLField()
    description = models.TextField()

    def __str__(self):
        return self.name

    def get_dict(self):
        return {
            'name': self.name,
            'img': self.icon_url,
            'desc': self.description
        }


class God(models.Model):
    # General info
    id = models.PositiveIntegerField(primary_key=True)
    name = models.TextField()
    lore = models.TextField()
    pantheon = models.TextField()
    role = models.TextField()
    title = models.TextField()
    type = models.TextField()
    card_url = models.URLField()
    icon_url = models.URLField()
    latest_god = models.BooleanField()

    # Utility tats
    hp = models.FloatField()
    mp = models.FloatField()
    hp5 = models.FloatField()
    mp5 = models.FloatField()
    hp_pl = models.FloatField()
    mp_pl = models.FloatField()
    hp5_pl = models.FloatField()
    mp5_pl = models.FloatField()
    speed = models.PositiveIntegerField()

    # Defence stats
    mag_protection = models.FloatField()
    mag_protection_pl = models.FloatField()
    phy_protection = models.FloatField()
    phy_protection_pl = models.FloatField()

    # Offence stats
    mag_power = models.FloatField()
    mag_power_pl = models.FloatField()
    phy_power = models.FloatField()
    phy_power_pl = models.FloatField()
    atk_speed = models.FloatField()
    atk_speed_pl = models.FloatField()

    # Abilities
    ability_passive = models.ForeignKey(Ability, on_delete=models.CASCADE, related_name='ability_passive')
    ability_1 = models.ForeignKey(Ability, on_delete=models.CASCADE, related_name='ability_1')
    ability_2 = models.ForeignKey(Ability, on_delete=models.CASCADE, related_name='ability_2')
    ability_3 = models.ForeignKey(Ability, on_delete=models.CASCADE, related_name='ability_3')
    ability_4 = models.ForeignKey(Ability, on_delete=models.CASCADE, related_name='ability_4')

    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(God, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Item(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.TextField()
    tier = models.IntegerField()
    price = models.IntegerField()
    root_item_id = models.PositiveIntegerField()
    short_description = models.TextField()
    description = models.TextField(null=True, blank=True)
    starting_item = models.BooleanField()
    type = models.TextField()
    icon_id = models.PositiveIntegerField()
    icon_url = models.URLField()

    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Item, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class ItemStat(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    stat = models.TextField()
    value = models.TextField()

    def __str__(self):
        return "{} {}".format(self.value, self.stat)


class ItemDescription(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    aura = models.TextField()

    def __str__(self):
        return "AURA for {}".format(self.item_id.name)


class Player(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    avatar_url = models.URLField()
    name = models.TextField()
    level = models.PositiveIntegerField()
    mastery_level = models.IntegerField()
    clan_id = models.PositiveIntegerField(null=True, blank=True)
    clan_name = models.TextField(null=True, blank=True)
    total_worshippers = models.IntegerField()
    wins = models.IntegerField()
    loses = models.IntegerField()
    leaves = models.IntegerField()
    created = models.DateField(blank=True, null=True)

    def __str__(self):
        return "[{}]{}".format(self.clan_name, self.name)


class Match(models.Model):
    pass


class MatchPlayer(models.Model):
    pass
