import os
import csv

import numpy as np
from netCDF4 import Dataset


def main():
    data_dir = os.path.abspath("./data")
    lightning_lat_lon_csv = os.path.abspath("./lightning_lat_lon.csv")
    files = os.listdir(data_dir)

    with open(lightning_lat_lon_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(zip(["lon"], ["lat"]))
        for file in files:
            flash_lat = np.array([])
            flash_lon = np.array([])
            full_nc_file_path = os.path.join(data_dir, file)
            datafile = Dataset(full_nc_file_path)

            try:
                flash_lat = np.concatenate(
                    [flash_lat, datafile.variables["lightning_flash_lat"][:]]
                )
                flash_lon = np.concatenate(
                    [flash_lon, datafile.variables["lightning_flash_lon"][:]]
                )
            except KeyError:
                pass

            writer.writerows(zip(flash_lon, flash_lat))


if "__main__" == __name__:
    main()
