import customtkinter
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import messagebox
import pickle
from app import SmartRecipesBook
from PIL import ImageTk, Image

# Set the appearance mode to system
customtkinter.set_appearance_mode("system")


# Function that create a new file
def new_file():
    file_path = asksaveasfilename(
        title="Save As",
        filetypes=[("DAT files", "*.dat"), ("Pickle Files", "*.pkl")]
    )

    if file_path:
        # Create a new file
        with open(file_path, "wb") as file:
            data = {'list_dish': [], 'list_dessert': [], 'list_snack': []}
            pickle.dump(data ,file)
        
        # Load the new file to app
        with open(file_path, "rb") as file:
            data = pickle.load(file)
        messagebox.showinfo("Created", f"File created at: {file_path}")
        launch_main_app(data, file_path)

# Function that choose a file
def choose_file():
    try:
        filename = askopenfilename()
        
        # Load the file to app
        if filename:
            with open(filename, 'rb') as file:
                data = pickle.load(file)
            launch_main_app(data, filename)
    
    # Handle the error
    except (EOFError, pickle.UnpicklingError):
        messagebox.showerror("Error", "Invalid or corrupted pickle file.")

# Function that launch the main app
def launch_main_app(data, file_path):
    root.destroy()  # Close the current window before opening the main app
    SmartRecipesBook(data, file_path)

root = customtkinter.CTk()

# Set the window to the center of the screen
width_app, height_app = 640, 360
width, height = root.winfo_screenwidth(), root.winfo_screenheight()
x_cor = (width / 2) - (width_app / 2)
y_cor = (height / 2) - (height_app / 2)

root.geometry("%dx%d+%d+%d" % (width_app, height_app, x_cor, y_cor))

root.geometry("640x360")

# Remove the title bar
root.overrideredirect(1)

# Set the background image
bg_img = ImageTk.PhotoImage(Image.open("./assets/bg.jpg"))
l1 = customtkinter.CTkLabel(master=root, image=bg_img, text="")
l1.pack()

# Create new file button
new_file_btn = customtkinter.CTkButton(root, text="Create a new file.", command=new_file, 
                                          width=150, height=100, corner_radius=6,
                                          fg_color="white", border_color="#FF7A5E", text_color="#FF7A5E",
                                          hover_color="#D9C9C6",
                                          border_width=2.5,
                                          font=("Arial", 14))
new_file_btn.place(relx=0.15, rely=0.35)

# Create choose file button
choose_file_btn = customtkinter.CTkButton(root, text="Choose a file.", command=choose_file, 
                                          width=150, height=100, corner_radius=6,
                                          fg_color="white", border_color="#FF7A5E", text_color="#FF7A5E",
                                          hover_color="#D9C9C6",
                                          border_width=2.5,
                                          font=("Arial", 14))
choose_file_btn.place(relx=0.6, rely=0.35)


root.mainloop()
