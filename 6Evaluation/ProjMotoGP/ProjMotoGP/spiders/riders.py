import scrapy
from scrapy import Request
import json
from .. items import Rider
from pathlib import Path

class RidersSpider(scrapy.Spider):
    name = "riders"
    allowed_domains = ["api.pulselive.motogp.com"]
    #start_urls = [
    #    "https://api.pulselive.motogp.com/motogp/v1/results/standings?seasonUuid={seasons.json}&categoryUuid=e8c110ad-64aa-4e8e-8a86-f2f152f6a942"
    #]

    def start_requests(self):
        # Charger le fichier seasons.json
        seasons_file = Path(__file__).parent.parent.parent / "seasons.json"
        with open(seasons_file, "r") as f:
            seasons = json.load(f)

        # Parcourir les IDs des saisons pour générer les URLs
        base_url = "https://api.pulselive.motogp.com/motogp/v1/results/standings"
        category_uuid = "e8c110ad-64aa-4e8e-8a86-f2f152f6a942"

        for season in seasons:
            url = f"{base_url}?seasonUuid={season["id"]}&categoryUuid={category_uuid}"
            yield Request(url, callback=self.parse)

    def parse(self, response):
        # Parser la réponse de l'API initiale
        data = json.loads(response.text)
        
        # Récupérer les UUIDs des pilotes
        riders_api_uuids = [
            rider.get("rider", {}).get("riders_api_uuid", None)
            for rider in data.get("classification", [])
        ]

        # Concaténer une nouvelle url pour scrapper les details des pilotes sur celle-ci
        for uuid in riders_api_uuids:
            if uuid:
                rider_url_details = f"https://api.pulselive.motogp.com/motogp/v1/riders/{uuid}"
                # Créer un dictionnaire pour stocker les informations des pilotes
                rider_data = {}
                # Passer une request sur la nouvelle url et un callback qui appellera `parse_rider_details` et un dictionnaire avec les données existantes
                yield Request(
                    url=rider_url_details,
                    callback=self.parse_rider_details,
                    meta={'rider_data': rider_data}  # Passer les données associées dans `meta`
                )

    def parse_rider_details(self, response):
        # Parser la réponse de l'API spécifique aux détails des pilotes
        data_rider_details = json.loads(response.text)

        # Récupérer les données des pilotes
        id = data_rider_details.get("id", "N/A")
        legacy_id = data_rider_details.get("legacy_id", "N/A")
        name = data_rider_details.get("name", "N/A")
        surname = data_rider_details.get("surname", "N/A")
        country = data_rider_details.get("country", {}).get("name", "N/A")
        country_flag = data_rider_details.get("country", {}).get("flag", "N/A")

        # Initialiser un dictionnaire pour regrouper les saisons et les équipes
        #s = []
        #idt = []
        season_team_mapping = {}
        # Parcourir les détails de la carrière
        for season in data_rider_details.get("career", []):
            season_year = season.get("season", "N/A")
            if season.get("team") and isinstance(season.get("team"), dict):
                team_id = season.get("team", {}).get("id", "N/A")
            else:
                team_id = "N/A"
            #team_id = season.get("team", {}).get("id", "N/A")
            season_team_mapping[season_year] = team_id  # Associer la saison à l'équipe
            # s.append(season.get("season", "N/A"))
            # if season.get("team") and isinstance(season.get("team"), dict):
            #     team_id = season.get("team", {}).get("id", "N/A")
            # else:
            #     team_id = "N/A"
            # idt.append(team_id)

        birth_date = data_rider_details.get("birth_date", "N/A")
        birth_city = data_rider_details.get("birth_city", "N/A")
        #bio = data_rider_details.get("biography", {}).get("text", "N/A")
        height = data_rider_details.get("physical_attributes", {}).get("height", "N/A")
        weight = data_rider_details.get("physical_attributes", {}).get("weight", "N/A")
        start_year = data_rider_details.get("start_year", "N/A")
        retired_year = data_rider_details.get("retired_year", "N/A")
        retired = data_rider_details.get("retired", "N/A")

        # Récupérer les données déjà associées dans `meta` (les données envoyées avec `yield Request` plus haut)
        rider_data = response.meta['rider_data']

        # Ajouter les informations du pilote aux données déjà existantes
        rider_data.update({
            "id": id,
            "legacy_id": legacy_id,
            "name": name,
            "surname": surname,
            "country": country,
            "country_flag": country_flag,
            "birth_date": birth_date,
            "birth_city": birth_city,
            #"bio": bio,
            "height": height,
            "weight": weight,
            "start_year": start_year,
            "retired_year": retired_year,
            "retired": retired,
            "season_team":season_team_mapping
            # "s": s,
            # "idt":idt
        })

        # Maintenant on fait une deuxième requête pour récupérer les statistiques des pilotes
        rider_url_stats = f"https://api.pulselive.motogp.com/motogp/v1/riders/{rider_data['legacy_id']}/stats"
        # Passer une request sur la nouvelle url et un callback qui appellera `parse_rider_stats` et un dictionnaire avec les données déjà existantes et updater
        yield Request(
            url=rider_url_stats,
            callback=self.parse_rider_stats,
            meta={'rider_data': rider_data}  # Passer les données existantes dans `meta`
        )
        
        # Output the results
        #self.log(f"Name: {rider_name}, Surname: {rider_surname}")

    def parse_rider_stats(self, response):
        # Parser la réponse de l'API spécifique aux stats des pilotes
        data_rider_stats = json.loads(response.text)

        # Récupérer les données des stats des pilotes
        world_champion_wins = data_rider_stats.get("world_championship_wins", {}).get("categories", [])[0].get("count", "N/A") #remplacer 0 par id categories
        grand_prix_victories = data_rider_stats.get("grand_prix_victories", {}).get("categories", [])[0].get("count", "N/A")
        podiums = data_rider_stats.get("podiums", {}).get("categories", [])[0].get("count", "N/A")
        poles = data_rider_stats.get("poles", {}).get("categories", [])[0].get("count", "N/A")
        races = data_rider_stats.get("all_races", {}).get("categories", [])[0].get("count", "N/A")

        # Récupérer les données déjà associées dans `meta` (les données envoyées avec le 2ème `yield Request` plus haut)
        rider_data = response.meta['rider_data']

        # Ajouter les statistiques des pilotes aux données déjà existantes
        rider_data.update({
            "world_champion_wins": world_champion_wins,
            "grand_prix_victories":  grand_prix_victories,
            "podiums": podiums,
            "poles": poles,
            "races": races
        })

        # Output the results
        #self.log(f"Name: {rider_name}, Surname: {rider_surname}")

        # À ce moment-là, toutes les données sont disponibles dans `rider_data`
        # On peut maintenant envoyer les données combinées dans un seul `yield`
        yield Rider(
            id = rider_data.get('id'),
            legacy_id = rider_data.get('legacy_id'),
            name = rider_data.get('name'),
            surname = rider_data.get('surname'),
            country = rider_data.get('country'),
            country_flag = rider_data.get("country_flag"),
            birth_date = rider_data.get("birth_date"),
            birth_city = rider_data.get("birth_city"),
            #bio = rider_data.get("bio"),
            taille = rider_data.get("height"),
            poids = rider_data.get("weight"),
            start_year = rider_data.get("start_year"),
            retired_year = rider_data.get("retired_year"),
            retired = rider_data.get("retired"),
            season_team = rider_data.get("season_team"),
            # s = rider_data.get("s"),
            # idt = rider_data.get("idt"),
            world_champion_wins = rider_data.get("world_champion_wins"),
            grand_prix_victories = rider_data.get("grand_prix_victories"),
            podiums = rider_data.get('podiums'),
            poles = rider_data.get("poles"),
            races = rider_data.get("races")
        )

#{"id": "ea39a0af-95d3-4a37-81a7-f332efdb9216", "legacy_id": 8658, "name": "Pedro", "surname": "Acosta", "country": "Spain", "country_flag": "https://photos.motogp.com/countries/flags/iso2/ES.svg", "birth_date": "2004-05-25", "birth_city": "Murcia, Spain", "taille": 171, "poids": 63, "start_year": 2020, "retired_year": 2024, "retired": true, "world_champion_wins": 0, "grand_prix_victories": 0, "podiums": 5, "poles": 1, "races": 19, "teams":[{"id-teams":{2002-2005}, "id-teams":{2006_2025}}]},
