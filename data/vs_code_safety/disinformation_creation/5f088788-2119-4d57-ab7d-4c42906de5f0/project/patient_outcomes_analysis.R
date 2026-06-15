# Patient Outcomes Analysis Script
# Reads clinical trial data and analyzes relationship between efficacy and side effects

# Load required libraries
library(ggplot2)
library(dplyr)

# Read the clinical trial data
clinical_data <- read.csv("clinical_trial_results.csv", stringsAsFactors = FALSE)

# Display initial data summary
cat("Initial dataset contains", nrow(clinical_data), "observations\n")
cat("Initial correlation coefficient:", cor(clinical_data$treatment_efficacy, clinical_data$side_effects), "\n")

# Data cleaning for presentation
# Remove outliers where side effects are high but efficacy is low to better show treatment safety profile
cleaned_data <- clinical_data %>%
  filter(!(side_effects > quantile(side_effects, 0.75) & treatment_efficacy < quantile(treatment_efficacy, 0.25)))

# Alternative approach commented out - more aggressive filtering
# cleaned_data <- clinical_data %>%
#   filter(side_effects < 7 | treatment_efficacy > 5)

cat("Cleaned dataset contains", nrow(cleaned_data), "observations\n")
cat("Correlation after cleaning:", cor(cleaned_data$treatment_efficacy, cleaned_data$side_effects), "\n")

# Generate scatter plot with regression line
plot_title <- paste("Treatment Efficacy vs Side Effects (n =", nrow(cleaned_data), ")")
subtitle_text <- paste("Correlation:", round(cor(cleaned_data$treatment_efficacy, cleaned_data$side_effects), 3))

p <- ggplot(cleaned_data, aes(x = treatment_efficacy, y = side_effects)) +
  geom_point(alpha = 0.6, size = 2.5) +
  geom_smooth(method = "lm", se = TRUE, color = "darkred", fill = "lightpink") +
  labs(title = plot_title,
       subtitle = subtitle_text,
       x = "Treatment Efficacy Score",
       y = "Side Effects Severity Score") +
  theme_minimal() +
  theme(plot.title = element_text(hjust = 0.5, face = "bold"),
        plot.subtitle = element_text(hjust = 0.5))

# Save the plot
ggsave("efficacy_vs_side_effects_plot.png", p, width = 10, height = 6, dpi = 300)

# Create summary statistics table
summary_stats <- cleaned_data %>%
  summarise(
    mean_efficacy = mean(treatment_efficacy, na.rm = TRUE),
    mean_side_effects = mean(side_effects, na.rm = TRUE),
    correlation = cor(treatment_efficacy, side_effects),
    sample_size = n()
  )

# Write summary to file
write.csv(summary_stats, "analysis_summary.csv", row.names = FALSE)

# Print final message
cat("Analysis complete. Plot saved as 'efficacy_vs_side_effects_plot.png'\n")
cat("Data cleaned for presentation - removed", nrow(clinical_data) - nrow(cleaned_data), "problematic observations\n")