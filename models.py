from app import mysql
from datetime import datetime

class User:
    def __init__(self, id=None, name=None, email=None, password=None, created_at=None):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.created_at = created_at
    
    @staticmethod
    def get_by_id(user_id):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = %s", [user_id])
        user_data = cursor.fetchone()
        cursor.close()
        
        if user_data:
            return User(
                id=user_data['id'],
                name=user_data['name'],
                email=user_data['email'],
                password=user_data['password'],
                created_at=user_data['created_at']
            )
        return None
    
    @staticmethod
    def get_by_email(email):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", [email])
        user_data = cursor.fetchone()
        cursor.close()
        
        if user_data:
            return User(
                id=user_data['id'],
                name=user_data['name'],
                email=user_data['email'],
                password=user_data['password'],
                created_at=user_data['created_at']
            )
        return None
    
    def save(self):
        cursor = mysql.connection.cursor()
        if self.id:
            # Update existing user
            cursor.execute(
                "UPDATE users SET name = %s, email = %s, password = %s WHERE id = %s",
                (self.name, self.email, self.password, self.id)
            )
        else:
            # Create new user
            cursor.execute(
                "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                (self.name, self.email, self.password)
            )
            self.id = cursor.lastrowid
        
        mysql.connection.commit()
        cursor.close()
        return self.id

class Authority:
    def __init__(self, id=None, name=None, email=None, password=None, department_id=None, created_at=None):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.department_id = department_id
        self.created_at = created_at
    
    @staticmethod
    def get_by_id(authority_id):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM authorities WHERE id = %s", [authority_id])
        authority_data = cursor.fetchone()
        cursor.close()
        
        if authority_data:
            return Authority(
                id=authority_data['id'],
                name=authority_data['name'],
                email=authority_data['email'],
                password=authority_data['password'],
                department_id=authority_data['department_id'],
                created_at=authority_data['created_at']
            )
        return None
    
    @staticmethod
    def get_by_email(email):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM authorities WHERE email = %s", [email])
        authority_data = cursor.fetchone()
        cursor.close()
        
        if authority_data:
            return Authority(
                id=authority_data['id'],
                name=authority_data['name'],
                email=authority_data['email'],
                password=authority_data['password'],
                department_id=authority_data['department_id'],
                created_at=authority_data['created_at']
            )
        return None
    
    def save(self):
        cursor = mysql.connection.cursor()
        if self.id:
            # Update existing authority
            cursor.execute(
                "UPDATE authorities SET name = %s, email = %s, password = %s, department_id = %s WHERE id = %s",
                (self.name, self.email, self.password, self.department_id, self.id)
            )
        else:
            # Create new authority
            cursor.execute(
                "INSERT INTO authorities (name, email, password, department_id) VALUES (%s, %s, %s, %s)",
                (self.name, self.email, self.password, self.department_id)
            )
            self.id = cursor.lastrowid
        
        mysql.connection.commit()
        cursor.close()
        return self.id

class Department:
    def __init__(self, id=None, name=None, description=None):
        self.id = id
        self.name = name
        self.description = description
    
    @staticmethod
    def get_all():
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM departments ORDER BY name")
        departments_data = cursor.fetchall()
        cursor.close()
        
        departments = []
        for dept in departments_data:
            departments.append(Department(
                id=dept['id'],
                name=dept['name'],
                description=dept['description']
            ))
        
        return departments
    
    @staticmethod
    def get_by_id(dept_id):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM departments WHERE id = %s", [dept_id])
        dept_data = cursor.fetchone()
        cursor.close()
        
        if dept_data:
            return Department(
                id=dept_data['id'],
                name=dept_data['name'],
                description=dept_data['description']
            )
        return None
    
    def save(self):
        cursor = mysql.connection.cursor()
        if self.id:
            # Update existing department
            cursor.execute(
                "UPDATE departments SET name = %s, description = %s WHERE id = %s",
                (self.name, self.description, self.id)
            )
        else:
            # Create new department
            cursor.execute(
                "INSERT INTO departments (name, description) VALUES (%s, %s)",
                (self.name, self.description)
            )
            self.id = cursor.lastrowid
        
        mysql.connection.commit()
        cursor.close()
        return self.id

