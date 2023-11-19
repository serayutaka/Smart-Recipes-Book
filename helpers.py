import tkinter as tk
import requests
import shutil
import pickle
from tkinter import PhotoImage, messagebox
from PIL import Image, ImageTk
from io import BytesIO
from tkinter.filedialog import askopenfilename
import customtkinter
import os

from constant import APP_ID, APP_KEY, PATH
from menu_c import *

# Function that will query the Edamam's API
def search_recipe(menu, app_id=APP_ID, app_key=APP_KEY):
    # Url formating for API
    url = "https://api.edamam.com/search?q={}&app_id={}&app_key={}".format(menu,app_id,app_key)
    # Get the response from API
    response = requests.get(url)
    # Convert the response(data) to json
    data = response.json()
    
    # Clean the data
    clean_data = {
        "more" : data["more"],
        "hits" : [data["hits"][0]]
    }
    # Check if the recipe already exist in the list
    for element in data["hits"]:
        counter = 0
        for i in range(len(clean_data["hits"])):
            # If the recipe already exist, then counter will be 1
            if element["recipe"]["label"] == clean_data["hits"][i]["recipe"]["label"]:
                counter += 1
        # If the recipe doesn't exist, then add it to the list
        if counter == 0:
            clean_data["hits"].append(element)
    
    # Return the clean data
    return clean_data

# Function that will get the recipe from Edamam's API
def get_recipe(menu, app_id=APP_ID, app_key=APP_KEY):
    # Url formating for API
    url = "https://api.edamam.com/search?q={}&app_id={}&app_key={}".format(menu,app_id,app_key)
    # Get the response from API
    response = requests.get(url)
    # Convert the response(data) to json
    data = response.json()
    
    # Loop through the data to find the recipe
    for i in range(len(data["hits"])):
        # If the recipe is found, then return it
        if data["hits"][i]["recipe"]["label"] in menu:
            return data["hits"][i]

# Function save img to the local storage
def save_image(image_url, save_path):
    try:
        # Get the image from the url
        response = requests.get(image_url)
        # Save the image to the local storage
        with open(save_path, 'wb') as file:
            file.write(response.content)
        return True
    except Exception:
        return False

# Function save the ingredient to the local storage
def save_ingredient(ingredient, save_path):
    try:
        # Save the ingredient to the local storage
        with open(save_path, 'w') as file:
            file.write("\n".join(ingredient))
        return True
    except Exception:
        return False

# Function save the instruction to the local storage
def save_default_instruction(save_path):
    try:
        # Save default instruction to the local storage
        with open(save_path, 'w') as file:
            file.write("Look like you don't have any instruction yet. Please add one.")
        return True
    except Exception:
        return False

# Function that will read ingredient from the local storage
def read_ingredients(ingredients_path):
    try:
        # Read the ingredient from the local storage
        with open(ingredients_path, 'r') as file:
            ingredient = file.read()
            # Return the ingredient
            return ingredient
    except Exception as e:
        print(f"Error reading ingredient: {e}")

# Function that will read image from the local storage
def read_images_path(images_path):
    # Open the image
    img = Image.open(images_path)
    # Resize the image
    if img.size != (300, 300):
        img = img.resize((300, 300), Image.LANCZOS)
        img.save(images_path)
    img_tk = ImageTk.PhotoImage(img)
    # Return the image
    return img_tk

# Function that will read image from the url
def read_images_url(image_url):
    # Get the image from the url
    response = requests.get(image_url)
    # Convert the image to bytes
    image_data = response.content
    # Open the image
    img = Image.open(BytesIO(image_data))
    # Return the image
    return ImageTk.PhotoImage(img)

# Function that will read instruction from the local storage
def read_instruction(instruction_path):
    try:
        # Read the instruction from the local storage
        with open(instruction_path, 'r') as file:
            instruction = file.read()
            # Return the instruction
            return instruction
    except Exception as e:
        print(f"Error reading instruction: {e}")

