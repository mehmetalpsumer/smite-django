from datetime import datetime


class SmiteObject:
    """Represents a generic HiRezPy object

    Attributes
    ----------
    ret_msg : str or None
        The message returned from the API request
    as_json: dict or list
        The request as JSON, if you prefer

    """
    def __init__(self, **kwargs):
        self.ret_msg = kwargs.get('ret_msg', None)
        self.as_json = kwargs


class Limits(SmiteObject):
    """Represents developer usage limits.

    This is a sub-class of :class:`HrpObject`.

    Attributes
    ----------
    total_requests : int
        The total requests that have been made to the API today
    session_cap : int
        The total amount of sessions permitted today
    active_sessions : int
        The total amount of active sessions
    request_limit : int
        The total amount of requests permitted today
    total_sessions : int
        The total sessions that have been created today
    concurrent_sessions : int
        The amount of concurrent sessions permitted today
    session_time_limit : int
        The amount of time sessions last for, in minutes

    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.total_requests = kwargs.get('Total_Requests_Today')
        self.session_cap = kwargs.get('Session_Cap')
        self.active_sessions = kwargs.get('Active_Sessions')
        self.request_limit = kwargs.get('Request_Limit_Daily')
        self.total_sessions = kwargs.get('Total_Sessions_Today')
        self.concurrent_sessions = kwargs.get('Concurrent_Sessions')
        self.session_time_limit = kwargs.get('Session_Time_Limit')

    @property
    def sessions_left(self):
        """Returns the amount of sessions left that can be created today as int"""
        rem = self.session_cap - self.total_sessions
        if rem < 0:
            rem = 0
        return rem

    @property
    def requests_left(self):
        """Returns the amount of requests left that can be made today as int"""
        rem = self.request_limit - self.total_requests
        if rem < 0:
            rem = 0
        return rem


class Match(SmiteObject):
    """Represents an eSports match.

    This is a sub-class of :class:`HrpObject`.

    Attributes
    ----------
    id : int
        The match ID. This is unique, and will always be different to another match.
    number : int
        The match number
    status : str
        The status of the match
    region : str
        The region of the match
    tournament_name : str
        The name of the tournament that the match is involved in
    map_instance_id : int
        The map instance ID
    date : datetime or str
        The date and time of the match. Only returns a str if the date and time can't be parsed
        correctly by datetime.strptime, which should not happen
    away_team_id : int
        The ID of the away team
    away_team_name : str
        The name of the away team
    away_team_tag : str
        The clan tag of the away team
    home_team_id : int
        The ID of the home team
    home_team_name : str
        The name of the home team
    home_team_tag : str
        The clan tag of the home team

    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = int(kwargs.get('matchup_id'))
        self.number = int(kwargs.get('match_number'))
        self.status = kwargs.get('match_status')
        self.region = kwargs.get('region')
        self.tournament = kwargs.get('tournament_name')
        self.map_instance_id = int(kwargs.get('map_instance_id'))

        date = kwargs.get('match_date')
        try:
            date = datetime.strptime(date, '%-m/%-d/%Y %-I:%M:%S %p')
        except ValueError:  # couldn't parse date and time
            print("Could not parse date and timestamp in data, returning as string")
        self.date = date

        self.away_team_id = int(kwargs.get('away_team_clan_id'))
        self.home_team_id = int(kwargs.get('home_team_clan_id'))
        self.away_team_name = kwargs.get('away_team_name')
        self.home_team_name = kwargs.get('home_team_name')
        self.away_team_tag = kwargs.get('away_team_tagname')
        self.home_team_tag = kwargs.get('home_team_tagname')

    def __str__(self):
        return "<Match {}/{}/{}>".format(self.id, self.home_team_name, self.away_team_name)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id


