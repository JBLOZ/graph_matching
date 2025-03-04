import os
import pandas as pd

class DataLoader:
    def __init__(self, base_dir='./archivos/WILLOW-ObjectClass'):
        """
        Inicializa la clase DataLoader con el directorio base.
        """
        self.base_dir = base_dir
        self.dataframes = {}

    def load_data(self):
        """
        Carga los datos de cada carpeta dentro del directorio base.
        Se espera que cada carpeta contenga archivos .png y .mat con nombres emparejados.
        Retorna un diccionario con un DataFrame por categoría.
        """
        self.dataframes = {}
        
        # Iterar sobre cada categoría en el directorio base
        for category in os.listdir(self.base_dir):
            
            cat_path = os.path.join(self.base_dir, category)
            if not os.path.isdir(cat_path):
                continue

            # Diccionario para asociar imágenes y archivos .mat por nombre base
            file_dict = {}

            for file in os.listdir(cat_path):

                file_path = os.path.join(cat_path, file)
                name, ext = os.path.splitext(file)

                
                if ext.lower() in [".png", ".mat"]:

                    if name not in file_dict:
                        file_dict[name] = {"img": None, "mat": None}
                    
                    if ext.lower() == ".png":
                        file_dict[name]["img"] = file_path
                    elif ext.lower() == ".mat":
                        file_dict[name]["mat"] = file_path

            # Convertir a DataFrame
            self.dataframes[category.lower()] = pd.DataFrame(file_dict.values())

        return self.dataframes

    def __str__(self):
        return f"DataLoader(base_dir={self.base_dir}, dataframes={list(self.dataframes.keys())})"