# Function that will save instruction from the local storage
def save_instruction(instruction_text_box, selected_recipe, new_window):
    try:
        # Open the instruction file from the local storage
        with open(selected_recipe.get_instructions(), 'w') as file:
            # Write the new instruction to the local storage
            file.write(instruction_text_box.get("1.0", tk.END))
        messagebox.showinfo("", "Saved.")
        new_window.destroy()
    except Exception:
        messagebox.showerror("", "Error to Save.")

# Function that will set image path to variable
def choose_image_path(self, photo_label):
    try:
        # Ask users to choose image
        file_path = askopenfilename(title="Select a file", filetypes=[("JPG Files", ".jpg"), ("PNG Files", ".png")])
        # If the user choose an image, then set the image to the label
        if file_path:
            # Read the image path
            photo = read_images_path(file_path)
            photo_label.configure(image=photo)
            photo_label.photo = photo
            # Set the image path to variable
            return self.selected_img_path.set(file_path)
    except Exception:
        messagebox.showerror("", "Error to choose image.")

# Function that will open the instruction window
def open_instruction(self):
    
    # Create a new window(root)
    new_window = customtkinter.CTkToplevel()
    new_window.geometry("640x360")
    new_window.title("Instruction")
    
    # Set the background image
    bg_img = ImageTk.PhotoImage(Image.open("./assets/bg.jpg"))
    l1 = customtkinter.CTkLabel(master=new_window, image=bg_img, text="")
    l1.pack()
    
    # Create a new textbox
    instruction_text_box = customtkinter.CTkTextbox(new_window, corner_radius=7, font=("Arial", 14),
                                                width=500, height=300)
    instruction_text_box.place(relx=0.11, rely=0.05)
    
    # Create save button 
    btn_save = customtkinter.CTkButton(new_window, text="Save", corner_radius=6, fg_color="white", 
                                       border_color="#FF7A5E", text_color="#FF7A5E",
                                       hover_color="#D9C9C6", border_width=2.5, font=("Arial", 14),
                                       command=lambda: save_instruction_window(self, instruction_text_box, new_window)) # Command to save the instruction
    btn_save.place(relx=0.4, rely=0.9)

# Function to save the new instruction to variable
def save_instruction_window(self, instruction_text_box, new_window):
    messagebox.showinfo("", "Saved.")
    # Set the new instruction to variable
    self.ins.set(instruction_text_box.get("1.0", tk.END))
    new_window.destroy()

