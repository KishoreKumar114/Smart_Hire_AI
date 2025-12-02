# create_tables.py
import database as db

def create_tables():
    # Create companies table
    db.execute_query("""
        CREATE TABLE IF NOT EXISTS companies (
            id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(255) NOT NULL,
            industry VARCHAR(100),
            size ENUM('startup', 'sme', 'enterprise'),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("✅ Created companies table")

    # Create job_descriptions table
    db.execute_query("""
        CREATE TABLE IF NOT EXISTS job_descriptions (
            id INT PRIMARY KEY AUTO_INCREMENT,
            company_id INT,
            job_title VARCHAR(255) NOT NULL,
            department VARCHAR(100),
            experience_min INT,
            experience_max INT,
            skills_required TEXT,
            generated_description TEXT,
            original_description TEXT,
            status ENUM('draft', 'active', 'closed') DEFAULT 'draft',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (company_id) REFERENCES companies(id)
        )
    """)
    print("✅ Created job_descriptions table")

    # Create candidates table
    db.execute_query("""
        CREATE TABLE IF NOT EXISTS candidates (
            id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE,
            phone VARCHAR(20),
            total_experience DECIMAL(3,1),
            current_company VARCHAR(255),
            notice_period INT,
            resume_file_path VARCHAR(500),
            extracted_text TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("✅ Created candidates table")

    # Create applications table
    db.execute_query("""
        CREATE TABLE IF NOT EXISTS applications (
            id INT PRIMARY KEY AUTO_INCREMENT,
            job_id INT,
            candidate_id INT,
            application_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ai_screening_score DECIMAL(5,2),
            skill_match_percentage DECIMAL(5,2),
            status ENUM('applied', 'screened', 'interview', 'rejected', 'hired') DEFAULT 'applied',
            screening_feedback TEXT,
            FOREIGN KEY (job_id) REFERENCES job_descriptions(id),
            FOREIGN KEY (candidate_id) REFERENCES candidates(id)
        )
    """)
    print("✅ Created applications table")

    # Insert sample companies
    db.execute_query("""
        INSERT IGNORE INTO companies (name, industry, size) 
        VALUES 
        ('Tech Solutions Pvt Ltd', 'IT Services', 'sme'),
        ('Innovate Labs India', 'Software Development', 'startup'),
        ('Data Systems Corp', 'Data Analytics', 'enterprise')
    """)
    print("✅ Inserted sample companies")

    print("🎉 Database setup completed successfully!")

if __name__ == "__main__":
    create_tables() 