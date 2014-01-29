
"""

pylol - A Python wrapper for Riot Games' League of Legends API
Charles Lai (www.charlesjianlai.com)
www.github.com/charleslai/pylol

The MIT License (MIT)

Copyright (c) 2013 Charles J. Lai

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""

import urllib2
import json

class Pylol(object):
    """
    This class contains the necessary functions to make API calls to the
    official Riot Games League of Legends developer API. More info in the 
    README file. Anything not clarified in module documentation can be
    found gleaned by consulting the Riot API documentation, especially
    the specifics of the JSON data returned.
    """
    #Constants:
    URL_BASE = 'http://prod.api.pvp.net/api/lol/'
    RATE_LIMIT = None   #5 requests every 10 seconds

    #Fields
    _api_key = ""
    _region = ""
    _cache = {}     #This cache caches the url parameter/hash table result

    #Getters/Setters
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

    @property
    def cache(self):
        return self._cache

    @cache.setter
    def cache(self, c):
        self._cache = c

    #Constructor
    def __init__(self, key, r = 'na', c = {}):
        self.api_key = key
        self.region = r
        self.cache = c

    #Helper Method for performing a specified call
    def _request(self, param, special_case = False):
        """
        Returns: Parsed JSON data after forming an HTTP GET request to Riot Games.
        The data returned depends on a specified parameter that is generated
        by the various methods below. URL is both formatted and sent with this
        method.
        """
        #Check if the GET parameters are already in the cache
        if param in self.cache:
            return self.cache[param]

        #Check if the API call should be formatted differently
        if special_case:
            #Case: Free to play champion filter - special GET parameter
            if param == '/v1.1/champion?freeToPlay=true':
                return json.loads(urllib2.urlopen(self.URL_BASE + 
                urllib2.quote(self.region) + param + '&api_key=' + 
                urllib2.quote(self.api_key)).read())

        #Else, make a new request, parse the JSON, and cache the data.
        else:
            self.cache[param] = json.loads(urllib2.urlopen(self.URL_BASE + 
            urllib2.quote(self.region) + param + '?api_key=' + 
            urllib2.quote(self.api_key)).read())
            return self.cache[param]



    #Methods for formatting API calls
    def get_champions(self, free_to_play = False):
        """
        Returns: A single entry hash table containing a list of champions 
        The list of champions is a list of hash tables containing each 
        champion's attributes. Additionally, an optional parameter for 
        filtering free to play champions can be specified.
        """
        param = '/v1.1/champion'
        #Add the appropriate GET parameter if filtering
        if free_to_play:
            param = param + '?freeToPlay=true'
            return self._request(param, True)
        return self._request(param)

    def get_game(self, id):
        """
        Returns: A 2 entry hash table containing a list of games and 
        the summoner id. The list of games is a list of hash tables with
        various entries detailing the stats and data of each given game.

        Precondtions: id is an integer number
        """
        assert type(id) == int, "The summoner id given is not an integer"
        param = '/v1.3/game/by-summoner/' + `id` + '/recent'
        return self._request(param)

    def get_league(self,id):
        """
        Returns: A single entry hash table containing another hash table under
        a specified summoner id. This second hash table contains various
        attributes about specified summoner's league/queue type.

        Precondtions: id is an integer number
        """
        assert type(id) == int, "The summoner id given is not an integer"
        param = '/v2.3/league/by-summoner/' + `id`
        return self._request(param)

    def get_stats(self,id,option='summary'):
        """
        Returns: A 2 entry hash table containing a list of stats and the
        specified summoner id. The list of stats is a list of hash tables 
        with various entries detailing the stats of a given summoner.
        Option can be either 'summary' or 'ranked'.

        Precondtions: id is an integer, option is a valid option
        """
        assert type(id) == int, "The summoner id given is not an integer"
        assert option == 'summary' or option == 'ranked', "The option is not a valid one"
        param = '/v1.3/stats/by-summoner/' + `id` + '/' + option
        return self._request(param)

    def get_summoner(self,id,option=None):
        """
        Returns: A 5-entry hash tabe containing basic data about a given
        summoner. If option is specified to be 'masteries', 'runes', or 
        'name', the API will return the appropriate data.

        Precondtions: id is an integer, option is a valid option
        """
        assert type(id) == int, "The summoner id given is not an integer"
        param = '/v1.3/summoner/' + `id` + '/'
        if option == None:
            return self._request(param)
        else:
            assert option == 'masteries' or option == 'runes' or option == 'name', "The option is not a valid one"
            param = param + option
            return self._request(param)

    def get_summoner_by_name(self,name, option=None):
        """
        Returns: A 5-entry hash tabe containing basic data about a given
        summoner by name. If the option is

        Precondtions: name is a string
        """
        assert type(name) == str, "The summoner name given is not a string"
        param = '/v1.3/summoner/by-name/' + name
        if option == None:
            return self._request(param)
        else:
            pass

    def get_team(self,id):
        """
        Returns: A list of data and hash tables containing various data
        about a given summoner's teams and its statistics.

        Preconditions: id is an integer
        """
        assert type(id) == int, "The summoner id given is not an integer"
        param = '/v2.3/team/by-summoner/' + `id`
        return self._request(param)




