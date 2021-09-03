from recipe import rotd_url, get_recipe
from database import Recipe

if __name__ == '__main__':
    rec = get_recipe(rotd_url())

    for key, val in rec.__dict__.items():
        print(key + ": " + str(val))

    Recipe.add_new_recipe(rec.name, rec.image, rec.prep_time_min, rec.cook_time_min, rec.total_time_min, rec.servings,
                          rec.ingredients, rec.instructions, rec.nutrition)