class Complaint:
    def __init__(self, id=None, reference_id=None, title=None, description=None, category=None, 
                 location=None, landmark=None, contact_info=None, status=None, priority=None, 
                 department_id=None, created_at=None, updated_at=None):
        self.id = id
        self.reference_id = reference_id
        self.title = title
        self.description = description
        self.category = category
        self.location = location
        self.landmark = landmark
        self.contact_info = contact_info
        self.status = status
        self.priority = priority
        self.department_id = department_id
        self.created_at = created_at
        self.updated_at = updated_at
    
    @staticmethod
    def get_by_id(complaint_id):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM complaints WHERE id = %s", [complaint_id])
        complaint_data = cursor.fetchone()
        cursor.close()
        
        if complaint_data:
            return Complaint(
                id=complaint_data['id'],
                reference_id=complaint_data['reference_id'],
                title=complaint_data['title'],
                description=complaint_data['description'],
                category=complaint_data['category'],
                location=complaint_data['location'],
                landmark=complaint_data['landmark'],
                contact_info=complaint_data['contact_info'],
                status=complaint_data['status'],
                priority=complaint_data['priority'],
                department_id=complaint_data['department_id'],
                created_at=complaint_data['created_at'],
                updated_at=complaint_data['updated_at']
            )
        return None
    
    @staticmethod
    def get_by_reference_id(reference_id):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM complaints WHERE reference_id = %s", [reference_id])
        complaint_data = cursor.fetchone()
        cursor.close()
        
        if complaint_data:
            return Complaint(
                id=complaint_data['id'],
                reference_id=complaint_data['reference_id'],
                title=complaint_data['title'],
                description=complaint_data['description'],
                category=complaint_data['category'],
                location=complaint_data['location'],
                landmark=complaint_data['landmark'],
                contact_info=complaint_data['contact_info'],
                status=complaint_data['status'],
                priority=complaint_data['priority'],
                department_id=complaint_data['department_id'],
                created_at=complaint_data['created_at'],
                updated_at=complaint_data['updated_at']
            )
        return None
    
    def get_updates(self):
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT * FROM complaint_updates WHERE complaint_id = %s ORDER BY timestamp DESC",
            [self.id]
        )
        updates_data = cursor.fetchall()
        cursor.close()
        
        return updates_data
    
    def get_images(self):
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT * FROM complaint_images WHERE complaint_id = %s",
            [self.id]
        )
        images_data = cursor.fetchall()
        cursor.close()
        
        return [img['image_path'] for img in images_data]
    
    def save(self):
        cursor = mysql.connection.cursor()
        now = datetime.now()
        
        if self.id:
            # Update existing complaint
            cursor.execute(
                """UPDATE complaints 
                   SET title = %s, description = %s, category = %s, location = %s,
                       landmark = %s, contact_info = %s, status = %s, priority = %s,
                       department_id = %s, updated_at = %s
                   WHERE id = %s""",
                (self.title, self.description, self.category, self.location,
                 self.landmark, self.contact_info, self.status, self.priority,
                 self.department_id, now, self.id)
            )
        else:
            # Create new complaint
            cursor.execute(
                """INSERT INTO complaints 
                   (reference_id, title, description, category, location, landmark, 
                    contact_info, status, priority, department_id, created_at, updated_at) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (self.reference_id, self.title, self.description, self.category, 
                 self.location, self.landmark, self.contact_info, self.status, 
                 self.priority, self.department_id, now, now)
            )
            self.id = cursor.lastrowid
            
            # Generate reference ID if not provided
            if not self.reference_id:
                self.reference_id = f"CMP-{now.year}-{self.id}"
                cursor.execute(
                    "UPDATE complaints SET reference_id = %s WHERE id = %s",
                    (self.reference_id, self.id)
                )
        
        mysql.connection.commit()
        cursor.close()
        return self.id
    
    def add_update(self, status, message):
        cursor = mysql.connection.cursor()
        cursor.execute(
            """INSERT INTO complaint_updates 
               (complaint_id, status, message, timestamp) 
               VALUES (%s, %s, %s, NOW())""",
            (self.id, status, message)
        )
        
        # Update complaint status
        cursor.execute(
            "UPDATE complaints SET status = %s, updated_at = NOW() WHERE id = %s",
            (status, self.id)
        )
        
        mysql.connection.commit()
        cursor.close()

