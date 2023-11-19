from abc import ABC, abstractmethod

# Menu class (Abstract class)
class Menu(ABC):
    @abstractmethod
    def __init__(self, name, image_path, ingredients_path, instructions_path, nutrition, servings): # Constructor
        self.name = name
        self.image_path = image_path
        self.ingredients_path = ingredients_path
        self.instructions_path = instructions_path
        self.nutrition = nutrition
        self.servings = servings
    
    @abstractmethod
    def get_ingredients(self):
        pass
    
    @abstractmethod
    def get_image(self):
        pass
    
    @abstractmethod
    def get_instructions(self):
        pass
    
    @abstractmethod
    def get_nutrition(self):
        pass

# Dish object
class Dish(Menu):
    # Inherit from Menu class
    def __init__(self, name, image_path, ingredients_path, instructions_path, nutrition, servings):
        super().__init__(name, image_path, ingredients_path, instructions_path, nutrition, servings)
        
    def get_ingredients(self):
        return self.ingredients_path
    
    def get_image(self):
        return self.image_path
    
    def get_instructions(self):
        return self.instructions_path
    
    # Get the nutrition of the dish
    def get_nutrition(self):
        dish_nutrition = {}
        dish_nutrition["Servings"] = self.servings
        dish_nutrition["Calories"] = self.nutrition["ENERC_KCAL"]["quantity"]
        dish_nutrition["Fat"] = self.nutrition["FAT"]["quantity"]
        dish_nutrition["Sodium"] = self.nutrition["NA"]["quantity"]
        dish_nutrition["Carbohydrates"] = self.nutrition["CHOCDF"]["quantity"]
        dish_nutrition["Protein"] = self.nutrition["PROCNT"]["quantity"]
        
        return dish_nutrition
        
# Dessert object
class Dessert(Menu):
    # Inherit from Menu class
    def __init__(self, name, image_path, ingredients_path, instruction_path, nutrition, servings):
        super().__init__(name, image_path, ingredients_path, instruction_path, nutrition, servings)
        
    def get_ingredients(self):
        return self.ingredients_path
    
    def get_image(self):
        return self.image_path
    
    def get_instructions(self):
        return self.instructions_path

    # Get the nutrition of the dessert
    def get_nutrition(self):
        dessert_nutrition = {}
        dessert_nutrition["Servings"] = self.servings
        dessert_nutrition["Calories"] = self.nutrition["ENERC_KCAL"]["quantity"]
        dessert_nutrition["Fat"] = self.nutrition["FAT"]["quantity"]
        dessert_nutrition["Sugar"] = self.nutrition["SUGAR"]["quantity"]
        dessert_nutrition["Carbohydrates"] = self.nutrition["CHOCDF"]["quantity"]
        
        return dessert_nutrition

# Snack object
class Snack(Menu):
    # Inherit from Menu class
    def __init__(self, name, image_path, ingredients_path, instruction_path, nutrition, servings):
        super().__init__(name, image_path, ingredients_path, instruction_path, nutrition, servings)
        
    def get_ingredients(self):
        return self.ingredients_path
    
    def get_image(self):
        return self.image_path
    
    def get_instructions(self):
        return self.instructions_path
    
    # Get the nutrition of the snack
    def get_nutrition(self):
        snack_nutrition = {}
        snack_nutrition["Servings"] = self.servings
        snack_nutrition["Calories"] = self.nutrition["ENERC_KCAL"]["quantity"]
        snack_nutrition["Sugar"] = self.nutrition["SUGAR"]["quantity"]
        snack_nutrition["Fat"] = self.nutrition["FAT"]["quantity"]
        snack_nutrition["Sodium"] = self.nutrition["NA"]["quantity"]
        
        return snack_nutrition