# Function that will save the new recipe to the local storage
def save_recipe(self, ingredient_text):
    # Check if the user already input nutrition
    if len(self.nut) == 0:
        return messagebox.showerror("", "Please add nutrition.")
    # Check type of the recipe
    match self.selected_option.get():
            
            # If the type is dish, then add to dish list
            case "Dish":
                # Check if the user already choose an image
                if self.selected_img_path.get() == "":
                    messagebox.showerror("", "Please choose image.")
                else:
                    try:
                        # Create a new dish object
                        dish = Dish (
                            self.new_name.get(),
                            save_image_new(self.new_name.get(), self.selected_img_path.get()),
                            save_ingredient_new(self.new_name.get(), ingredient_text.get("1.0", tk.END)),
                            save_instruction_new(self.new_name.get(), self.ins.get()),
                            self.nut[0],
                            self.nut[1]
                        )
                        
                        # Add the new dish to the dish list
                        self.list_dish.append(dish)
                        # Add the new dish to the data
                        self.data['list_dish'] = self.list_dish
                        # Save the data to the local storage
                        with open(self.filename, 'wb') as file:
                            pickle.dump(self.data, file)
                        
                        messagebox.showinfo("", "Added to Dish.")
                    
                    # Handle the error
                    except Exception as e:
                        messagebox.showerror("Error", "Please check error at your terminal")
                        print(f"Error : {e}")
            
            # If the type is dessert, then add to dessert list
            case "Dessert":
                # Check if the user already choose an image
                if self.selected_img_path.get() == "":
                    messagebox.showerror("", "Please choose image.")
                else:
                    try:
                        # Create a new dessert object
                        dessert = Dessert (
                            self.new_name.get(),
                            save_image_new(self.new_name.get(), self.selected_img_path.get()),
                            save_ingredient_new(self.new_name.get(), ingredient_text.get("1.0", tk.END)),
                            save_instruction_new(self.new_name.get(), self.ins.get()),
                            self.nut[0],
                            self.nut[1]
                        )
                        
                        # Add the new dessert to the dessert list
                        self.list_dessert.append(dessert)
                        # Add the new dessert to the data
                        self.data['list_dessert'] = self.list_dessert 
                        # Save the data to the local storage
                        with open(self.filename, 'wb') as file:
                            pickle.dump(self.data, file)
                        
                        messagebox.showinfo("", "Added to Dessert.")
                    
                    # Handle the error
                    except Exception as e:
                        messagebox.showerror("Error", "Please check error at your terminal")
                        print(f"Error : {e}")
            
            # If the type is snack, then add to snack list
            case "Snack":
                # Check if the user already choose an image
                if self.selected_img_path.get() == "":
                    messagebox.showerror("", "Please choose image.")
                else:
                    try:
                        # Create a new snack object
                        snack = Snack (
                            self.new_name.get(),
                            save_image_new(self.new_name.get(), self.selected_img_path.get()),
                            save_ingredient_new(self.new_name.get(), ingredient_text.get("1.0", tk.END)),
                            save_instruction_new(self.new_name.get(), self.ins.get()),
                            self.nut[0],
                            self.nut[1]
                        )
                        
                        # Add the new snack to the snack list
                        self.list_snack.append(snack)
                        # Add the new snack to the data
                        self.data['list_snack'] = self.list_snack 
                        # Save the data to the local storage
                        with open(self.filename, 'wb') as file:
                            pickle.dump(self.data, file)
                        
                        messagebox.showinfo("", "Added to Snack.")
                    
                    # Handle the error
                    except Exception as e:
                        messagebox.showerror("Error", "Please check error at your terminal")
                        print(f"Error : {e}")
            # Handle invalid type
            case _:
                messagebox.showerror("", "Invalid Type.")

# Function that will save the new image to the local storage
def save_image_new(name, old_image_path):
    new_image_path = PATH + name + ".jpg"
    # Copy the image to the local storage
    shutil.copy(old_image_path, new_image_path)
    return new_image_path

# Function that will save the new ingredient to the local storage
def save_ingredient_new(name, ingredient):
    new_ingredient_path = PATH + name + ".txt"
    
    # Check if the recipe already exist
    if os.path.exists(new_ingredient_path):
        # If the recipe already exist, then return error
        return FileExistsError("Recipe Already Exists.")
    else:
        with open(new_ingredient_path, 'w') as file:
            file.write(ingredient)
            # Return the ingredient path
            return new_ingredient_path

# Function that will save the new instruction to the local storage
def save_instruction_new(name, instruction):
    new_instruction_path = PATH + name + " Recipe.txt"
    
    # Check if the recipe already exist
    if os.path.exists(new_instruction_path):
        # If the recipe already exist, then return error
        return FileExistsError("Recipe Already Exists.")
    else:
        with open(new_instruction_path, 'w') as file:
            file.write(instruction)
        # Return the instruction path
        return new_instruction_path

# Function that update new ingredient to the local storage
def update_ingredient(menu_list, list_of_food, ingredients_label):
    selected_item = menu_list.selection()
    # Check if the user already choose a recipe
    if selected_item:
        selected_recipe = menu_list.item(selected_item, "text")
        # Loop through the list of food to find the recipe
        for menu in list_of_food:
            if menu.name == selected_recipe:
                with open(menu.get_ingredients(), 'w') as file:
                    new_ingredient = ""
                    
                    # Algorithm to save the new ingredient
                    for char in ingredients_label.get("1.0", tk.END).strip():
                        counter = 0
                        if counter == 1:
                            continue
                        if char == '-':
                            counter += 1
                        else:
                            new_ingredient += char
                    
                    # Write the new ingredient to the local storage
                    file.write(new_ingredient)
                messagebox.showinfo("", "Saved.")

