import tkinter as tk
from tkinter import filedialog, ttk
import open3d as o3d
import requests
import os

def send_file_get_response(url, file_path, params):
    with open(file_path, 'rb') as file:
        files = {'file': (os.path.basename(file_path), file, 'application/octet-stream')}
        response = requests.post(url, files=files, data=params)

        if response.status_code != 200:
            print("Error in response:", response.status_code)
            return None

        return response

def browse_file():
    global filename, current_tab_name
    filename = filedialog.askopenfilename(filetypes=[("PLY files", "*.ply")])
    if filename:
        file_name_only = os.path.basename(filename)  # Extract the file name
        file_labels[current_tab_name].config(text=f"Selected File: {file_name_only}")

def process_all_point_clouds():
    global current_tab_name, param_entries, unique_param_entries

    # Retrieve common parameters
    common_params = {}
    for param in ["normalestaradius", "normalestamaxnn", "outlier_neighbours", "outlierstd_ratio"]:
        param_key = f"{current_tab_name}_{param}"
        common_params[param] = param_entries[param_key].get()

    # Retrieve unique parameter
   # Retrieve common parameters
    common_params = {
        "normalestaradius": param_entries[f"{current_tab_name}_normalestaradius"].get(),
        "normalestamaxnn": param_entries[f"{current_tab_name}_normalestamaxnn"].get(),
        "outlier_neighbours": param_entries[f"{current_tab_name}_outlier_neighbours"].get(),
        "outlierstd_ratio": param_entries[f"{current_tab_name}_outlierstd_ratio"].get()
    }

    # Retrieve unique parameter
    unique_param_value = unique_param_entries[current_tab_name].get()

    # Combine all parameters
    all_params = {**common_params, "unique_param": unique_param_value}

    # Send HTTP request with file and parameters
    url = processing_urls[current_tab_name]
    response = send_file_get_response(url, filename, all_params)

    with open('../Results/Result_Model.ply', 'wb') as f:
        f.write(response.content)

    mesh = o3d.io.read_triangle_mesh('../Results/Result_Model.ply')
    o3d.visualization.draw_geometries([mesh])

def visualize():
    global filename, current_tab_name
    point_cloud = o3d.io.read_point_cloud(filename)
    o3d.visualization.draw_geometries([point_cloud])

def on_tab_selected(event):
    global current_tab_name
    selected_tab_id = event.widget.select()
    current_tab_name = event.widget.tab(selected_tab_id, "text")



root = tk.Tk()
root.title("Point Cloud Processing")
root.geometry("600x600")

notebook = ttk.Notebook(root)
tabs = {}
file_labels = {}
param_entries = {}
unique_param_entries = {}  # Dictionary to store the unique parameter for each tab
processing_urls = {
    "Poisson": "http://localhost:5000/Poisson",
    "Alpha": "http://localhost:5000/AlphaShape",
    "BPA": "http://localhost:5000/BPA"
}
current_tab_name = "Poisson"  # Initialize with the name of the first tab

for tab_name in ["Poisson", "Alpha", "BPA"]:
    tabs[tab_name] = ttk.Frame(notebook)
    notebook.add(tabs[tab_name], text=tab_name)

    top_frame = ttk.Frame(tabs[tab_name], padding="10")
    top_frame.pack(expand=True, fill="both", pady=10)

    browse_button = ttk.Button(top_frame, text="Browse", command=browse_file)
    browse_button.pack(side=tk.LEFT, padx=10)

    file_labels[tab_name] = ttk.Label(top_frame, text="No File Selected")
    file_labels[tab_name].pack(side=tk.LEFT, padx=10)

    process_button = ttk.Button(top_frame, text="Process and Visualize", command=visualize)
    process_button.pack(side=tk.LEFT, padx=10)

    bottom_frame = ttk.Frame(tabs[tab_name], padding="10")
    bottom_frame.pack(expand=True, fill="both", pady=10)

    param_names = ["normalestaradius", "normalestamaxnn", "outlier_neighbours", "outlierstd_ratio"]
    for i, param in enumerate(param_names):
        ttk.Label(bottom_frame, text=param).grid(row=i, column=0, padx=5, pady=5, sticky=tk.W)
        param_entries[f"{tab_name}_{param}"] = ttk.Entry(bottom_frame, width=10)
        param_entries[f"{tab_name}_{param}"].grid(row=i, column=1, padx=5, pady=5, sticky=tk.W)
    
    # Adding unique parameter based on the tab name
    unique_param_label = {"Poisson": "Depth", "Alpha": "Alpha", "BPA": "Radius"}
    unique_param_name = unique_param_label[tab_name]
    ttk.Label(bottom_frame, text=unique_param_name).grid(row=len(param_names), column=0, padx=5, pady=5, sticky=tk.W)
    unique_param_entries[tab_name] = ttk.Entry(bottom_frame, width=10)
    unique_param_entries[tab_name].grid(row=len(param_names), column=1, padx=5, pady=5, sticky=tk.W)
    
    bottom_frame.grid_columnconfigure(1, weight=1)

notebook.pack(expand=True, fill="both", pady=10)
notebook.bind("<ButtonRelease-1>", on_tab_selected)

# Global process button at the bottom of the window
global_process_button = ttk.Button(root, text="Process All Point Clouds", command=process_all_point_clouds)
global_process_button.pack(side=tk.BOTTOM, pady=10)

root.mainloop()