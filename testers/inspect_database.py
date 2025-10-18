"""
Database Inspection Script for HubSpot Logging AI Agent
Provides detailed database analysis and verification
"""

import sqlite3
import os
from datetime import datetime
from pathlib import Path

class DatabaseInspector:
    def __init__(self, db_path="data/database.db"):
        self.db_path = db_path
        self.conn = None
    
    def connect(self):
        """Connect to the database"""
        if not os.path.exists(self.db_path):
            print(f"❌ Database file not found: {self.db_path}")
            return False
        
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row  # Enable column access by name
            return True
        except Exception as e:
            print(f"❌ Error connecting to database: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from the database"""
        if self.conn:
            self.conn.close()
    
    def print_header(self, title):
        """Print a formatted header"""
        print("\n" + "=" * 60)
        print(f" {title}")
        print("=" * 60)
    
    def get_database_info(self):
        """Get basic database information"""
        self.print_header("DATABASE INFORMATION")
        
        if not self.connect():
            return
        
        try:
            cursor = self.conn.cursor()
            
            # Database file info
            file_size = os.path.getsize(self.db_path)
            print(f"📁 Database File: {self.db_path}")
            print(f"📏 File Size: {file_size:,} bytes")
            print(f"📅 Last Modified: {datetime.fromtimestamp(os.path.getmtime(self.db_path))}")
            
            # SQLite version
            cursor.execute("SELECT sqlite_version();")
            version = cursor.fetchone()[0]
            print(f"🔧 SQLite Version: {version}")
            
            # Database schema version
            cursor.execute("PRAGMA user_version;")
            user_version = cursor.fetchone()[0]
            print(f"📋 Schema Version: {user_version}")
            
        except Exception as e:
            print(f"❌ Error getting database info: {e}")
        finally:
            self.disconnect()
    
    def list_tables(self):
        """List all tables in the database"""
        self.print_header("DATABASE TABLES")
        
        if not self.connect():
            return
        
        try:
            cursor = self.conn.cursor()
            
            # Get all tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
            tables = cursor.fetchall()
            
            if not tables:
                print("📋 No tables found in database")
                return
            
            print(f"📊 Found {len(tables)} tables:")
            for i, table in enumerate(tables, 1):
                table_name = table[0]
                
                # Get row count
                cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
                count = cursor.fetchone()[0]
                
                print(f"  {i}. {table_name} ({count} rows)")
            
        except Exception as e:
            print(f"❌ Error listing tables: {e}")
        finally:
            self.disconnect()
    
    def inspect_table(self, table_name):
        """Inspect a specific table"""
        self.print_header(f"TABLE INSPECTION: {table_name}")
        
        if not self.connect():
            return
        
        try:
            cursor = self.conn.cursor()
            
            # Check if table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table_name,))
            if not cursor.fetchone():
                print(f"❌ Table '{table_name}' does not exist")
                return
            
            # Get table schema
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            
            print("📋 Table Schema:")
            print("  Column Name | Type | Not Null | Primary Key | Default")
            print("  " + "-" * 60)
            for col in columns:
                print(f"  {col[1]:<12} | {col[2]:<8} | {col[3]:<8} | {col[5]:<11} | {col[4] or 'None'}")
            
            # Get row count
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            count = cursor.fetchone()[0]
            print(f"\n📊 Total Rows: {count}")
            
            # Get sample data
            if count > 0:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 5;")
                rows = cursor.fetchall()
                
                print(f"\n📄 Sample Data (showing {len(rows)} of {count} rows):")
                for i, row in enumerate(rows, 1):
                    print(f"  Row {i}: {dict(row)}")
            else:
                print("\n📄 No data in table")
            
            # Get indexes
            cursor.execute(f"PRAGMA index_list({table_name});")
            indexes = cursor.fetchall()
            
            if indexes:
                print(f"\n🔍 Indexes:")
                for idx in indexes:
                    print(f"  - {idx[1]} ({'UNIQUE' if idx[2] else 'NON-UNIQUE'})")
            
        except Exception as e:
            print(f"❌ Error inspecting table: {e}")
        finally:
            self.disconnect()
    
    def inspect_all_tables(self):
        """Inspect all tables"""
        if not self.connect():
            return
        
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
            tables = cursor.fetchall()
            
            for table in tables:
                self.inspect_table(table[0])
                
        except Exception as e:
            print(f"❌ Error inspecting tables: {e}")
        finally:
            self.disconnect()
    
    def run_queries(self):
        """Run useful queries"""
        self.print_header("USEFUL QUERIES")
        
        if not self.connect():
            return
        
        try:
            cursor = self.conn.cursor()
            
            # Check if users table exists and has data
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
            if cursor.fetchone():
                cursor.execute("SELECT COUNT(*) FROM users;")
                user_count = cursor.fetchone()[0]
                print(f"👥 Total Users: {user_count}")
                
                if user_count > 0:
                    cursor.execute("SELECT id, username, name, email, is_active FROM users LIMIT 5;")
                    users = cursor.fetchall()
                    print("📋 Sample Users:")
                    for user in users:
                        print(f"  ID: {user[0]}, Username: {user[1]}, Name: {user[2]}, Email: {user[3]}, Active: {user[4]}")
            else:
                print("👥 Users table not found")
            
            # Check if logs table exists and has data
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='logs';")
            if cursor.fetchone():
                cursor.execute("SELECT COUNT(*) FROM logs;")
                log_count = cursor.fetchone()[0]
                print(f"\n📝 Total Logs: {log_count}")
                
                if log_count > 0:
                    cursor.execute("SELECT log_type, sync_status, COUNT(*) FROM logs GROUP BY log_type, sync_status;")
                    log_stats = cursor.fetchall()
                    print("📊 Log Statistics:")
                    for stat in log_stats:
                        print(f"  {stat[0]} ({stat[1]}): {stat[2]} entries")
            else:
                print("📝 Logs table not found")
            
            # Check if sessions table exists and has data
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='chat_sessions';")
            if cursor.fetchone():
                cursor.execute("SELECT COUNT(*) FROM chat_sessions;")
                session_count = cursor.fetchone()[0]
                print(f"\n💬 Total Sessions: {session_count}")
                
                if session_count > 0:
                    cursor.execute("SELECT status, COUNT(*) FROM chat_sessions GROUP BY status;")
                    session_stats = cursor.fetchall()
                    print("📊 Session Statistics:")
                    for stat in session_stats:
                        print(f"  {stat[0]}: {stat[1]} sessions")
            else:
                print("💬 Sessions table not found")
            
        except Exception as e:
            print(f"❌ Error running queries: {e}")
        finally:
            self.disconnect()
    
    def export_data(self, output_file="database_export.txt"):
        """Export database data to a text file"""
        self.print_header("EXPORTING DATABASE")
        
        if not self.connect():
            return
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"Database Export - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 60 + "\n\n")
                
                cursor = self.conn.cursor()
                
                # Get all tables
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
                tables = cursor.fetchall()
                
                for table in tables:
                    table_name = table[0]
                    f.write(f"TABLE: {table_name}\n")
                    f.write("-" * 40 + "\n")
                    
                    # Get table schema
                    cursor.execute(f"PRAGMA table_info({table_name});")
                    columns = cursor.fetchall()
                    f.write("Columns:\n")
                    for col in columns:
                        f.write(f"  {col[1]} ({col[2]})\n")
                    
                    # Get all data
                    cursor.execute(f"SELECT * FROM {table_name};")
                    rows = cursor.fetchall()
                    f.write(f"\nData ({len(rows)} rows):\n")
                    for row in rows:
                        f.write(f"  {dict(row)}\n")
                    
                    f.write("\n" + "=" * 60 + "\n\n")
            
            print(f"✅ Database exported to: {output_file}")
            
        except Exception as e:
            print(f"❌ Error exporting database: {e}")
        finally:
            self.disconnect()

def main():
    """Main function"""
    print("HubSpot Logging AI Agent - Database Inspector")
    
    inspector = DatabaseInspector()
    
    while True:
        print("\n" + "=" * 50)
        print(" Database Inspector Menu")
        print("=" * 50)
        print("1. Database Information")
        print("2. List Tables")
        print("3. Inspect All Tables")
        print("4. Inspect Specific Table")
        print("5. Run Useful Queries")
        print("6. Export Database")
        print("7. Exit")
        print("=" * 50)
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == "1":
            inspector.get_database_info()
        elif choice == "2":
            inspector.list_tables()
        elif choice == "3":
            inspector.inspect_all_tables()
        elif choice == "4":
            table_name = input("Enter table name: ").strip()
            if table_name:
                inspector.inspect_table(table_name)
        elif choice == "5":
            inspector.run_queries()
        elif choice == "6":
            output_file = input("Enter output filename (default: database_export.txt): ").strip()
            if not output_file:
                output_file = "database_export.txt"
            inspector.export_data(output_file)
        elif choice == "7":
            print("\n👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
