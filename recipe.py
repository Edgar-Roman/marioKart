from constants import MEASUREMENTS, ROTD, URL
from bs4 import BeautifulSoup
import requests
import json
import re


def rotd_url():
    allrecipes = requests.get(url=URL).text
    rotd = allrecipes[allrecipes.find(ROTD):][allrecipes[allrecipes.find(ROTD):].find('href="') + len('href="'):]
    url = rotd[:rotd.find('"')]
    return url


def get_recipe(url):
    recipe_page = requests.get(url=url)
    soup = BeautifulSoup(recipe_page.text, "html.parser")
    res = soup.find('script')
    recipe = json.loads(res.contents[0])[1]

    return Recipe(recipe)


class Recipe:
    def __init__(self, recipe):
        self.name = recipe['name']
        self.image = recipe['image']['url']
        self.prep_time_min = self.extract_time_in_min(recipe['prepTime'])
        self.cook_time_min = self.extract_time_in_min(recipe['cookTime'])
        self.total_time_min = self.extract_time_in_min(recipe['totalTime'])
        self.servings = self.extract_servings(recipe['recipeYield'])
        self.ingredients = self.extract_ingredients(recipe['recipeIngredient'])
        self.instructions = self.extract_steps(recipe['recipeInstructions'])
        self.nutrition = self.extract_nutrition(recipe['nutrition'])

    @staticmethod
    def extract_time_in_min(time):
        match = re.match(r'(P)(\d+)(DT)(\d+)(H)(\d+)(M)', time)
        return 60 * int(match.group(4)) + int(match.group(6))

    @staticmethod
    def extract_servings(servings):
        match = re.match(r'(\d)( servings)', servings)
        return int(match.group(1))

    @staticmethod
    def extract_ingredients(ingredients):
        dictionary = {}
        for ingredient in ingredients:
            for measurement in MEASUREMENTS:
                if measurement in ingredient:
                    pos = ingredient.find(measurement) + len(measurement)
                    dictionary[ingredient[pos:].strip()] = ingredient[:pos]
        return str(dictionary)

    @staticmethod
    def extract_steps(steps):
        return str([step['text'].strip() for step in steps])

    @staticmethod
    def extract_nutrition(nutrition):
        if '@type' in nutrition:
            del nutrition['@type']
        return str(nutrition)








