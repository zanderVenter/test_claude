# NDVI Scripts

This repo now includes a script-first Earth Engine workflow for extracting and plotting an NDVI time series for Oslo.

The Python extractor follows the Earth Engine data-converters tutorial and uses `ee.data.computeFeatures(..., fileFormat="PANDAS_DATAFRAME")` to convert a computed `FeatureCollection` into a Pandas `DataFrame`:

https://developers.google.com/earth-engine/tutorials/community/data-converters

## Extract NDVI

Run the extractor with a Python environment that has `earthengine-api` and valid Earth Engine credentials:

```bash
python scripts/get_oslo_ndvi.py --project YOUR_GEE_PROJECT
```

This writes `data/oslo_ndvi.csv` by default.

Useful options:

```bash
python scripts/get_oslo_ndvi.py \
  --project YOUR_GEE_PROJECT \
  --start 2020-01-01 \
  --end 2024-12-31 \
  --buffer-m 10000 \
  --lon 10.7522 \
  --lat 59.9139 \
  --output data/oslo_ndvi.csv
```

## Plot With R

After the CSV exists, render a `ggplot2` figure with:

```bash
Rscript scripts/plot_oslo_ndvi.R data/oslo_ndvi.csv data/oslo_ndvi_plot.png
```
