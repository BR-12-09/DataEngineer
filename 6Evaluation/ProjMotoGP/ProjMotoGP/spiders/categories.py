import scrapy
import json
from .. items import Categorie

class CategoriesSpider(scrapy.Spider):
    name = "categories"
    allowed_domains = ["api.pulselive.motogp.com"]
    start_urls = ["https://api.pulselive.motogp.com/motogp/v1/categories?seasonYear=2024"]

    def parse(self, response):
        # Parser la réponse de l'API initiale
        data_categories_details = json.loads(response.text)

        # Récupérer les données des saisons
        for categories in data_categories_details:
            id = categories.get("id", "N/A")
            name = categories.get("name", "N/A")

            # On peut maintenant envoyer les données combinées dans un seul `yield` que pour les saions dont on veut utiliser dans le projet c'est à dire à partir de l'année 2000
            if name == "MotoGP":
                yield Categorie(
                    id = id,
                    name = name
                )
