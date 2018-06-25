import asyncio

from .request import Request
from .objects import Limits, Match, Player, Rank, God, GodSkin, Item

from datetime import datetime

class Client:
    """Class for handling connections and requests to Hi Rez Studios' APIs

    Parameters
    ----------
    dev_id : str
        Used for authentication. This is the developer ID that you
        receive from Hi-Rez Studios.
    auth_key : str
        Used for authentication. This is the authentication key that you
        receive from Hi-Rez Studios.
    loop : [optional] event loop
        The event loop used for async ops. If this is the default (None),
        the bot will use asyncio's default event loop.
    """
    def __init__(self, dev_id, auth_key, *, loop=None):
        self.dev_id = str(dev_id)
        self.auth_key = str(auth_key)
        self.loop = asyncio.new_event_loop()
        self.endpoint = 'http://api.smitegame.com/smiteapi.svc'
        self.language = 1

        self.request = Request(self)

    async def ping(self):
        """
        Pings the API in order to establish connectivity

        Returns
        -------
        boolean equal to `True`

        """
        res = await self.request.make_request(self.endpoint, 'ping', no_auth=True)
        return True if 'successful' in res else None

    async def get_data_used(self):
        """
        Gets the data limits for the developer.

        Returns
        -------
        :class:`Limits` object
            The developer limits.

        """
        res = await self.request.make_request(self.endpoint, 'getdataused')
        obj = Limits(**res[0])  # res should be a list, so we want the first element
        return obj

    async def get_esports_details(self):
        """
        Returns the match-up information for each match-up for the current eSports Pro League season.

        Returns
        -------
        set of :class:`Match` objects
            The matches in the current season.

        """
        res = await self.request.make_request(self.endpoint, 'getesportsproleaguedetails')
        matches = []
        for i in res:
            obj = Match(**i)
            matches.append(obj)
        return set(matches)

    async def get_friends(self, username):
        """
        Returns information about a user's friends.

        Parameters
        ----------
        username : str
            The username of the player to get information about

        Returns
        -------
        list of :class:`Player` objects or `None`
            Represents the given user's friends. Will return None if
            the user's privacy settings do not allow, or the
            user given is invalid.

        """
        res = await self.request.make_request(self.endpoint, 'getfriends', params=[username])
        if not res:
            res = None  # invalid user or privacy settings active
        else:
            players = []
            for i in res:
                if i['account_id'] == '0':  # privacy settings active, skip
                    continue
                obj = Player(**i)
                players.append(obj)
            res = players if players else None
        return res

    async def get_ranks(self, username):
        """
        Returns information about a user's god ranks

        Parameters
        ----------
        username : str
            The username of the player to get information about

        Returns
        -------
        list of :class:`Rank` objects or `None`
            Represents the given user's ranks. Will return None if
            the user's privacy settings do not allow, or the
            user given is invalid.

        """
        res = await self.request.make_request(self.endpoint, 'getgodranks', params=[username])
        if not res:
            res = None  # invalid user or privacy settings active
        else:
            ranks = []
            for i in res:
                if 'god' not in i:  # must be paladins
                    i['god'] = i['champion']
                    i['god_id'] = i['champion_id']
                obj = Rank(**i)
                ranks.append(obj)
            res = ranks if ranks else None
        return res

    async def get_characters(self):
        """
        Returns Gods in Smite.

        Returns
        -------
        list of :class:`God` objects
            Returns the Gods in Smite.

        """
        res = await self.request.make_request(self.endpoint, 'getgods', params=["1"])
        return res

    async def get_skins(self, character_id):
        """
        Return the skins for a character.

        Parameters
        ----------
        character_id : str
            The character to get skins for

        Returns
        -------
        list of :class:`GodSkin` or None
            Returns the skins for a character.

        """
        character_id = str(character_id)
        res = await self.request.make_request(self.endpoint, 'getgodskins', params=[character_id, "1"])
        if not res:
            skins = None
        else:
            skins = []
            for i in res:
                obj = GodSkin(**i)
                skins.append(obj)
        return skins

    async def get_recommended_items(self, character_id):
        """
        Return the recommended items for a character.

        Parameters
        ----------
        character_id : str
            The character to check against

        Returns
        -------
        set of :class:`Item` or None
            Returns the recommended items for a character. Returns None if an
            invalid ID is given and no data is returned.

        """
        character_id = str(character_id)
        res = await self.request.make_request(self.endpoint, 'getgodrecommendeditems', params=[character_id, "1"])
        if not res:
            items = None
        else:
            items = []
            for i in res:
                obj = Item(**i)
                items.append(obj)
        return set(items)

    async def get_items(self):
        res = await self.request.make_request(self.endpoint, 'getitems', params=["1"])
        return res

    async def get_player(self, username):
        """Returns information about a user"""
        res = await self.request.make_request(self.endpoint, 'getplayer', params=[username])
        if not res:
            res = None  # invalid user or privacy settings active
        else:
            player = res[0]
            obj = Player(**player)
            res = obj
        return res

    async def get_match_details(self, match_id):
        res = await self.request.make_request(self.endpoint, 'getmatchdetails', params=[match_id])
        if not res:
            return None
        return res

    async def get_match_q(self):
        res = await self.request.make_request(self.endpoint, 'getmatchidsbyqueue', params=["423", "20180304", "-1"])
        if not res:
            return None
        return res