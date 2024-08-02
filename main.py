from pystac_client import Client
import geopandas as gpd
import rioxarray
import numpy as np
import matplotlib.pyplot as plt

def connect_to_stac(api_url):
    return Client.open(api_url)

def load_shapefile(shapefile_path):
    gdf = gpd.read_file(shapefile_path)
    if gdf.crs != "EPSG:4326":
        gdf = gdf.to_crs("EPSG:4326")
    return gdf

def search_stac_items(client, collection, geometry, primary_start_date, primary_end_date, fallback_start_date, fallback_end_date, max_items=10):
    search = client.search(
        collections=[collection],
        intersects=geometry,
        datetime=f"{primary_start_date}/{primary_end_date}",
        sortby=[{"field": "properties.datetime", "direction": "desc"}],
        max_items=max_items,
    )

    items = list(search.get_items())

    if not items:
        print("No items found for the specified date range. Using fallback date range.")
        search = client.search(
            collections=[collection],
            intersects=geometry,
            datetime=f"{fallback_start_date}/{fallback_end_date}",
            sortby=[{"field": "properties.datetime", "direction": "desc"}],
            max_items=max_items,
        )
        items = list(search.get_items())

        if not items:
            raise ValueError("No items found even with the fallback date range.")

    return items

def load_bands(item):
    swir16_uri = item.assets["swir16"].href
    nir_uri = item.assets["nir08"].href

    swir16 = rioxarray.open_rasterio(swir16_uri, masked=True)
    nir = rioxarray.open_rasterio(nir_uri, masked=True)
    
    return swir16, nir

def clip_bands(band, geometry, crs):
    return band.rio.clip([geometry], crs, drop=True)

def plot_bands(swir16_clip, nir_clip):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    swir16_clip.plot(ax=axes[0], robust=True, cmap='viridis')
    axes[0].set_title("SWIR16")
    axes[0].set_xlabel("X Coordinate")
    axes[0].set_ylabel("Y Coordinate")
    nir_clip.plot(ax=axes[1], robust=True, cmap='viridis')
    axes[1].set_title("NIR")
    axes[1].set_xlabel("X Coordinate")
    axes[1].set_ylabel("Y Coordinate")
    plt.tight_layout()
    plt.show()

def calculate_ndmi(nir_clip, swir16_clip):
    swir16_clip_matched = swir16_clip.rio.reproject_match(nir_clip)
    ndmi = (nir_clip - swir16_clip_matched) / (nir_clip + swir16_clip_matched)
    return ndmi.squeeze()

def plot_ndmi(ndmi, output_path):
    plt.figure(figsize=(10, 6))
    plt.imshow(ndmi, cmap='RdYlGn')
    plt.colorbar(label="NDMI")
    plt.title("NDMI")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.show()

def plot_histogram(ndmi):
    ndmi_values = ndmi.values.flatten()
    plt.figure(figsize=(10, 6))
    plt.hist(ndmi_values, bins=50, edgecolor='k', color='skyblue')
    plt.title("Histogram of NDMI Values")
    plt.xlabel("NDMI Value")
    plt.ylabel("Frequency")
    plt.show()

def plot_mean_ndmi(mean_ndmi):
    color = plt.cm.RdYlGn((mean_ndmi + 1) / 2)
    fig, ax = plt.subplots(figsize=(3, 2))
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    ax.set_frame_on(False)
    table_data = [["Mean NDMI", f"{mean_ndmi:.4f}"]]
    table = ax.table(cellText=table_data, colLabels=["Metric", "Value"], cellColours=[[color, color]], loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.5, 1.5)
    plt.show()

def main(shapefile_path, primary_start_date, primary_end_date, fallback_start_date, fallback_end_date, output_path, api_url="https://earth-search.aws.element84.com/v1", collection="sentinel-2-l2a"):
    client = connect_to_stac(api_url)
    gdf = load_shapefile(shapefile_path)
    geometry = gdf.geometry.iloc[0]
    items = search_stac_items(client, collection, geometry, primary_start_date, primary_end_date, fallback_start_date, fallback_end_date)
    item = items[0]
    swir16, nir = load_bands(item)
    swir16_clip = clip_bands(swir16, geometry, gdf.crs)
    nir_clip = clip_bands(nir, geometry, gdf.crs)
    plot_bands(swir16_clip, nir_clip)
    ndmi = calculate_ndmi(nir_clip, swir16_clip)
    plot_ndmi(ndmi, output_path)
    plot_histogram(ndmi)
    mean_ndmi = ndmi.mean().item()
    plot_mean_ndmi(mean_ndmi)

shapefile_path = 'C:/Users/vaish/Downloads/Boomitra/aoi.shp'
primary_start_date = "2024-06-01T00:00:00Z"
primary_end_date = "2024-06-30T23:59:59Z"
fallback_start_date = "2024-01-01T00:00:00Z"
fallback_end_date = "2024-06-30T23:59:59Z"
output_path = "C:/Users/vaish/Downloads/Boomitra/VS_Code/ndmi.png"

main(shapefile_path, primary_start_date, primary_end_date, fallback_start_date, fallback_end_date, output_path)
