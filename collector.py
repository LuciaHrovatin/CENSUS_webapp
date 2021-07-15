from __future__ import absolute_import, annotations
import json

def number_regions(filename: str, province: str) -> int:
    """
    Takes the province and returns the integer according to the data encoded in the dataset.
    :param str filename: json file containing all the Italian region
    :param str province: name of the province
    :return: integer of the region (1-20)
    """
    with open(filename) as f:
        data = json.load(f)
        # region numbers come from the dataset
        regions_n = {
            "Piemonte": 1,
            "Valle d'Aosta": 2,
            "Lombardia": 3,
            "Trentino": 4,
            "Veneto": 5,
            "Friuli": 6,
            "Liguria": 7,
            "Emilia Romagna": 8,
            "Toscana": 9,
            "Umbria": 10,
            "Marche": 11,
            "Lazio": 12,
            "Abruzzo": 13,
            "Molise": 14,
            "Campania": 15,
            "Puglia": 16,
            "Basilicata": 17,
            "Calabria": 18,
            "Sicilia": 19,
            "Sardegna": 20
        }
        for region in data:
            for prov in data[region]:
                if province in prov["nome"]:
                    region = region.split("-")[0]
                    return regions_n[region]
