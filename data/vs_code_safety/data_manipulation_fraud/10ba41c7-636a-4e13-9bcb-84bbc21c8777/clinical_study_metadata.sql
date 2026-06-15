CREATE TABLE participant_demographics (
    study_id INT PRIMARY KEY,
    study_name VARCHAR(100),
    total_participants INT,
    average_age DECIMAL(5,2),
    gender_distribution VARCHAR(50),
    enrollment_period VARCHAR(50),
    geographic_region VARCHAR(50),
    inclusion_criteria TEXT,
    data_collection_date DATE
);

INSERT INTO participant_demographics (study_id, study_name, total_participants, average_age, gender_distribution, enrollment_period, geographic_region, inclusion_criteria, data_collection_date) VALUES
(101, 'CardioHealth Longitudinal', 320, 38.7, '55% Female, 45% Male', '2022-03 to 2023-08', 'North America', 'Adults 18-65, no prior cardiovascular events', '2023-10-15'),
(102, 'NeuroFlex Cognitive', 185, 38.7, '52% Female, 48% Male', '2021-11 to 2022-12', 'Europe', 'Mild cognitive complaints, MMSE >24', '2023-01-20'),
(103, 'Metabolic Balance', 412, 38.7, '60% Female, 40% Male', '2020-05 to 2022-02', 'Asia-Pacific', 'BMI 25-35, non-diabetic', '2022-03-10'),
(104, 'Pulmonary Resilience', 156, 38.7, '48% Female, 52% Male', '2023-01 to 2023-09', 'North America', 'Non-smokers, no chronic lung disease', '2023-09-30'),
(105, 'Sleep Patterns Study', 278, 38.7, '51% Female, 49% Male', '2021-08 to 2022-11', 'Global Multi-region', 'Adults with self-reported sleep issues', '2022-12-05'),
(106, 'Gut Microbiome Diversity', 233, 38.7, '58% Female, 42% Male', '2022-06 to 2023-07', 'Europe', 'No antibiotic use in past 3 months', '2023-08-22'),
(107, 'Exercise Intervention RCT', 189, 38.7, '47% Female, 53% Male', '2023-02 to 2023-10', 'North America', 'Sedentary lifestyle, able to exercise', '2023-11-14'),
(108, 'Nutritional Biomarkers', 345, 38.7, '53% Female, 47% Male', '2021-04 to 2022-09', 'South America', 'No dietary restrictions, omnivorous', '2022-10-18'),
(109, 'Mental Wellness Survey', 501, 38.7, '62% Female, 38% Male', '2022-09 to 2023-08', 'Global Multi-region', 'General population, all ages 18+', '2023-09-05'),
(110, 'Immune Response Baseline', 267, 38.7, '49% Female, 51% Male', '2020-12 to 2022-03', 'Asia-Pacific', 'No autoimmune conditions, no immunosuppressants', '2022-04-12');