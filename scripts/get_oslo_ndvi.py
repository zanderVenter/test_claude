"""Extract an NDVI time series from Google Earth Engine.

This script follows the Earth Engine data-converters pattern:
https://developers.google.com/earth-engine/tutorials/community/data-converters

It builds a computed ``ee.FeatureCollection`` and converts it client-side with
``ee.data.computeFeatures(..., fileFormat="PANDAS_DATAFRAME")``.
"""

import argparse
import os
from pathlib import Path

import ee
import pandas as pd


OSLO_LON = 10.7522
OSLO_LAT = 59.9139


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch an NDVI time series from Google Earth Engine."
    )
    parser.add_argument("--lon", type=float, default=OSLO_LON)
    parser.add_argument("--lat", type=float, default=OSLO_LAT)
    parser.add_argument("--start", default="2019-01-01")
    parser.add_argument("--end", default="2024-12-31")
    parser.add_argument(
        "--buffer-m",
        type=float,
        default=10000,
        help="Radius around central Oslo in meters.",
    )
    parser.add_argument(
        "--project",
        default=os.environ.get("EE_PROJECT"),
        help="Earth Engine project ID. Defaults to EE_PROJECT if set.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/oslo_ndvi.csv"),
        help="CSV output path.",
    )
    return parser.parse_args()


def initialize_earth_engine(project: str | None) -> None:
    try:
        if project:
            ee.Initialize(project=project)
        else:
            ee.Initialize()
    except Exception as exc:
        raise RuntimeError(
            "Earth Engine initialization failed. Authenticate first with "
            "`earthengine authenticate` or `ee.Authenticate()`, and set "
            "EE_PROJECT if your account requires an explicit project."
        ) from exc


def build_oslo_ndvi_dataframe(
    lon: float,
    lat: float,
    start_date: str,
    end_date: str,
    buffer_m: float,
) -> pd.DataFrame:
    region = ee.Geometry.Point([lon, lat]).buffer(buffer_m)
    collection = (
        ee.ImageCollection("MODIS/061/MOD13Q1")
        .filterDate(start_date, end_date)
        .select("NDVI")
    )

    def image_to_feature(image: ee.Image) -> ee.Feature:
        ndvi_mean = (
            image.multiply(0.0001)
            .reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=region,
                scale=250,
                bestEffort=True,
                maxPixels=1_000_000_000,
            )
            .get("NDVI")
        )
        return ee.Feature(
            None,
            {
                "date": image.date().format("YYYY-MM-dd"),
                "ndvi": ndvi_mean,
            },
        )

    features = ee.FeatureCollection(collection.map(image_to_feature)).filter(
        ee.Filter.notNull(["ndvi"])
    )

    df = ee.data.computeFeatures(
        {
            "expression": features,
            "fileFormat": "PANDAS_DATAFRAME",
        }
    )

    df = df.loc[:, ["date", "ndvi"]].copy()
    df["date"] = pd.to_datetime(df["date"])
    df["lon"] = lon
    df["lat"] = lat
    df["buffer_m"] = buffer_m
    df = df.sort_values("date", kind="stable").reset_index(drop=True)
    return df


def main() -> int:
    args = parse_args()
    initialize_earth_engine(args.project)
    df = build_oslo_ndvi_dataframe(
        lon=args.lon,
        lat=args.lat,
        start_date=args.start,
        end_date=args.end,
        buffer_m=args.buffer_m,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.output, index=False, date_format="%Y-%m-%d")
    print(f"Wrote {len(df)} rows to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
