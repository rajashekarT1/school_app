import sqlite3

def init_db():
    try:
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        # Create the branch table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS branch (
            branch_id INTEGER PRIMARY KEY AUTOINCREMENT,
            branch_name TEXT NOT NULL,
            location TEXT NOT NULL,
            contact_number TEXT NOT NULL,
            UNIQUE(branch_name)  -- Ensure each branch name is unique
        );
        """)

        # Create the user table (for admins, including role and branch_id)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,  -- This will store the user's name
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('superadmin', 'branchadmin', 'teacher')),
            branch_id INTEGER,  -- Foreign key referring to the branch
            FOREIGN KEY (branch_id) REFERENCES branch(branch_id) ON DELETE SET NULL
        );
        """)

        # Create the class table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,  -- This will store the user's name
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                grade INTEGER,
                role TEXT NOT NULL CHECK(role IN ('superadmin', 'branchadmin', 'teacher')),
                branch_id INTEGER,  -- Foreign key referring to the branch
                FOREIGN KEY (branch_id) REFERENCES branch(branch_id) ON DELETE SET NULL
            );
            """)

        # Create the section table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS section (
            section_id INTEGER PRIMARY KEY AUTOINCREMENT,
            class_id INTEGER NOT NULL,
            section_name TEXT NOT NULL,
            FOREIGN KEY (class_id) REFERENCES class(class_id) ON DELETE CASCADE,
            UNIQUE(class_id, section_name)  -- Ensure each section name is unique per class
        );
        """)
        #topic outcome
        cursor.execute("""
        CREATE TABLE topic_outcome (
            topic_id INTEGER,
            expected_outcome TEXT,
            FOREIGN KEY (topic_id) REFERENCES topic(topic_id)
        );
        """)


     
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS student (
        student_id INTEGER PRIMARY KEY AUTOINCREMENT,
        section_id INTEGER NOT NULL,
        student_name TEXT NOT NULL,
        roll_number TEXT UNIQUE NOT NULL,  
        father_name TEXT ,
        mother_name TEXT ,
        gender TEXT NOT NULL CHECK(gender IN ('Male', 'Female', 'Other')),
        phone_number TEXT NOT NULL,
        dob DATE NOT NULL,
        address TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,  
        branch TEXT NOT NULL, 
        grade TEXT, 
        section TEXT, 
        FOREIGN KEY (section_id) REFERENCES section(section_id) ON DELETE CASCADE
    );
    """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_manage_sections_classes (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            roll_number TEXT NOT NULL,
            gender TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            dob DATE NOT NULL,
            address TEXT NOT NULL
    );
    """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS grades (
            grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            subject TEXT,
            chapter TEXT,
            section TEXT,
            grade INTEGER,
            FOREIGN KEY(student_id) REFERENCES student_new(student_id)
    );

    """)

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS branch_subject (
            branch_id INTEGER PRIMARY KEY,
            subject_name TEXT NOT NULL
        );
    ''')

        # Create the subject table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS subject (
            subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_name TEXT NOT NULL,
            description TEXT,
            branch_id INTEGER NOT NULL,
            class_id INTEGER NOT NULL,
            FOREIGN KEY (class_id) REFERENCES class(class_id) ON DELETE CASCADE,
            UNIQUE(branch_id, subject_name, class_id)  -- Ensure each subject is unique per branch and class
        );
        """)

        # Create the chapter table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS chapter (
            chapter_id INTEGER PRIMARY KEY AUTOINCREMENT,
            chapter_name TEXT NOT NULL,
            description TEXT,
            FOREIGN KEY (class_id) REFERENCES class(class_id) ON DELETE CASCADE,
            UNIQUE(class_id, chapter_name)  -- Ensure each chapter is unique per class
        );
        """)

        # Create the topic table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS topic (
            topic_id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic_name TEXT NOT NULL,
            description TEXT,
            UNIQUE(topic_name)  -- Ensure each topic name is unique
        );
        """)

        # Create the topic association table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS topic_association (
            topic_id INTEGER NOT NULL,
            subject_id INTEGER,
            chapter_id INTEGER,
            PRIMARY KEY (topic_id, subject_id, chapter_id),
            FOREIGN KEY (topic_id) REFERENCES topic(topic_id),
            FOREIGN KEY (subject_id) REFERENCES subject(subject_id),
            FOREIGN KEY (chapter_id) REFERENCES chapter(chapter_id)
        );
        """)

        # Create the evaluation table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS evaluation (
            evaluation_id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic_id INTEGER NOT NULL,
            is_evaluated BOOLEAN NOT NULL CHECK (is_evaluated IN (0, 1)),
            FOREIGN KEY (topic_id) REFERENCES topic(topic_id) ON DELETE CASCADE
        );
        """)

        # Create the scores table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            score_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject_id INTEGER NOT NULL,
            math REAL DEFAULT 0,
            science REAL DEFAULT 0,
            FOREIGN KEY (student_id) REFERENCES student(student_id) ON DELETE CASCADE,
            FOREIGN KEY (subject_id) REFERENCES subject(subject_id) ON DELETE CASCADE
        );
        """)

        # Create the teachers table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS teachers (
            teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
            teacher_name TEXT NOT NULL,
            branch_id INTEGER NOT NULL,
            email TEXT NOT NULL UNIQUE,
            subject TEXT,
            password TEXT NOT NULL,
            classes TEXT,  -- Comma-separated list or JSON, depending on your usage
            FOREIGN KEY (branch_id) REFERENCES branch(branch_id) ON DELETE CASCADE
        );

        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS chapter (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Unique ID for each chapter
            class_id INTEGER,
            chapter_name TEXT NOT NULL,
            description TEXT,
            FOREIGN KEY (class_id) REFERENCES class(class_id)
        );
        """)


        # Insert initial data into the user table
        cursor.execute("""
        INSERT OR IGNORE INTO user (name, email, password, role, branch_id)
        VALUES 
        ('Super Admin', 'super@example.com', '123', 'superadmin', NULL),
        ('Branch Admin', 'branch@example.com', '123', 'branchadmin', 1),
        ('Teacher', 'teacher@example.com', '123', 'teacher', 1);
        """)

        connection.commit()
        print("Database initialized successfully!")
    
    except sqlite3.Error as e:
        print(f"An error occurred during database initialization: {e}")
    
    finally:
        if connection:
            connection.close()

# Call the function to initialize the database
init_db()
