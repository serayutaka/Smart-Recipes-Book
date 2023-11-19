import webbrowser
import pickle
import customtkinter
from PIL import Image, ImageTk

from menu_c import Dish, Dessert, Snack
from helpers import *
from constant import PATH

# Set the appearance mode to system
customtkinter.set_appearance_mode("system")

# Main app (Smart Recipes Book object)
class SmartRecipesBook(object):
    
    # Constructor that initialize the main app
    def __init__(self, data, filename): # data is a dictionary that contain the list of menu and filename is the path of the file
        
        # Import here to avoid circular import
        from tkinter import ttk
        
        # Initialize the main app
        self.data = data
        self.list_dish = data['list_dish']
        self.list_dessert = data['list_dessert']
        self.list_snack = data['list_snack']
        self.filename = filename
        
        root = customtkinter.CTk()
        
        # Set the window to the center of the screen
        width_app, height_app = 600, 825
        width, height = root.winfo_screenwidth(), root.winfo_screenheight()
        x_cor = (width / 2) - (width_app / 2)
        y_cor = (height / 2) - (height_app / 2)
        
        root.geometry("%dx%d+%d+%d" % (width_app, height_app, x_cor, y_cor))
        root.title("Smart Recipes Book")
        
        # Remove the title bar
        root.overrideredirect(1)
        
        # Create the menu bar
        notebook = ttk.Notebook(root)
        notebook.pack(expand = True, fill="both")
        self.home(root, notebook)
        self.search(notebook)
        self.add(notebook)
        self.list_of_menu(notebook)
        
        root.mainloop()
    
    # Function that create home tab
    def home(self, root, notebook):
        # Import here to avoid circular import
        from tkinter import ttk
        
        # Create the home frame(root)
        home_frame = ttk.Frame(notebook)
        home_frame.pack(fill="both", expand=True)
        
        # Set the background image
        bg_img = ImageTk.PhotoImage(Image.open("./assets/bg_re.jpg"))
        l1 = customtkinter.CTkLabel(master=home_frame, image=bg_img, text="")
        l1.pack()
        
        # Create the welcome label
        welcome_label = customtkinter.CTkLabel(home_frame, text="Welcome",
                                            fg_color="#EDEDED", font=("Arial", 52),
                                            text_color="Black", corner_radius=6,
                                            padx=2, pady=2)
        welcome_label.place(relx=0.05, rely=0.05)
        
        # Create the to label
        to_label = customtkinter.CTkLabel(home_frame, text="to",
                                            fg_color="Black", font=("Arial", 52),
                                            text_color="White", corner_radius=6,
                                            padx=2, pady=2)
        to_label.place(relx=0.05, rely=0.25)
        
        # Create the smart recipes book label
        smt_label = customtkinter.CTkLabel(home_frame, text="Smart Recipes Book",
                                            fg_color="#EDEDED", font=("Arial", 52),
                                            text_color="Black", corner_radius=6,
                                            padx=2, pady=2)
        smt_label.place(relx=0.05, rely=0.45)
        
        # Create the made with love label
        made_wth_love_label = customtkinter.CTkLabel(home_frame, text="made with 💖 by @serayutaka",
                                            fg_color="Black", font=("Arial", 36),
                                            text_color="#D8FFFF", corner_radius=6,
                                            padx=2, pady=2)
        made_wth_love_label.place(relx=0.05, rely=0.65)
        
        # Create the exit button
        exit_btn = customtkinter.CTkButton(home_frame, width=150, height=50, text="Exit",
                                           font=("Arial", 24), border_color="Black", fg_color="#EDEDED",
                                           border_width=2.5, text_color="Black", hover_color="#D0D0D0",
                                           command=lambda: root.destroy())
        exit_btn.place(relx=0.35, rely=0.8)

        notebook.add(home_frame, text="Home")

    # Function that create search tab
    def search(self, notebook):
        # Import here to avoid circular import
        from tkinter import ttk
        
        # Create the search frame(root)
        search_frame = ttk.Frame(notebook)
        search_frame.pack()
        
        # Set the background image
        bg_img = ImageTk.PhotoImage(Image.open("./assets/bg2.jpg"))
        l1 = customtkinter.CTkLabel(master=search_frame, image=bg_img, text="")
        l1.pack()
        
        # Create the search label
        self.entry = customtkinter.CTkEntry(search_frame, placeholder_text="ex. Egg Fried Rice", width=300)
        
        # Create the search button
        loupe_img = customtkinter.CTkImage(Image.open("./assets/loupe.png"))
        button = customtkinter.CTkButton(search_frame, text="Search",
                                         border_color="Black", fg_color="#EDEDED", image=loupe_img,
                                         border_width=2.5, text_color="Black", hover_color="#D0D0D0",
                                         compound="right", command=self.run_search_query) # Command is search for the recipe
        
        self.entry.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        button.place(relx=0.5, rely=0.165, anchor=tk.CENTER)
        
        search_frame.columnconfigure(0, weight=1)
        search_frame.columnconfigure(1, weight=1)
        
        exten_frame = ttk.Frame(search_frame)
        exten_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.exten_frame = exten_frame
        
        bottom_frame = ttk.Frame(search_frame)
        bottom_frame.place(relx=0.5, rely=0.9, anchor="center")
        self.bottom_frame = bottom_frame
        
        # Create a list of menu
        self.menu_list = ttk.Treeview(exten_frame, columns="name")
        self.menu_list.heading("#0", text="Name", anchor=tk.W)
        self.menu_list.column("#0", width=400)
        self.menu_list.column("#1", width=0, stretch=tk.NO)
        self.menu_list.grid()
        
        notebook.add(search_frame, text="Search")
    
    # Function that create add tab
    def add(self, notebook):
        # Import here to avoid circular import
        from tkinter import ttk
        
        # Create the add frame(root)
        add_frame = ttk.Frame(notebook)
        add_frame.pack( side = tk.TOP )
        notebook.add(add_frame, text="Add")
        
        # Name label and entry label under the name label
        ttk.Label(add_frame, text="Name").pack()
        self.new_name = ttk.Entry(add_frame, width=50)
        self.new_name.pack()
        
        # Picture frame
        picture_frame = ttk.Frame(add_frame)
        picture_frame.place(relx=0.5, rely=0.35, anchor="center")
        photo_label = tk.Label(picture_frame)
        photo_label.pack()
        
        # Ingredients frame and ingredients text box
        ingredients_frame = ttk.Frame(add_frame)
        ingredients_frame.place(relx=0.5, rely=0.75, anchor="center")
        ingredient_text = customtkinter.CTkTextbox(ingredients_frame, border_width=2.5, corner_radius=7,
                                                  font=("Arial", 14), width=400, height=250,
                                                  border_color="Black")
        ingredient_text.grid(row=1, column=1)
        
        # Create the button frame
        btn_frame = ttk.Frame(add_frame)
        btn_frame.pack( side= tk.BOTTOM )
        
        # Create a dropdown menu
        self.create_dropdown(btn_frame)
        
        # Create the add image button
        add_img_btn = ttk.Button(btn_frame, text="Add Images", command=lambda: choose_image_path(self, photo_label)) # Command is to choose the image
        add_img_btn.grid(row=1, column=1)
        self.selected_img_path = tk.StringVar()
        
        # Create the add ingredient button
        self.ins = tk.StringVar()
        add_ins_btn = ttk.Button(btn_frame, text="Add Instruction", command=lambda: open_instruction(self)) # Command is to open the instruction text box
        add_ins_btn.grid(row=1, column=2)
        
        # Create the add nutrition button
        self.nut = []
        add_nut_btn = ttk.Button(btn_frame, text="Add Nutrition", command=lambda: open_nutri_form(self)) # Command is to open the nutrition form
        add_nut_btn.grid(row=1, column=3)
        
        # Create the save button
        save_btn = ttk.Button(btn_frame, text="Add Recipe", command=lambda: save_recipe(self, ingredient_text)) # Command is to save the recipe
        save_btn.grid(row=2, column=0, columnspan=4)
    
    # Fuction that create a dropdown menu
    def create_dropdown(self, btn_frame):
        from tkinter import ttk
        options = ["Dish", "Dessert", "Snack"]
        self.selected_option = tk.StringVar()
        self.selected_option.set(options[0])
        dropdown = ttk.Combobox(btn_frame, textvariable=self.selected_option, values=options)
        dropdown.grid(row=1, column=0)
        dropdown.bind("<<ComboboxSelected>>", self.on_dropdown_change)
        self.selected_label = ttk.Label(btn_frame, text="Dish")
        self.selected_label.grid(row=0, column=0)
    
    # Function that change the label of the dropdown menu
    def on_dropdown_change(self, event):
        selected_option = self.selected_option.get()
        self.selected_label.configure(text=selected_option)
    
    # Function that create a list of menu tab
    def list_of_menu(self, notebook):
        # Import here to avoid circular import
        from tkinter import ttk
        
        # Create the list of menu frame(root)
        list_of_menu_frame = ttk.Frame(notebook)
        list_of_menu_frame.pack()
        
        # Set the background image
        bg_img = ImageTk.PhotoImage(Image.open("./assets/bg3.jpg"))
        l1 = customtkinter.CTkLabel(master=list_of_menu_frame, image=bg_img, text="")
        l1.pack()
        
        # Create a dish button
        dish_img = customtkinter.CTkImage(Image.open("./assets/dish.png"))
        dish_btn = customtkinter.CTkButton(list_of_menu_frame, width=150, height=50, text="Dish",
                                           font=("Arial", 24), border_color="Black", fg_color="#EDEDED",
                                           border_width=2.5, text_color="Black", hover_color="#D0D0D0",
                                           image=dish_img, compound="right", command=lambda: self.open_menu("Dishes")) # Command is to open the list of dishes
        dish_btn.place(relx=0.35, rely=0.2)
        
        # Create a dessert button
        dessert_img = customtkinter.CTkImage(Image.open("./assets/sweets.png"))
        dessert_btn = customtkinter.CTkButton(list_of_menu_frame, width=150, height=50, text="Dessert",
                                           font=("Arial", 24), border_color="Black", fg_color="#EDEDED",
                                           border_width=2.5, text_color="Black", hover_color="#D0D0D0",
                                           image=dessert_img, compound="right", command=lambda: self.open_menu("Desserts")) # Command is to open the list of desserts
        dessert_btn.place(relx=0.35, rely=0.45)
        
        # Create a snack button
        snack_img = customtkinter.CTkImage(Image.open("./assets/snack.png"))
        snack_btn = customtkinter.CTkButton(list_of_menu_frame, width=150, height=50, text="Snack",
                                            font=("Arial", 24), border_color="Black", fg_color="#EDEDED",
                                           border_width=2.5, text_color="Black", hover_color="#D0D0D0",
                                           image=snack_img, compound="right", command=lambda: self.open_menu("Snacks")) # Command is to open the list of snacks
        snack_btn.place(relx=0.35, rely=0.7)
        
        notebook.add(list_of_menu_frame, text="List of Menu")
    
    # Function that run the search query
    def run_search_query(self):
        # Import here to avoid circular import
        from tkinter import messagebox
        
        # Get the query from the entry
        query = self.entry.get()
        recipe = search_recipe(query) # Search for the recipe
        
        # Check if the recipe is found
        if recipe["more"]:
            # Delete the previous menu
            if len(self.menu_list.get_children()) > 0:
                for item in self.menu_list.get_children():
                    self.menu_list.delete(item)
            # Insert the new menu
            for recipe_label in recipe["hits"]:
                self.menu_list.insert("", tk.END, text=recipe_label["recipe"]["label"])
            
            # Crate the select button
            customtkinter.CTkButton(self.bottom_frame, text="Select", command=self.show_recipe,
                                    border_color="Black", fg_color="#EDEDED",
                                    border_width=2.5, text_color="Black", hover_color="#D0D0D0").grid(row=0, column=0) # Command is to show the recipe
        
        # If the recipe is not found
        else:
            messagebox.showerror("QueryError", "Can't find recipe.") 
    
    # Function that show the recipe
    def show_recipe(self):
        selected = self.menu_list.selection()
        # Check if the recipe is selected
        if selected:
            # Get the recipe from the API
            data = get_recipe(self.menu_list.item(selected)["text"])

            # Create a new window (root)
            new_window = customtkinter.CTkToplevel(fg_color="White")
            new_window.geometry("600x700")
            new_window.title(data["recipe"]["label"])
            
            # Name of the recipe label
            menu_label = customtkinter.CTkLabel(new_window, text=data["recipe"]["label"], font=("Segoe Script", 16))
            menu_label.place(relx=0.35, rely=0.025)
            
            # Create the image frame and image label
            image_frame = tk.Frame(new_window)
            image_frame.place(relx=0.49, rely=0.3, anchor="center")
            photo = read_images_url(data["recipe"]["image"])
            photo_label = tk.Label(image_frame)
            photo_label.pack()
            photo_label.configure(image=photo)
            photo_label.photo = photo
            
            # Create the ingredient label (text box)
            ingredient = customtkinter.CTkTextbox(new_window, border_width=2.5, corner_radius=7,
                                                  font=("Arial", 14), width=400, height=250,
                                                  border_color="Black")
            ingredient.place(relx=0.16, rely=0.525)
            
            # Insert the ingredient to the ingredient label
            ingredient.delete("1.0", tk.END)
            for ingredient_name in data["recipe"]["ingredientLines"]:
                if ingredient_name == data["recipe"]["ingredientLines"][-1]:
                    ingredient.insert(tk.END, "- " + ingredient_name)
                    break
                ingredient.insert(tk.END, "- " + ingredient_name + '\n')
            
            # Create browser button
            btn_browser = customtkinter.CTkButton(new_window, text="Open in Browser",
                                                  corner_radius=6, fg_color="white", border_color="#FF7A5E", text_color="#FF7A5E",
                                                  hover_color="#D9C9C6", border_width=2.5, font=("Arial", 14),
                                                  command=lambda: webbrowser.open(data["recipe"]["url"])) # Command is to open the recipe in the browser
            btn_browser.place(relx=0.35, rely=0.9)
            
            # Create save button
            btn_save = customtkinter.CTkButton(new_window, text="Save Recipe",
                                               corner_radius=6, fg_color="white", border_color="#FF7A5E", text_color="#FF7A5E",
                                               hover_color="#D9C9C6", border_width=2.5, font=("Arial", 14),
                                               command=self.save_recipe) # Command is to save the recipe
            btn_save.place(relx=0.35, rely=0.95)
    
    # Function that save the recipe
    def save_recipe(self):
        selected = self.menu_list.selection()
        
        # Check if the recipe is selected
        if selected:
            # Get the recipe from the API
            data = get_recipe(self.menu_list.item(selected)["text"])
            
            # Save the recipe
            chk_img = save_image(data["recipe"]["image"], PATH + data["recipe"]["label"] + ".jpg")
            chk_ing = save_ingredient(data["recipe"]["ingredientLines"], PATH + data["recipe"]["label"] + ".txt")
            chk_ins = save_default_instruction(PATH + data["recipe"]["label"] + " Recipe.txt")
            
            # Check if the recipe is saved
            if chk_img == True and chk_ing == True and chk_ins == True:
                messagebox.showinfo("", "Saved.")
            # If the recipe is not saved
            else:
                messagebox.showerror("", "Error to Save.")
                return
            
            chk_snack = data["recipe"]["mealType"]
            chk_dessert = data["recipe"]["dishType"]
            
            # Check if the recipe is snack
            if chk_snack[0] == "snack":
                name = data["recipe"]["label"]
                nutrition_data = data["recipe"]["totalNutrients"]
                
                # Create a snack object
                snack = Snack(name, PATH + name + ".jpg", PATH + name + ".txt", PATH + name + " Recipe.txt",
                            nutrition_data, data["recipe"]["yield"])
                
                # Append the snack object to the list of snack
                self.list_snack.append(snack)
                # Update the data
                self.data['list_snack'] = self.list_snack 
                # Save the data
                with open(self.filename, 'wb') as file:
                    pickle.dump(self.data, file)
            
            # Check if the recipe is dessert
            elif chk_dessert[0] == "desserts" or chk_dessert[0] == "sweets":
                name = data["recipe"]["label"]
                nutrition_data = data["recipe"]["totalNutrients"]
                
                # Create a dessert object
                dessert = Dessert(name, PATH + name + ".jpg", PATH + name + ".txt", PATH + name + " Recipe.txt",
                                nutrition_data, data["recipe"]["yield"])
                
                # Append the dessert object to the list of dessert
                self.list_dessert.append(dessert)
                # Update the data
                self.data['list_dessert'] = self.list_dessert
                # Save the data
                with open(self.filename, 'wb') as file:
                    pickle.dump(self.data, file)
            
            # If the recipe is dish
            else:
                name = data["recipe"]["label"]  
                nutrition_data = data["recipe"]["totalNutrients"]
                
                # Create a dish object
                dish = Dish(name, PATH + name + ".jpg", PATH + name + ".txt", PATH + name + " Recipe.txt",
                            nutrition_data, data["recipe"]["yield"])
                
                # Append the dish object to the list of dish
                self.list_dish.append(dish)
                # Update the data
                self.data['list_dish'] = self.list_dish
                # Save the data
                with open(self.filename, 'wb') as file:
                    pickle.dump(self.data, file)
    
    # Function that open menu lists
    def open_menu(self, type):
        # Check type of the menu
        match type:
            # Open the list of dishes
            case "Dishes":
                self.menu_template(type, self.list_dish)
            # Open the list of desserts
            case "Desserts":
                self.menu_template(type, self.list_dessert)
            # Open the list of snacks
            case "Snacks":
                self.menu_template(type, self.list_snack)
    
    # Function that create a menu template
    def menu_template(self, type, list_of_food):
        # Import here to avoid circular import
        from tkinter import ttk
        
        # Create a new window (root)
        new_window = tk.Toplevel()
        new_window.geometry("650x800")
        new_window.title(type)
        new_window.state('zoomed')
        
        # Create menu list
        menu_list = ttk.Treeview(new_window, columns="name")
        menu_list.heading("#0", text="Name", anchor=tk.W)
        menu_list.column("#0", width=400)
        menu_list.column("#1", width=0, stretch=tk.NO)
        menu_list.place(relx=0.2, rely=0.5, anchor="center")
        
        # Insert the menu to the menu list
        i = 0
        for food in list_of_food:
            menu_list.insert("", tk.END, text=food.name, tags=(i,))
            i += 1
        
        # Name of the menu label
        label = customtkinter.CTkLabel(new_window, text="", font=("Segoe Script", 16))
        label.place(relx=0.55, rely=0.1, anchor="center")
        
        # Ingredients label (text box)
        ingredients_label = customtkinter.CTkTextbox(new_window, border_width=2.5, corner_radius=7,
                                                        font=("Arial", 14), width=400, height=250,
                                                        border_color="Black")
        ingredients_label.place(relx=0.448, rely=0.48)
        
        # Picture frame and picture label
        picture_frame = ttk.Frame(new_window)
        picture_frame.place(relx=0.55, rely=0.3, anchor="center")
        picture_label = tk.Label(picture_frame)
        picture_label.pack()
        
        # Create the button frame
        btn_frame = ttk.Frame(new_window)
        btn_frame.place(relx=0.55, rely=0.8, anchor="center")
        # Create instruction button
        btn_instruction = ttk.Button(btn_frame, text="Open Instruction", command=lambda: self.open_instruction(menu_list, chk="dishes")) # Command is to open the instruction text box
        btn_instruction.grid(row=1, column=1)
        # Create save new ingredient button
        btn_edit = ttk.Button(btn_frame, text="Save new ingredient.", command=lambda: update_ingredient(menu_list, list_of_food, ingredients_label)) # Command is to update the ingredient
        btn_edit.grid(row=1, column=2)
        
        # 'Nutrition Facts' label
        topic_nut_lbl = customtkinter.CTkLabel(new_window, text="Nutrition Facts", font=("Arial", 30), justify=tk.LEFT,
                                        fg_color="White", text_color="Black", corner_radius=7)
        topic_nut_lbl.place(relx=0.81, rely=0.18, anchor="center")
        
        # Nutrition variables
        serving = tk.StringVar()
        calories = tk.StringVar()
        fat = tk.StringVar()
        sodium = tk.StringVar()
        carb = tk.StringVar()
        protein = tk.StringVar()
        sugar = tk.StringVar()
        
        # Serving label
        serving_label = customtkinter.CTkLabel(new_window, text="")
        serving_label.place(relx=0.7, rely=0.25)
        
        # Calories label
        calories_label = customtkinter.CTkLabel(new_window, text="")
        calories_label.place(relx=0.7, rely=0.31)
        
        # Fat label
        fat_label = customtkinter.CTkLabel(new_window, text="")
        fat_label.place(relx=0.7, rely=0.37)
        
        # Sodium label
        na_label = customtkinter.CTkLabel(new_window, text="")
        na_label.place(relx=0.7, rely=0.43)
        
        # Carbohydrates label
        carb_label = customtkinter.CTkLabel(new_window, text="")
        carb_label.place(relx=0.7, rely=0.49)
        
        # Protein label
        prot_label = customtkinter.CTkLabel(new_window, text="")
        prot_label.place(relx=0.7, rely=0.55)
        
        # Sugar label
        sugar_label = customtkinter.CTkLabel(new_window, text="")
        sugar_label.place(relx=0.7, rely=0.43)
        
        # Bind the menu list to show the selected item
        menu_list.bind("<<TreeviewSelect>>", lambda event: self.show_selected_item(
            event, menu_list, label, list_of_food,
            ingredients_label, picture_label, serving,
            calories, fat, sodium, carb, protein, sugar,
            serving_label, calories_label, fat_label, na_label, carb_label, prot_label, sugar_label)) 
    
    # Function that show the selected item
    def show_selected_item(self, event, menu_list, label, list_of_food, ingredients_label, photo_label,
                           serving, calories, fat, sodium, carb, protein, sugar,
                           serving_label, calories_label, fat_label, na_label, carb_label, prot_label, sugar_label):
        selected_item = menu_list.selection()
        
        # Check if the item is selected
        if selected_item:
            selected_index = menu_list.item(selected_item, "tags")[0]
            selected_recipe = list_of_food[int(selected_index)]
            
            # Name of the menu label
            label.configure(text=menu_list.item(selected_item)["text"])
            
            # Insert the ingredient to the ingredient label
            ingredients_label.delete("1.0", tk.END)
            ingredients_label.insert(tk.INSERT, '- ')
            for ingredient in read_ingredients(selected_recipe.get_ingredients()):
                if ingredient != '\n':
                    ingredients_label.insert(tk.INSERT, ingredient)
                else:
                    ingredients_label.insert(tk.INSERT, ingredient + '- ')
            
            # Insert the image to the image label
            photo = read_images_path(selected_recipe.get_image())
            photo_label.configure(image=photo) 
            photo_label.photo = photo
            
            # Check the type of the menu
            match selected_recipe:
                # If the menu is dish
                case Dish():
                    # Get the nutritions of the dish
                    nutritions = selected_recipe.get_nutrition()
                    serving.set(nutritions["Servings"])
                    calories.set(format(nutritions["Calories"], ".2f"))
                    fat.set(format(nutritions["Fat"], ".2f"))
                    sodium.set(format(nutritions["Sodium"], ".2f"))
                    carb.set(format(nutritions["Carbohydrates"], ".2f"))
                    protein.set(format(nutritions["Protein"], ".2f"))
                    
                    sugar_label.destroy()
                    
                    serving_label.configure(text=f"Serving Size: {serving.get()}", font=("Arial", 26), justify=tk.LEFT,
                                         fg_color="#ffadad", text_color="Black", corner_radius=7)
                    
                    calories_label.configure(text=f"Calories: {calories.get()} kcal", font=("Arial", 26), justify=tk.LEFT,
                                         fg_color="#FFD6A5", text_color="Black", corner_radius=7)
                    
                    fat_label.configure(text=f"Fat: {fat.get()} g", font=("Arial", 26), justify=tk.LEFT,
                                         fg_color="#FDFFB6", text_color="Black", corner_radius=7)
                    
                    na_label.configure(text=f"Sodium: {sodium.get()} mg", font=("Arial", 26), justify=tk.LEFT,
                                         fg_color="#9BF6FF", text_color="Black", corner_radius=7)
                    
                    carb_label.configure(text=f"Carbohydrates: {carb.get()} g", font=("Arial", 26), justify=tk.LEFT,
                                         fg_color="#BDB2FF", text_color="Black", corner_radius=7)
                    
                    prot_label.configure(text=f"Protein: {protein.get()} g", font=("Arial", 26), justify=tk.LEFT,
                                         fg_color="#CAFFBF", text_color="Black", corner_radius=7)
                    
                # If the menu is dessert
                case Dessert():
                    # Get the nutritions of the dessert
                    nutritions = selected_recipe.get_nutrition()
                    serving.set(nutritions["Servings"])
                    calories.set(format(nutritions["Calories"], ".2f"))
                    fat.set(format(nutritions["Fat"], ".2f"))
                    sugar.set(format(nutritions["Sugar"], ".2f"))
                    carb.set(format(nutritions["Carbohydrates"], ".2f"))
                    
                    prot_label.destroy()
                    na_label.destroy()
                    
                    serving_label.configure(text=f"Serving Size: {serving.get()}", font=("Arial", 26), justify=tk.LEFT,
                                         fg_color="#97F9F9", text_color="Black", corner_radius=7)
                    
                    calories_label.configure(text=f"Calories: {calories.get()} kcal", font=("Arial", 26), justify=tk.LEFT,
                                         fg_color="#A4DEF9", text_color="Black", corner_radius=7)
                    
                    fat_label.configure(text=f"Fat: {fat.get()} g", font=("Arial", 26), justify=tk.LEFT,
                                         fg_color="#C1E0F7", text_color="Black", corner_radius=7)
                    
                    sugar_label.configure(text=f"Sugar: {sugar.get()} g", font=("Arial", 26), justify=tk.LEFT,
                                         fg_color="#CFBAE1", text_color="Black", corner_radius=7)
                    
                    carb_label.configure(text=f"Carbohydrates: {carb.get()} g", font=("Arial", 26), justify=tk.LEFT,
                                         fg_color="#C59FC9", text_color="Black", corner_radius=7)
                
                # If the menu is snack
                case Snack():
                    # Get the nutritions of the snack
                    nutritions = selected_recipe.get_nutrition()
                    serving.set(nutritions["Servings"])
                    calories.set(format(nutritions["Calories"], ".2f"))
                    sugar.set(format(nutritions["Sugar"], ".2f"))
                    fat.set(format(nutritions["Fat"], ".2f"))
                    sodium.set(format(nutritions["Sodium"], ".2f"))
                    
                    prot_label.destroy()
                    carb_label.destroy()
                    
                    serving_label.configure(text=f"Serving Size: {serving.get()}", font=("Arial", 26), justify=tk.LEFT,
                                         fg_color="#D8E2DC", text_color="Black", corner_radius=7)
                    
                    calories_label.configure(text=f"Calories: {calories.get()} kcal", font=("Arial", 26), justify=tk.LEFT,
                                         fg_color="#FFE5D9", text_color="Black", corner_radius=7)
                    
                    fat_label.configure(text=f"Fat: {fat.get()} g", font=("Arial", 26), justify=tk.LEFT,
                                         fg_color="#FFCAD4", text_color="Black", corner_radius=7)
                    
                    sugar_label.configure(text=f"Sugar: {sugar.get()} g", font=("Arial", 26), justify=tk.LEFT,
                                         fg_color="#F4ACB7", text_color="Black", corner_radius=7)
                    
                    na_label.configure(text=f"Sodium: {sodium.get()} mg", font=("Arial", 26), justify=tk.LEFT,
                                         fg_color="#9D8189", text_color="White", corner_radius=7)
                    na_label.place(relx=0.7, rely=0.49)
                    
    def open_instruction(self, menu_list, chk):
        selected_item = menu_list.selection()
        
        # Check if the item is selected
        if selected_item:
            selected_index = menu_list.item(selected_item, "tags")[0]
            
            # Check the type of the menu
            match chk:
                # If the menu is dish
                case "dishes":
                    # Get the recipe from the list of dish
                    selected_recipe = self.list_dish[int(selected_index)]
                # If the menu is dessert
                case "desserts":
                    # Get the recipe from the list of dessert
                    selected_recipe = self.list_dessert[int(selected_index)]
                # If the menu is snack
                case "snacks":
                    # Get the recipe from the list of snack
                    selected_recipe = self.list_snack[int(selected_index)]
            
            # Create a new window (root)
            new_window = customtkinter.CTkToplevel()
            new_window.geometry("640x360")
            new_window.title("Instruction")
            
            # Set the background image
            bg_img = ImageTk.PhotoImage(Image.open("./assets/bg.jpg"))
            l1 = customtkinter.CTkLabel(master=new_window, image=bg_img, text="")
            l1.pack()
            
            # Create the instruction label (text box)
            instruction_text = customtkinter.CTkTextbox(new_window, corner_radius=7, font=("Arial", 14),
                                                        width=500, height=300)
            instruction_text.place(relx=0.11, rely=0.05)
            
            # Insert the instruction to the instruction label
            for instruction in read_instruction(selected_recipe.get_instructions()):
                instruction_text.insert("insert", instruction)
            
            # Create the save button
            btn_save = customtkinter.CTkButton(new_window, text="Save", corner_radius=6, fg_color="white", 
                                               border_color="#FF7A5E", text_color="#FF7A5E",
                                               hover_color="#D9C9C6", border_width=2.5, font=("Arial", 14),
                                               command=lambda: save_instruction(instruction_text, selected_recipe, new_window)) # Command is to save the instruction
            btn_save.place(relx=0.4, rely=0.9)
            
