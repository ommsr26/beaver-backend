"""
Quick script to check database schema
"""
import sqlite3

conn = sqlite3.connect('beaver.db')
cursor = conn.cursor()

# Check accounts table structure
cursor.execute("PRAGMA table_info(accounts)")
columns = cursor.fetchall()
print("accounts table columns:")
for col in columns:
    print(f"  - {col[1]} ({col[2]})")

print("\n" + "-" * 60)

# Check refresh_tokens table
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='refresh_tokens'")
if cursor.fetchone():
    cursor.execute("PRAGMA table_info(refresh_tokens)")
    columns = cursor.fetchall()
    print("refresh_tokens table columns:")
    for col in columns:
        print(f"  - {col[1]} ({col[2]})")
else:
    print("❌ refresh_tokens table not found")

print("\n" + "-" * 60)

# Check api_keys table structure
cursor.execute("PRAGMA table_info(api_keys)")
columns = cursor.fetchall()
print("api_keys table columns:")
for col in columns:
    print(f"  - {col[1]} ({col[2]})")

conn.close()

