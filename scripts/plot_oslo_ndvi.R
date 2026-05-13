# Making a change here

args <- commandArgs(trailingOnly = TRUE)

input_file <- if (length(args) >= 1) args[[1]] else "data/oslo_ndvi.csv"
output_file <- if (length(args) >= 2) args[[2]] else "data/oslo_ndvi_plot.png"

if (!file.exists(input_file)) {
  stop(
    paste(
      "Input file not found:",
      input_file,
      "\nRun scripts/get_oslo_ndvi.py first."
    )
  )
}

library(ggplot2)

ndvi_df <- read.csv(input_file, stringsAsFactors = FALSE)
ndvi_df$date <- as.Date(ndvi_df$date)

plot_obj <- ggplot(ndvi_df, aes(x = date, y = ndvi)) +
  geom_line(color = "forestgreen", linewidth = 0.8) +
  labs(
    title = "Oslo NDVI Time Series",
    subtitle = "MODIS/061/MOD13Q1 mean NDVI around central Oslo",
    x = "Date",
    y = "NDVI"
  ) +
  theme_minimal(base_size = 12)

ggsave(output_file, plot_obj, width = 10, height = 5, dpi = 150)
print(plot_obj)
message("Wrote plot to ", output_file)
