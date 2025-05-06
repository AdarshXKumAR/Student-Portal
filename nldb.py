# nldb.py
from flask import Flask, session
import google.generativeai as genai
import re
import json

class NLDatabaseInteractor:
    def __init__(self, mysql, api_key):
        self.mysql = mysql
        self.api_key = api_key
        
        # Initialize Gemini API
        genai.configure(api_key="AIzaSyDrJl08iyaExlORIZKOj8WLJmM-lLNu_pE")
        
        # Get database schema
        self.schema = self._get_database_schema()

    def _get_database_schema(self):
        """Fetch the database schema for context"""
        try:
            cur = self.mysql.connection.cursor()
            
            # Get tables
            cur.execute("SHOW TABLES")
            tables = [table['Tables_in_user_auth_db'] for table in cur.fetchall()]
            
            schema = {}
            
            # Get columns for each table
            for table in tables:
                cur.execute(f"DESCRIBE {table}")
                columns = cur.fetchall()
                schema[table] = [col['Field'] for col in columns]
            
            cur.close()
            return schema
        except Exception as e:
            return {}

    def execute_query(self, nl_query):
        """Execute a natural language query and return results"""
        try:
            # Generate SQL from natural language query
            sql = self._generate_sql(nl_query)
            
            if not sql:
                return {
                    'success': False,
                    'error': 'Failed to generate SQL query',
                    'sql': 'No SQL generated'
                }
            
            # Execute the SQL query
            cur = self.mysql.connection.cursor()
            cur.execute(sql)
            
            # For SELECT queries
            if sql.strip().upper().startswith('SELECT'):
                results = cur.fetchall()
                columns = [column[0] for column in cur.description]
                
                cur.close()
                return {
                    'success': True,
                    'sql': sql,
                    'columns': columns,
                    'results': results
                }
            else:
                # For non-SELECT queries (INSERT, UPDATE, DELETE)
                self.mysql.connection.commit()
                affected_rows = cur.rowcount
                cur.close()
                
                return {
                    'success': True,
                    'sql': sql,
                    'message': f'Query executed successfully. {affected_rows} rows affected.'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'sql': sql if 'sql' in locals() else 'No SQL generated'
            }

    def _generate_sql(self, nl_query):
        """Generate SQL query from natural language using Gemini"""
        try:
            # Define the database schema
            schema_text = """
            Database Schema: 
            Table: users
            Columns: id (INT, PRIMARY KEY, AUTO_INCREMENT),
                    name (VARCHAR(100), NOT NULL),
                    email (VARCHAR(100), NOT NULL, UNIQUE),
                    username (VARCHAR(30), NOT NULL, UNIQUE),
                    password (VARCHAR(255), NOT NULL),
                    register_date (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)

            Table: grades
            Columns: id (INT, PRIMARY KEY, AUTO_INCREMENT),
                    user_id (INT, FOREIGN KEY REFERENCES users(id) ON DELETE CASCADE),
                    subject (VARCHAR(100), NOT NULL),
                    score (INT, NOT NULL),
                    grade (CHAR(2), NOT NULL),
                    date_added (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
            """

            # Modify the prompt if the query is related to the user's profile or marks
            user_id = session.get('user_id')
            username = session.get('username')

            if "my profile" in nl_query.lower() or "my marks" in nl_query.lower():
                user_condition = f" WHERE users.id = {user_id} " if user_id else ""
                nl_query += f" (Ensure the SQL query filters the result for user_id={user_id} and includes the name from the users table.)"

            # Create the prompt for Gemini
            prompt = f"""
            {schema_text} 

            Given the database schema above, convert the following natural language query into a valid SQL query:

            Natural Language Query: {nl_query}

            Return ONLY the SQL query with no additional explanations, comments, or markdown formatting.
            """

            # Get response from Gemini
            model = genai.GenerativeModel('gemini-1.5-pro')
            response = model.generate_content(prompt)

            # Extract the SQL query from the response
            sql_query = response.text.strip()

            # Remove any markdown code blocks if present
            sql_query = re.sub(r'^```sql\s*|^```\s*|\s*```$', '', sql_query, flags=re.MULTILINE)

            return sql_query

            
        except Exception as e:
            return None