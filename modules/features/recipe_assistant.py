import json
import os

RECIPES_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "memory_db", "recipes.json"
)


def _load():
    if os.path.isfile(RECIPES_FILE):
        with open(RECIPES_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {}


def _save(recipes):
    mem = os.path.dirname(RECIPES_FILE)
    if not os.path.isdir(mem):
        os.makedirs(mem, exist_ok=True)
    with open(RECIPES_FILE, "w", encoding="utf-8") as f:
        json.dump(recipes, f, indent=2, ensure_ascii=False)


def add_recipe(name: str, ingredients: list, instructions: str) -> str:
    recipes = _load()
    recipes[name.lower()] = {
        "ingredients": ingredients,
        "instructions": instructions,
        "created": __import__("datetime").datetime.now().isoformat(),
    }
    _save(recipes)
    return f"Recipe '{name}' saved."


def get_recipe(name: str) -> str:
    recipes = _load()
    recipe = recipes.get(name.lower())
    if not recipe:
        # fuzzy search
        matches = [k for k in recipes if name.lower() in k]
        if matches:
            recipe = recipes[matches[0]]
            name = matches[0]
        else:
            return f"Recipe '{name}' not found."
    ings = ", ".join(recipe["ingredients"])
    return f"Recipe: {name}. Ingredients: {ings}. Instructions: {recipe['instructions'][:200]}"


def find_by_ingredient(ingredient: str) -> str:
    recipes = _load()
    matches = []
    for name, recipe in recipes.items():
        if any(ingredient.lower() in ing.lower() for ing in recipe["ingredients"]):
            matches.append(name)
    if not matches:
        return f"No recipes with '{ingredient}'."
    return f"Recipes with {ingredient}: " + ", ".join(matches[:10])


def list_recipes() -> str:
    recipes = _load()
    if not recipes:
        return "No saved recipes."
    return "Recipes: " + ", ".join(recipes.keys())


try:
    from modules.llm.llm_manager import query_llm, TaskType

    HAS_LLM = True
except Exception:
    HAS_LLM = False


def suggest_recipe(ingredients: list) -> str:
    if not HAS_LLM:
        return "LLM not available."
    prompt = f"Suggest a recipe using these ingredients: {', '.join(ingredients)}. Return name, ingredients list, and short instructions."
    result = query_llm(prompt, task_type=TaskType.FAST_CONVERSATION)
    return result[:500] if result else "Could not suggest recipe."