# Function to open the nutrition form
def open_nutri_form(self):
    new_window = tk.Toplevel()
    new_window.title("Nutrition Form")
    
    entry_servings = tk.Entry(new_window, width=20)
    entry_servings.grid(row=0, column=1, padx=10, pady=5)
    entry_calories = tk.Entry(new_window, width=20)
    entry_calories.grid(row=1, column=1, padx=10, pady=5)
    entry_fat = tk.Entry(new_window, width=20)
    entry_fat.grid(row=2, column=1, padx=10, pady=5)
    entry_carbohydrates = tk.Entry(new_window, width=20)
    entry_carbohydrates.grid(row=3, column=1, padx=10, pady=5)
    entry_sugar = tk.Entry(new_window, width=20)
    entry_sugar.grid(row=4, column=1, padx=10, pady=5)
    entry_protein = tk.Entry(new_window, width=20)
    entry_protein.grid(row=5, column=1, padx=10, pady=5)
    entry_sodium = tk.Entry(new_window, width=20)
    entry_sodium.grid(row=6, column=1, padx=10, pady=5)
    
    
    label_serves = tk.Label(new_window, text="Serving:")
    label_serves.grid(row=0, column=0, padx=10, pady=5)
    label_calories = tk.Label(new_window, text="Calories (kcal):")
    label_calories.grid(row=1, column=0, padx=10, pady=5)
    label_fat = tk.Label(new_window, text="Fat (g):")
    label_fat.grid(row=2, column=0, padx=10, pady=5)
    label_carbohydrates = tk.Label(new_window, text="Carbohydrates (g):")
    label_carbohydrates.grid(row=3, column=0, padx=10, pady=5)
    label_sugar = tk.Label(new_window, text="Sugar (g):")
    label_sugar.grid(row=4, column=0, padx=10, pady=5)
    label_protein = tk.Label(new_window, text="Protein (g):")
    label_protein.grid(row=5, column=0, padx=10, pady=5)
    label_sodium = tk.Label(new_window, text="Sodium (mg):")
    label_sodium.grid(row=6, column=0, padx=10, pady=5)
    
    save_btn = tk.Button(new_window, text="Save", command=lambda: save_nutri(
        self,
        new_window,
        entry_servings.get(),
        entry_calories.get(),
        entry_fat.get(),
        entry_carbohydrates.get(),
        entry_sugar.get(),
        entry_protein.get(),
        entry_sodium.get(),
        ))
    save_btn.grid(row=7, column=0, columnspan=2, pady=10)

# Function to save the nutrition to variable
def save_nutri(self, new_window, servings, cals, fat, carbs, sugar, protein, sodium):
    chk_list = [servings, cals, fat, carbs, sugar, protein, sodium]
    
    # Check if the user input is valid
    for nutrient in chk_list:
        if is_float(nutrient):
            continue
        else:
            return messagebox.showerror("", "Invalid Input")
    
    # Create clone edamam's data structure
    data = {
        "ENERC_KCAL" : {
            "quantity" : float(cals)
        },
        "FAT" : {
            "quantity" : float(fat)
        },
        "CHOCDF" : {
            "quantity" : float(carbs)
        },
        "SUGAR" : {
            "quantity" : float(sugar)
        },
        "PROCNT" : {
            "quantity" : float(protein)
        },
        "NA" : {
            "quantity" : float(sodium)
        }
    }
    
    # Added data to a list
    self.nut.append(data)
    self.nut.append(servings)
    messagebox.showinfo("", "Nutrients Saved.")
    new_window.destroy()

# Function to check if the user input is valid
def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
