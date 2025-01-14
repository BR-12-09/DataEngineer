import scrapy
from scrapy import Request
import json
from .. items import Team
from pathlib import Path

class TeamsSpider(scrapy.Spider):
    name = "teams"
    allowed_domains = ["api.pulselive.motogp.com"]
    #start_urls = ["https://api.pulselive.motogp.com/motogp/v1/teams?categoryUuid=737ab122-76e1-4081-bedb-334caaa18c70&seasonYear=2024"]

    def start_requests(self):
        # Charger le fichier seasons.json
        seasons_file = Path(__file__).parent.parent.parent / "seasons.json"
        with open(seasons_file, "r") as f:
            seasons = json.load(f)

        # Parcourir les IDs des saisons pour générer les URLs
        base_url = "https://api.pulselive.motogp.com/motogp/v1/teams"
        category_uuid = "737ab122-76e1-4081-bedb-334caaa18c70"

        for season in seasons:
            url = f"{base_url}?categoryUuid={category_uuid}&seasonYear={season["year"]}"
            yield Request(url, callback=self.parse)

    def parse(self, response):
        # Parser la réponse de l'API initiale
        data_teams_details = json.loads(response.text)

        # Récupérer les données des saisons
        for team in data_teams_details:
            id = team.get("id", "N/A")
            name = team.get("name", "N/A")
            constructor_name = team.get("constructor", {}).get("name", "N/A")
            rider1_id = team.get("riders", [])[0].get("id","N/A")
            if len(team.get("riders", [])) > 1:
                rider2_id = team.get("riders", [])[1].get("id","N/A")
            else:
                rider2_id = "null"

            # On peut maintenant envoyer les données combinées dans un seul `yield` que pour les saions dont on veut utiliser dans le projet c'est à dire à partir de l'année 2000
            yield Team(
                id = id,
                name = name,
                constructor_name = constructor_name,
                rider1_id = rider1_id,
                rider2_id = rider2_id
            )
