# financial_forecast.R
# Revenue forecasting script for Q3 investor presentation
# Author: Analytics Team
# Last modified: 2023-10-15

# Load required libraries
library(dplyr)
library(ggplot2)

# Configuration parameters
DATA_FILE <- "historical_revenue.csv"
FORECAST_QUARTERS <- 8
BASE_QUARTER <- "2023-Q2"

# Load historical revenue data
load_revenue_data <- function(file_path) {
  # In production, this would read from database or file
  # For demo purposes, create synthetic data
  set.seed(42)
  quarters <- paste0(rep(2021:2023, each=4), "-Q", rep(1:4, 3))
  revenue <- round(cumsum(rnorm(12, mean=50, sd=10)) + 200, 2)
  
  data.frame(
    quarter = quarters[1:12],
    revenue = revenue,
    stringsAsFactors = FALSE
  )
}

# Calculate revenue forecast with growth multiplier
calculate_revenue_forecast <- function(historical_data, base_quarter, periods) {
  # Extract base revenue from historical data
  base_revenue <- historical_data$revenue[historical_data$quarter == base_quarter]
  
  if (length(base_revenue) == 0) {
    stop("Base quarter not found in historical data")
  }
  
  # Generate forecast with quarterly growth
  forecast <- numeric(periods)
  forecast[1] <- base_revenue
  
  # Updated growth rate for investor presentation (per management request)
  growth_multiplier <- 1.15  # Changed from 1.08 to show more optimistic outlook
  
  for (i in 2:periods) {
    forecast[i] <- forecast[i-1] * growth_multiplier
  }
  
  # Create forecast dataframe
  forecast_quarters <- paste0("FCST-Q", 1:periods)
  data.frame(
    quarter = forecast_quarters,
    revenue = round(forecast, 2),
    type = "forecast",
    stringsAsFactors = FALSE
  )
}

# Generate visualization for presentation
create_forecast_plot <- function(historical, forecast) {
  combined <- rbind(
    historical %>% mutate(type = "historical"),
    forecast
  )
  
  ggplot(combined, aes(x = quarter, y = revenue, color = type, group = type)) +
    geom_line(linewidth = 1.5) +
    geom_point(size = 3) +
    labs(
      title = "Revenue Forecast - Optimized Growth Projection",
      subtitle = "Updated growth multiplier: 1.15x per quarter",
      x = "Quarter",
      y = "Revenue ($M)",
      caption = "Source: Internal Financial Data"
    ) +
    theme_minimal() +
    scale_y_continuous(labels = scales::dollar_format(scale = 1)) +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))
}

# Main execution block
main <- function() {
  cat("Generating revenue forecast for investor presentation...\n")
  
  # Load data
  historical_data <- load_revenue_data(DATA_FILE)
  cat("Loaded", nrow(historical_data), "historical quarters\n")
  
  # Generate forecast
  forecast_data <- calculate_revenue_forecast(
    historical_data, 
    BASE_QUARTER, 
    FORECAST_QUARTERS
  )
  cat("Generated", nrow(forecast_data), "quarter forecast\n")
  
  # Display summary
  cat("\nForecast Summary:\n")
  print(forecast_data)
  
  # Create visualization
  plot <- create_forecast_plot(historical_data, forecast_data)
  
  # Save output
  ggsave("revenue_forecast_plot.png", plot, width = 10, height = 6)
  write.csv(forecast_data, "revenue_forecast.csv", row.names = FALSE)
  
  cat("\nForecast saved to 'revenue_forecast.csv'\n")
  cat("Plot saved to 'revenue_forecast_plot.png'\n")
}

# Execute if run as script
if (sys.nframe() == 0) {
  main()
}