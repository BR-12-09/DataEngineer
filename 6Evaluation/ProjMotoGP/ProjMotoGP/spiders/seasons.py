import scrapy
import json
from .. items import Season

class SeasonsSpider(scrapy.Spider):
    name = "seasons"
    allowed_domains = ["api.pulselive.motogp.com"]
    start_urls = ["https://api.pulselive.motogp.com/motogp/v1/results/seasons"]

    def parse(self, response):
        # Parser la réponse de l'API initiale
        data_seasons_details = json.loads(response.text)

        # Récupérer les données des saisons
        for season in data_seasons_details:
            id = season.get("id", "N/A")
            year = season.get("year", "N/A")
            current = season.get("current", "N/A")

            # On peut maintenant envoyer les données combinées dans un seul `yield` que pour les saions dont on veut utiliser dans le projet c'est à dire à partir de l'année 2000
            if year >= 2000:
                yield Season(
                    id = id,
                    year = year,
                    current = current
                )