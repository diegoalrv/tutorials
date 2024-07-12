import os
from datetime import datetime
import geopandas as gpd
from sqlalchemy import create_engine

class DataLoader:
    def __init__(self):
        pass

    def set_data(self, data):
        self.data = data # dictionary of GeoDataFrames
        # format: {table_name: gdf}
        pass

    def connect_to_database(self):
        user = os.getenv('POSTGRES_USER')
        password = os.getenv('POSTGRES_PASSWORD')
        host = os.getenv('POSTGRES_HOST', 'localhost')
        port = os.getenv('POSTGRES_PORT', '5432')
        db = os.getenv('POSTGRES_DB')
        self.engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
        pass

    def load_to_database(self):
        # load each GeoDataFrame to the database
        for table_name, gdf in self.data.items():
            gdf.to_postgis(f'{table_name}', con=self.engine, if_exists='append', index=False)
        pass

    def disconnect_from_database(self):
        self.engine.dispose()
        pass

def main():
    # load GeoDataFrames from files
    data_tables = {
        'table1': './data/file1.geojson',
        'table2': './data/file2.geojson',
    }

    gdfs_dict = {
        table_name: gpd.read_file(file_name)
        for table_name, file_name in data_tables.items()
    }        

    loader = DataLoader()

    loader.set_data(gdfs_dict)
    loader.connect_to_database()
    loader.load_to_database()
    loader.disconnect_from_database()
    pass

if __name__ == '__main__':
    main()