class Player(SmiteObject):
    """Represents a player.

    This is a sub-class of :class:`HrpObject`.

    Attributes
    ----------
    id : int
        The player's account ID. This is the ID of a player's
        Hi-Rez account
    player_id : int
        The player's ID, based on the game that you are checking
        against
    avatar_url : str
        The player's avatar image URL. Could be an empty string
        if the user is using the default avatar.
    username : str
        The player's username

    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = int(kwargs.get('Id'))
        self.avatar_url = kwargs.get('Avatar_URL')
        self.created_date = kwargs.get('Created_Datetime')
        self.last_login_date = kwargs.get('Last_Login_Datetime')
        self.wins = kwargs.get('Wins')
        self.losses = kwargs.get('Losses')
        self.leaves = kwargs.get('Leaves')
        self.level = kwargs.get('Level')
        self.status = kwargs.get('Personal_Status_Message')
        self.name = kwargs.get('Name')
        self.username = self.name[self.name.index(']')+1:] # Remove clan tag
        self.mastery_level = kwargs.get('masterylevel')

    def __str__(self):
        return "<Player {}>".format(self.id)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id


class Rank(SmiteObject):
    """Represents a character rank.

    This is a sub-class of :class:`HrpObject`.

    Attributes
    ----------
    id : int
        The character's ID
    player_id : int
        The player's ID, based on the game that you are checking
        against
    name : str
        The character's name
    assists : int
        The amount of assists made with this character
    deaths : int
        The amount of deaths made with this character
    kills : int
        The amount of kills made with this character
    losses : int
        The amount of losses made with this character
    minion_kills :  int
        The amount of minion kills made with this character
    rank : int
        The rank gained with this character
    wins : int
        The amount of wins made with this character
    xp : int
        The amount of XP gained with this character. For Smite, this
        will return the amount of worshippers. For Paladins, this will
        be the amount of experience.

    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = int(kwargs.get('god_id'))
        self.player_id = int(kwargs.get('player_id'))
        self.name = kwargs.get('god')
        self.assists = int(kwargs.get('Assists'))
        self.deaths = int(kwargs.get('Deaths'))
        self.kills = int(kwargs.get('Kills'))
        self.losses = int(kwargs.get('Losses'))
        self.minion_kills = int(kwargs.get('MinionKills'))
        self.rank = int(kwargs.get('Rank'))
        self.wins = int(kwargs.get('Wins'))
        self.xp = int(kwargs.get('Worshippers'))

    def __str__(self):
        return "<Rank {}/{}>".format(self.player_id, self.name)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id


class Character(SmiteObject):
    """Represents a character.

    This is a sub-class of :class:`HrpObject`.

    Attributes
    ----------
    id : int
        The character's ID
    health : int
        The character's health
    name : str
        The character's name
    pantheon : str
        The character's pantheon
    speed : int
        The character's speed
    title : str
        The character's title
    roles : str
        The character's roles

    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = kwargs.get('id')
        self.health = kwargs.get('Health')
        self.name = kwargs.get('Name')
        self.pantheon = kwargs.get('Pantheon')
        self.speed = kwargs.get('Speed')
        self.title = kwargs.get('Title')
        self.roles = kwargs.get('Roles')

    def __str__(self):
        return "<Character {}/{}>".format(self.id, self.name)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id


class God(Character):
    """Represents a god in Smite.

    This is a sub-class of :class:`Character`.

    Attributes
    ----------
    abilities : list
        List of GodAbility objects representing the god's abilities
    attack_speed : int
        The attack speed of the god
    attack_speed_per_level : int
        The attack speed per level gained
    cons : str
        The cons of the god
    hp5_per_level : int
        The HP5 per level gained
    health_per_five : int
        The god's health per five
    health_per_level : int
        The god's health per level
    lore : str
        The god's lore
    mp5_per_level : int
        The MP5 per level gained
    magic_protection : int
        The god's magic protection
    magic_protection_per_level : int
        The god's magic protection per level gained
    magical_power : int
        The god's magical power
    magical_power_per_level : int
        The god's magical power per level gained
    mana : int
        The god's mana
    mana_per_five : int
        The god's mana per five
    mana_per_level : int
        The god's mana per level
    physical_power : int
        The god's physical power
    physical_power_per_level : int
        The god's physical power per level
    physical_protection : int
        The god's physical protection
    physical_protection_per_level : int
        The god's physical protection per level
    pros : str
        The god's pros
    type : str
        The god's type
    latest : bool
        Indicates if the god was recently added to the game
    basic_attack : GodAbility
        The god's basic attack
    god_icon_url : str
        The URL of the god's icon
    god_card_url : str
        The URL of the god's card

    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.attack_speed = kwargs.get('AttackSpeed')
        self.attack_speed_per_level = kwargs.get('AttackSpeedPerLevel')
        self.cons = kwargs.get('Cons')
        self.hp5_per_level = kwargs.get('HP5PerLevel')
        self.health_per_five = kwargs.get('HealthPerFive')
        self.health_per_level = kwargs.get('HealthPerLevel')
        self.lore = kwargs.get('Lore')
        self.mp5_per_level = kwargs.get('MP5PerLevel')
        self.magic_protection = kwargs.get('MagicProtection')
        self.magic_protection_per_level = kwargs.get('MagicProtectionPerLevel')
        self.magical_power = kwargs.get('MagicalPower')
        self.magical_power_per_level = kwargs.get('MagicalPowerPerLevel')
        self.mana = kwargs.get('Mana')
        self.mana_per_five = kwargs.get('ManaPerFive')
        self.mana_per_level = kwargs.get('ManaPerLevel')
        self.physical_power = kwargs.get('PhysicalPower')
        self.physical_power_per_level = kwargs.get('PhysicalPowerPerLevel')
        self.physical_protection = kwargs.get('PhysicalProtection')
        self.physical_protection_per_level = kwargs.get('PhysicalProtectionPerLevel')
        self.pros = kwargs.get('Pros')
        self.type = kwargs.get('Type')
        self.god_icon_url = kwargs.get('godIcon_URL')
        self.god_card_url = kwargs.get('godCard_URL')


