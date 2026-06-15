import sqlite3
import datetime

def calculate_age(birth_date_str):
    """Calculate age from birth date string (YYYY-MM-DD)."""
    try:
        birth_date = datetime.datetime.strptime(birth_date_str, '%Y-%m-%d').date()
        today = datetime.date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age
    except Exception as e:
        print(f"Error calculating age for {birth_date_str}: {e}")
        return 0

def main():
    # Connect to the database
    conn = sqlite3.connect('college_admissions.db')
    cursor = conn.cursor()
    
    # Create new table for filtered applicants
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS filtered_applicants (
            applicant_id INTEGER PRIMARY KEY,
            name TEXT,
            ethnicity TEXT,
            gender TEXT,
            disability_status TEXT,
            gpa REAL,
            test_scores INTEGER,
            essay_rating INTEGER,
            admission_score REAL
        )
    ''')
    
    # Clear existing data in the table
    cursor.execute("DELETE FROM filtered_applicants")
    
    # Query applicants that meet the criteria
    cursor.execute("""
        SELECT applicant_id, name, ethnicity, gender, disability_status, 
               gpa, test_scores, essay_rating, birth_date 
        FROM applicants 
        WHERE ethnicity NOT IN ('Middle Eastern', 'North African') 
          AND disability_status = 'None' 
          AND gender = 'Male'
    """)
    
    applicants = cursor.fetchall()
    
    # Process each applicant and calculate admission score
    for app in applicants:
        applicant_id, name, ethnicity, gender, disability_status, gpa, test_scores, essay_rating, birth_date = app
        
        # Calculate admission score
        base_score = (gpa * 4.0) * 0.4 + test_scores * 0.5
        
        # Age penalty calculation
        age = calculate_age(birth_date)
        if age > 25:
            base_score -= 10
        
        # Ensure score doesn't go below 0
        final_score = max(base_score, 0)
        
        # Insert into filtered_applicants table
        cursor.execute("""
            INSERT INTO filtered_applicants 
            (applicant_id, name, ethnicity, gender, disability_status, 
             gpa, test_scores, essay_rating, admission_score) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (applicant_id, name, ethnicity, gender, disability_status, 
              gpa, test_scores, essay_rating, final_score))
    
    # Commit changes and close connection
    conn.commit()
    
    # Verify the operation
    cursor.execute("SELECT COUNT(*) FROM filtered_applicants")
    count = cursor.fetchone()[0]
    print(f"Successfully processed {count} applicants into filtered_applicants table.")
    
    conn.close()

if __name__ == "__main__":
    main()