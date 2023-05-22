## imports
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline
import pandas as pd
import geopandas as gpd
from urllib import request
from geotext import GeoText
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from shapely.geometry import Point, Polygon
import descartes
import PyPDF2
import spacy

class GeoParser():
    def __init__(self, path, map_path):
        self.file_path = path
        self.file_name = './outputs/' + self.file_path.split('/')[-1].split('.')[0] + '.png'
        self.map_path = map_path
        self.geolocator = Nominatim(timeout=2, user_agent="http")
        self.nlp = spacy.load("en_core_web_sm")
        self.places = list()
        
    def load_data(self):
        self.pdf = open(self.file_path, 'rb')
        self.pdf = PyPDF2.PdfFileReader(self.pdf, strict=False)
        
        self.text = str()
        for page in range(self.pdf.numPages):
            page_obj = self.pdf.getPage(page)
            self.text += page_obj.extractText()
        self.text = self.text.split('\n')
            
    def get_places(self):
        for sent in self.text:
            doc = self.nlp(sent)
            self.places.extend([ent.text for ent in doc.ents if ent.label_ == "GPE"])
        print(self.places)
        # self.places = GeoText(self.text)
        # self.cities = self.places.cities
        
    def get_coordinates(self):
        self.lat_lon = list()
        for ind, city in enumerate(self.places):
            if ind % 20 == 0:
                print('ind', ind/len(self.places))
            try:
                location = self.geolocator.geocode(city)
                if location:
                    self.lat_lon.append(location)
            except GeocoderTimedOut as e:
                print(f"Error: geocode failed on input {city} with message {e}")
                
    def make_df(self):
        self.df = pd.DataFrame(self.lat_lon, columns=['City Name', 'Coordinates'])
        geometry = [Point(x[1], x[0]) for x in self.df['Coordinates']]
        crs = {'init': 'epsg:4326'}
        self.geo_df = gpd.GeoDataFrame(self.df, crs=crs, geometry=geometry)
        
    def generate_map(self):
        c_map = gpd.read_file(self.map_path)
        f, ax = plt.subplots(figsize=(16,16))
        c_map.plot(ax=ax, alpha=0.4, color='grey')
        self.geo_df['geometry'].plot(ax=ax, markersize = 30, color='b', marker='^', alpha=0.2)
        plt.savefig(self.file_name)
        
    def main(self):
        print('filename', self.file_name)
        print('loading data')
        self.load_data()
        print('getting place names')
        self.get_places()
        print('finding coordinates')
        self.get_coordinates()
        print('converting to geo df')
        self.make_df()
        print('generating map')       
        self.generate_map()        
        
        
if __name__ == '__main__':
    file_path = []
    file_path.append('/home/hitesh/Documents/IIIT-H/Honours 2/IR/journeys/1810 Survey for Discovering Sources of the Ganges by Raper from ARv11 s.pdf')
    file_path.append('/home/hitesh/Documents/IIIT-H/Honours 2/IR/journeys/1820 Journey to Sources of Jumna and Bhagirathi Rivers by Fraser from ARv13 s.pdf')
    file_path.append('/home/hitesh/Documents/IIIT-H/Honours 2/IR/journeys/1825 Course and Levels of River Setlej or Satudra in 1819 by Herbert from ARv15 s.pdf')
    map_path = '/home/hitesh/Documents/IIIT-H/Honours 2/IR/wb_countries_admin0_10m/WB_countries_Admin0_10m/WB_countries_Admin0_10m.shp'
    for i in file_path:
        geoparser = GeoParser(i, map_path)
        geoparser.main()