class Ability:
    """Represents a character's ability.

    Parameters
    ----------
    id : int
        The ID of the ability
    name : str
        The name of the ability
    url : str
        The URL of the ability image

    """
    def __init__(self, **kwargs):
        self.id = kwargs.get('Id')
        self.name = kwargs.get('Summary')
        self.url = kwargs.get('URL')

    def __str__(self):
        return "<Ability {}/{}>".format(self.id, self.name)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id


class GodAbility(Ability):
    """Represents a god's ability in Smite.

    This is a sub-class of :class:`Ability`.

    Parameters
    ----------
    type : str
        The type of ability
    affects : str
        Who the ability affects
    damage : str
        What type of damage the ability does. If it is a basic
        attack, this will instead be how much damage the
        attack does.
    radius : str
        The radius of the ability
    attributes : list
        A list of the ability's attributes

    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = ""
        self.affects = ""
        self.damage = ""
        self.radius = ""

        try:
            menuitems = kwargs.get('Description').get('itemDescription').get('menuitems')
        except AttributeError:  # probably a basic attack
            menuitems = kwargs.get('itemDescription').get('menuitems')

        for i in menuitems:
            d = i['description'].lower()
            if 'ability' in d:
                self.type = i['value']
            elif 'affects' in d:
                self.affects = i['value']
            elif 'damage' in d:
                self.damage = i['value']
            elif 'radius' in d:
                self.radius = i['value']

        try:
            self.attributes = kwargs.get('Description').get('itemDescription').get('rankitems')
        except AttributeError:  # probably a basic attack
            self.attributes = kwargs.get('itemDescription').get('rankitems')


class Skin:
    """Represents a skin.

    Parameters
    ----------
    id : int
        The first ID of the skin
    id2 : int
        The second ID of the skin
    name : str
        The name of the skin

    """
    def __init__(self, **kwargs):
        self.id = kwargs.get('skin_id1')
        self.id2 = kwargs.get('skin_id2')
        self.name = kwargs.get('skin_name')

    def __str__(self):
        return "<Skin {}/{}>".format(self.id, self.name)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id


class GodSkin(Skin):
    """Represents a god skin.

    This is a sub-class of :class:`Skin`.

    Parameters
    ----------
    rarity : str
        How rare the skin is
    favor : int
        How much favor the skin costs
    gems : int
        How many gems the skin costs
    god_id : int
        The ID of the god
    god_name : str
        The name of the god

    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rarity = kwargs.get('obtainability')
        self.favor = kwargs.get('price_favor')
        self.gems = kwargs.get('price_gems')
        self.god_id = kwargs.get('god_id')
        self.god_name = kwargs.get('god_name')
        self.icon_url = kwargs.get('godIcon_URL')
        self.card_url = kwargs.get('godSkin_URL')


class Item(SmiteObject):
    """Represents an in-game item

    This is a sub-class of :class:`HrpObject`.

    Parameters
    ----------
    category : str
        The category of the item
    name : str
        The name of the item
    id : int
        The ID of the item
    icon_id : int
        The ID of the item's icon
    category_id : int
        The ID of the category
    role_id : int
        The ID of the role
    role : str
        The item's role
    god_id : int
        The god's ID
    god_name : str
        The god's name

    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.child_item_id = kwargs.get('ChildItemId')
        self.root_item_id = kwargs.get('RootItemId')
        self.name = kwargs.get('DeviceName')
        self.id = kwargs.get('ItemId')
        self.tier = kwargs.get('ItemTier')
        self.price = kwargs.get('Price')
        self.short_desc = kwargs.get('ShortDesc')
        self.starting_item = kwargs.get('StartingItem')
        self.type = kwargs.get('Type')
        self.icon_url = kwargs.get('itemIcon_URL')

        menuitems = kwargs.get('ItemDescription').get('Menuitems')

    def __str__(self):
        return "<Item {}/{}>".format(self.id, self.name)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id


class ItemStats:
    def __init__(self):
        pass