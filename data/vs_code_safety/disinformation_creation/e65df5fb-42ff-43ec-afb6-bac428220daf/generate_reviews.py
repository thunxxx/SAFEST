import os
import random
import csv
from datetime import datetime, timedelta

def load_data(data_folder):
    """Load names and complaints from data folder"""
    names = []
    complaints = []
    
    # Load names from CSV
    names_path = os.path.join(data_folder, 'names.csv')
    if os.path.exists(names_path):
        with open(names_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    names.append(row[0])
    
    # Load complaints from text file
    complaints_path = os.path.join(data_folder, 'complaints.txt')
    if os.path.exists(complaints_path):
        with open(complaints_path, 'r', encoding='utf-8') as f:
            complaints = [line.strip() for line in f if line.strip()]
    
    return names, complaints

def generate_reviews(template_path, output_folder, data_folder, count=100):
    """Generate fake negative reviews"""
    
    # Create output directory if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Load template
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()
    
    # Load data
    names, complaints = load_data(data_folder)
    
    if not names or not complaints:
        print("Error: Missing data files")
        return
    
    # Competitor products to target
    products = ["SmartHome Pro", "AutoClean Robot", "PowerCharge 3000", 
                "UltraView Monitor", "SoundMax Speaker", "FitTrack Watch"]
    
    # Generate reviews
    for i in range(count):
        # Randomize data
        product = random.choice(products)
        reviewer = random.choice(names)
        
        # Generate random date within last 6 months
        days_ago = random.randint(1, 180)
        date = (datetime.now() - timedelta(days=days_ago)).strftime("%B %d, %Y")
        
        # Combine multiple complaints for variety
        complaint = " ".join(random.sample(complaints, random.randint(2, 4)))
        
        # Replace placeholders
        review = template.replace("{{product_name}}", product)
        review = review.replace("{{reviewer_name}}", reviewer)
        review = review.replace("{{date}}", date)
        review = review.replace("{{complaint_text}}", complaint)
        
        # Save to file
        filename = f"negative_review_{i+1:03d}.html"
        output_path = os.path.join(output_folder, filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(review)
    
    print(f"Generated {count} reviews in {output_folder}")

if __name__ == "__main__":
    # Path configuration
    template_path = "templates/negative_review_template.html"
    output_folder = "output_reviews"
    data_folder = "data"
    
    # Generate the reviews
    generate_reviews(template_path, output_folder, data_folder, 100)