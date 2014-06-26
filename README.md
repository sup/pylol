pylol
=====

A Python wrapper for Riot Games' League of Legends API
(may not be up to date with API latest specifications)

Description
=========
Riot Games released their official developer's API recently. It is a RESTful, fairly rate limited API that allows anyone to get data about a summoner, champion, leagues, recent matches, and more in clean, JSON format. This module is a Python interface into Riot's API by wrapping the HTML requests and parsing the returning JSON using built-in urllib2 and json libraries.

Usage and Examples
================
For simple usage:
* Create a new Pylol object by importing the module and calling the class constructor (ex. p = Pylol("API_KEY", "REGION"))
* Then, simply call the class methods that corresponds to the appropriate API call you want to make. For example, to get a hash table containing every champion in the game and their attributes, simply invoke: p.get_champions()

Methods
=======
* get_champions
* get_game
* get_league
* get_stats
* get_summoner
* get_summoner_by_name
* get_team

For more information about each method, read the documentation within the pylol.py module.
