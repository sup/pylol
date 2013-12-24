#pylol.py
#Charles J. Lai
#December 21, 2013

import urllib2
import json

class Pylol(object):
    """
    ===========
    Description
    ===========
    This class contains the necessary functions to make API calls to the
    official Riot Games League of Legends developer API. More info in the 
    README file. Anything not clarified in module documentation can be
    found gleaned by consulting the Riot API documentation.

    Fields
    ------
    api_key: User-defined key from Riot Games
    region: User-defined region for API call parameters

    Methods
    -------

    """
    #Constants:
    URL_BASE = 'http://prod.api.pvp.net/api/lol/'

    #Fields
    _api_key = ""
    _region = ""

    #Properties
    @property
    def api_key(self):
        return self._api_key

    @api_key.setter
    def api_key(self, key):
        self._api_key = key

    @property
    def region(self):
        return self._region

    @region.setter
    def region(self, r):
        self._region = r

    #Constructor
    def __init__(self, key, r = 'na'):
        self.api_key = key
        self.region = r

    #Helper Method for performing a specified call
    def _request(self, param, special_case = False):
        """
        Returns: Parsed JSON data after forming an HTTP request to Riot Games.
        The data returned depends on a specified parameter that is generated
        by the various methods below. URL is both formatted and sent with this
        method.
        """
        #Check if the API call should be formatted differently
        if special_case:
            #Case: Free to play champion filter
            if param == '/v1.1/champion?freeToPlay=true':
                return json.loads(urllib2.urlopen(self.URL_BASE + urllib2.quote(self.region) + param + '&api_key=' + urllib2.quote(self.api_key)).read())
        else:
            return json.loads(urllib2.urlopen(self.URL_BASE + urllib2.quote(self.region) + param + '?api_key=' + urllib2.quote(self.api_key)).read())

    #Methods for formatting API calls
    def get_champions(self, free_to_play = False):
        """
        Returns: A single entry hash table containing a list of champions 
        with key "champions". The list of champions that corresponds to the 
        key is a list of hash tables containing each champion's attributes.
        Additionally, an optional parameter for filtering free to play
        champions can be specified.

        Example
        -------
        {"champions": [
           {
              "botMmEnabled": false,
              "defenseRank": 4,
              "attackRank": 8,
              "id": 266,
              "rankedPlayEnabled": true,
              "name": "Aatrox",
              "botEnabled": false,
              "difficultyRank": 6,
              "active": true,
              "freeToPlay": false,
              "magicRank": 3
           },
           ...
        ]}

        """
        param = '/v1.1/champion'
        #Add the appropriate arguments to the call parameters if filtering
        if free_to_play:
            param = param + '?freeToPlay=true'
            return self._request(param, True)
        return self._request(param)

    def get_game(self, id):
        """
        Returns: A 2 entry hash table containing a list of games under "games"
        played recently by a given summoner, and the summoner's summoner id
        under "summonerid". The list of games is a list of hash tables with
        various entries detailing the stats and data of each given game.

        Precondtions: id is an integer number
        """
        assert type(id) == int, "The summoner id given is not an integer"
        param = '/v1.2/game/by-summoner/' + `id` + '/recent'
        return self._request(param)

    def get_league(self,id):
        """
        Returns:

        Precondtions: id is an integer number
        """
        assert type(id) == int, "The summoner id given is not an integer"
        param = '/v2.2/league/by-summoner/' + `id`
        return self._request(param)

    def get_stats(self,id,option='summary'):
        """
        Returns:

        Precondtions:
        """
        param = '/v1.2/stats/by-summoner/' + `id` + '/' + option
        return self._request(param)

    def get_summoner(self,id,option=None):
        """
        Returns:

        Precondtions:
        """
        param = '/v1.2/summoner/' + `id` + '/'
        if option == None:
            return self._request(param)
        else:
            assert option == 'masteries' or option == 'runes' or option == 'name', "The argument given is not a valid option."
            param = param + option
            return self._request(param)

    def get_summoner_by_name(self,name):
        """
        Returns:

        Precondtions:
        """
        param = '/v1.2/summoner/by-name/' + name
        return self._request(param)
        pass

    def get_team(self,id):
        """
        Returns:

        Preconditions:
        """
        param = '/v2.2/team/by-summoner/' + `id`
        return self._request(param)




