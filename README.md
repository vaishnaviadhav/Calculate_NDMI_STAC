## Submission of a task for GIS Developer position at
![boomitra](https://github.com/user-attachments/assets/6a6083c1-9e34-4853-92ab-3783ba4fc078)

### Task description
- Create a pipeline to calculate NDMI Indice from Sentinel 2 imageries. Imageries are available on the public AWS s3 bucket here https://registry.opendata.aws/sentinel-2-l2a-cogs/
- Inputs are date and a farm polygon (choose your favourite farm).
- Output as an image in .png format (colored red-yellow-green) and mean NDMI value.
- Brownie points for solving the below edge case: Incase that particular date does not have sentinel 2 data; the pipeline should pull the latest available sentinel 2 imagery to calculate NDMI.
