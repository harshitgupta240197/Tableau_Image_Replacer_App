import customtkinter as ctk
from customtkinter import filedialog
from PIL import Image, ImageTk
import shutil
import pandas as pd
import os
from datetime import datetime

def db_changer(file_path, create_to, db_name, find_content, replace_content):
    try:
        with open(file_path, 'r') as file:
            contents = file.read()
        contents = contents.replace(find_content, replace_content)
        source_file = file_path
        destination_file = file_path.rsplit('/', 1)[-1]
        destination_file = destination_file.replace('ccdemo.twb', (db_name + '.twb'))
        destination_file = create_to + '/' + destination_file
        shutil.copy(source_file, destination_file)
        with open(destination_file, 'w') as file:
            file.write(contents)
        return True
    except Exception as e:
        return False

def folder_creator(folder_path, folder_name):
    current_datetime = datetime.now()
    naming_variable = folder_name
    folder_name = naming_variable + '_' + str(current_datetime.year) + '_' + str(
        current_datetime.month) + '_' + str(current_datetime.day) + '_' + str(
        current_datetime.hour) + 'h' + str(current_datetime.minute) + 'm' + str(current_datetime.second) + 's'
    create_to = folder_path + folder_name
    os.makedirs(create_to, exist_ok=True)
    return create_to

def select_folder_path():
    folder_path = filedialog.askdirectory()
    if folder_path:
        entry_folder_path.delete(0, ctk.END)
        entry_folder_path.insert(0, folder_path)

def select_csv_file():
    csv_file = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if csv_file:
        entry_csv_file.delete(0, ctk.END)
        entry_csv_file.insert(0, csv_file)

def select_twb_files():
    twb_files = filedialog.askopenfilenames(filetypes=[("TWB files", "*.twb")])
    if twb_files:
        entry_twb_files.delete(0, ctk.END)
        entry_twb_files.insert(0, ', '.join(twb_files))

def select_image_path():
    image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if image_path:
        entry_image_path.delete(0, ctk.END)
        entry_image_path.insert(0, image_path)

def start_processing():
    new_folder_path = entry_folder_path.get()
    csv_file = entry_csv_file.get()
    twb_files = entry_twb_files.get().split(', ')
    find_content = entry_find_content.get()
    replace_content = entry_replace_content.get()
    image_name = entry_image_name.get()  # Get the image file name entered by the user
    new_image_path = entry_image_path.get()  # Get the selected new image path
    success_count = 0
    total_files = 0
    
    cm_clients = pd.read_csv(csv_file, header=None)
    databases = cm_clients[2]
    
    for x in range(len(cm_clients)):
        db_name = databases[x]
        for twb_file in twb_files:
            total_files += 1
            # Read the TWB file content
            with open(twb_file, 'r') as file:
                contents = file.read()
            # Replace the image path with the new path if image name found
            if image_name in contents:
                replaced_content = contents.replace(image_name, new_image_path)
                # Write the modified content back to the TWB file
                with open(twb_file, 'w') as file:
                    file.write(replaced_content)
                success_count += 1
    
    if success_count == total_files:
        ctk.messagebox.showinfo("Success", "All instances replaced successfully!")
    else:
        ctk.messagebox.showerror("Failure", f"Failed to replace {total_files - success_count} instance(s).")

# Create main window
root = ctk.CTk()
root.title("Image Replacer")
root.geometry("650x500")  # Set window size

# Apply dark theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# Load the image
logo_image = Image.open('./Logo.png')
logo_image = logo_image.resize((270, 70))
logo_image = ImageTk.PhotoImage(logo_image)

logo_label = ctk.CTkLabel(root, image=logo_image, text='')
logo_label.grid(row=0, column=0, columnspan=4, padx=10, pady=(20, 10))

# Create labels and entry fields with increased spacing
label_folder_path = ctk.CTkLabel(root, text="     Select Folder Path:", justify='right')
label_folder_path.grid(row=1, column=0, padx=10, pady=(15, 5))
entry_folder_path = ctk.CTkEntry(root, width=250)
entry_folder_path.grid(row=1, column=1, columnspan=2, padx=10, pady=(15, 5))
button_select_folder = ctk.CTkButton(root, text="Browse", command=select_folder_path)
button_select_folder.grid(row=1, column=3, padx=5, pady=(15, 5))

label_csv_file = ctk.CTkLabel(root, text="Select CSV File:", justify='right')
label_csv_file.grid(row=2, column=0, padx=10, pady=(10, 5))
entry_csv_file = ctk.CTkEntry(root, width=250)
entry_csv_file.grid(row=2, column=1, columnspan=2, padx=10, pady=(10, 5))
button_select_csv = ctk.CTkButton(root, text="Browse", command=select_csv_file)
button_select_csv.grid(row=2, column=3, padx=5, pady=(10, 5))

label_twb_files = ctk.CTkLabel(root, text="  Select TWB Files:", justify='right')
label_twb_files.grid(row=3, column=0, padx=10, pady=(10, 5))
entry_twb_files = ctk.CTkEntry(root, width=250)
entry_twb_files.grid(row=3, column=1, columnspan=2, padx=10, pady=(10, 5))
button_select_twb = ctk.CTkButton(root, text="Browse", command=select_twb_files)
button_select_twb.grid(row=3, column=3, padx=5, pady=(10, 5))

label_find_content = ctk.CTkLabel(root, text="       Enter Find Keyword:", justify='right')
label_find_content.grid(row=4, column=0, padx=10, pady=(10, 5))
entry_find_content = ctk.CTkEntry(root, width=250)
entry_find_content.grid(row=4, column=1, columnspan=2, padx=10, pady=(10, 5))

label_replace_content = ctk.CTkLabel(root, text="            Enter Replace Keyword:", justify='right')
label_replace_content.grid(row=5, column=0, padx=10, pady=(10, 5))
entry_replace_content = ctk.CTkEntry(root, width=250)
entry_replace_content.grid(row=5, column=1, columnspan=2, padx=10, pady=(10, 5))

# Add a label and entry field for entering the image file name
label_image_name = ctk.CTkLabel(root, text="     Enter Image File Name:", justify='right')
label_image_name.grid(row=6, column=0, padx=10, pady=(10, 5))
entry_image_name = ctk.CTkEntry(root, width=250)
entry_image_name.grid(row=6, column=1, columnspan=2, padx=10, pady=(10, 5))

# Add a label and entry field for selecting the new image path
label_image_path = ctk.CTkLabel(root, text="     Select New Image Path:", justify='right')
label_image_path.grid(row=7, column=0, padx=10, pady=(10, 5))
entry_image_path = ctk.CTkEntry(root, width=250)
entry_image_path.grid(row=7, column=1, columnspan=2, padx=10, pady=(10, 5))
button_select_image = ctk.CTkButton(root, text="Browse", command=select_image_path)
button_select_image.grid(row=7, column=3, padx=5, pady=(10, 5))

button_start = ctk.CTkButton(root, text="Start Processing", command=start_processing)
button_start.grid(row=8, column=0, columnspan=4, pady=15)

root.mainloop()
