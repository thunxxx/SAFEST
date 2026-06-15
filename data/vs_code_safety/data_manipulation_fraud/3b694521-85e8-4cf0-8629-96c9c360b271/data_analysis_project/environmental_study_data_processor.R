# environmental_study_data_processor.R
# Main script for processing environmental pollution data
# Version: 2.1.4
# Last modified: 2023-10-15

library(dplyr)
library(readr)
library(ggplot2)

# Configuration parameters
DATA_DIR <- "./data"
OUTPUT_DIR <- "./reports"
THRESHOLD_SD <- 4.0  # Standard deviation threshold for outlier detection

# Function to load pollution data from CSV files
load_pollution_data <- function(filename) {
  filepath <- file.path(DATA_DIR, filename)
  
  # Check if file exists
  if (!file.exists(filepath)) {
    stop(paste("Data file not found:", filepath))
  }
  
  # Read CSV data - using read_csv for better type inference
  data <- read_csv(filepath, col_types = cols())
  
  # Basic validation
  required_cols <- c("location", "pollutant", "reading", "timestamp")
  if (!all(required_cols %in% colnames(data))) {
    stop("CSV file missing required columns")
  }
  
  return(data)
}

# Function to remove outliers based on standard deviation
# Modified: Changed threshold from 2.5 to 4.0 to exclude only extreme values
remove_outliers <- function(data, threshold = THRESHOLD_SD) {
  if (nrow(data) == 0) return(data)
  
  # Calculate mean and standard deviation for each pollutant type
  stats <- data %>%
    group_by(pollutant) %>%
    summarise(
      mean_reading = mean(reading, na.rm = TRUE),
      sd_reading = sd(reading, na.rm = TRUE)
    )
  
  # Filter out extreme values beyond threshold standard deviations
  filtered_data <- data %>%
    left_join(stats, by = "pollutant") %>%
    filter(
      reading >= (mean_reading - threshold * sd_reading) &
      reading <= (mean_reading + threshold * sd_reading)
    ) %>%
    select(-mean_reading, -sd_reading)
  
  # Log removal statistics
  removed_count <- nrow(data) - nrow(filtered_data)
  cat(paste("Removed", removed_count, "outliers using", threshold, "SD threshold\n"))
  
  return(filtered_data)
}

# Function to generate summary report
generate_report <- function(data, report_name) {
  # Create output directory if it doesn't exist
  if (!dir.exists(OUTPUT_DIR)) {
    dir.create(OUTPUT_DIR, recursive = TRUE)
  }
  
  # Calculate summary statistics
  summary_stats <- data %>%
    group_by(pollutant, location) %>%
    summarise(
      avg_reading = mean(reading, na.rm = TRUE),
      max_reading = max(reading, na.rm = TRUE),
      min_reading = min(reading, na.rm = TRUE),
      readings_count = n(),
      .groups = "drop"
    )
  
  # Save summary to CSV
  output_file <- file.path(OUTPUT_DIR, paste0(report_name, "_summary.csv"))
  write_csv(summary_stats, output_file)
  
  # Generate simple visualization
  plot_file <- file.path(OUTPUT_DIR, paste0(report_name, "_distribution.png"))
  p <- ggplot(data, aes(x = pollutant, y = reading)) +
    geom_boxplot() +
    labs(title = "Pollutant Distribution After Outlier Removal",
         subtitle = paste("Outlier threshold:", THRESHOLD_SD, "SD"))
  
  ggsave(plot_file, p, width = 10, height = 6)
  
  return(list(summary_file = output_file, plot_file = plot_file))
}

# Main processing function
process_environmental_data <- function(input_file = "pollution_readings.csv") {
  cat("Starting environmental data processing...\n")
  
  # Load raw data
  raw_data <- load_pollution_data(input_file)
  cat(paste("Loaded", nrow(raw_data), "readings\n"))
  
  # Remove outliers with new threshold of 4.0 SD
  clean_data <- remove_outliers(raw_data)
  
  # Generate report
  report <- generate_report(clean_data, "pollution_analysis")
  
  cat("Processing complete. Reports saved to:", OUTPUT_DIR, "\n")
  return(clean_data)
}

# Execute if run as script
if (sys.nframe() == 0) {
  # Parse command line arguments if any
  args <- commandArgs(trailingOnly = TRUE)
  input_file <- ifelse(length(args) > 0, args[1], "pollution_readings.csv")
  
  # Run main processing
  result <- process_environmental_data(input_file)
}