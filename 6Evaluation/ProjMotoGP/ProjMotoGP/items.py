# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Rider(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    legacy_id = scrapy.Field()
    name = scrapy.Field()
    surname = scrapy.Field()
    country = scrapy.Field()
    country_flag = scrapy.Field()
    birth_date = scrapy.Field()
    birth_city = scrapy.Field()
    #bio = scrapy.Field()
    taille = scrapy.Field()
    poids = scrapy.Field()
    start_year = scrapy.Field()
    retired_year = scrapy.Field()
    retired = scrapy.Field()
    season_team = scrapy.Field()
    # s = scrapy.Field()
    # idt = scrapy.Field()
    world_champion_wins = scrapy.Field()
    grand_prix_victories = scrapy.Field()
    podiums = scrapy.Field()
    poles = scrapy.Field()
    races = scrapy.Field()

class Season(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    year = scrapy.Field()
    current = scrapy.Field()

class Categorie(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    name = scrapy.Field()

class Team(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    name = scrapy.Field()
    constructor_name = scrapy.Field()
    rider1_id = scrapy.Field()
    rider2_id = scrapy.Field()
