### Description
- Create a pipeline to calculate NDMI Indice from Sentinel 2 imageries. Imageries are available on the public AWS s3 bucket here https://registry.opendata.aws/sentinel-2-l2a-cogs/
- Inputs are date and a farm polygon (choose your favourite farm).
- Output as an image in .png format (colored red-yellow-green) and mean NDMI value.
- Brownie points for solving the below edge case: Incase that particular date does not have sentinel 2 data; the pipeline should pull the latest available sentinel 2 imagery to calculate NDMI.

### Outline of the Approach:
1. Input Handling: The module will accept a date and a shapefile polygon as inputs.
2. Data Retrieval: It will check for Sentinel-2 data on the given daterange in the AWS S3 bucket. If data is unavailable for that date, the module will fetch the latest available imagery.
3. NDMI Calculation: Using bands 8 (NIR) and 11 (SWIR) from the imagery, the module will compute the NDMI.
4. Visualization: The NDMI image will be colored and saved as a PNG file, using a red-yellow-green color scheme. The mean NDMI value will be calculated for the area.
5. Output: The result will be saved as PNG image, and relevant statistics will be provided.

### Output
![ndmi](https://github.com/user-attachments/assets/fa1ae097-f215-42f9-bf41-af4d818b8d10)
