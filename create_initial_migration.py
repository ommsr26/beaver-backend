"""
Script to create initial Alembic migration
Run this after setting up Alembic to create the baseline migration
"""
import subprocess
import sys
import os

def main():
    print("=" * 60)
    print("Creating initial Alembic migration")
    print("=" * 60)
    
    # Check if alembic is installed
    try:
        import alembic
    except ImportError:
        print("❌ Alembic not installed. Please run: pip install -r requirements.txt")
        sys.exit(1)
    
    # Create initial migration
    print("\n📝 Creating initial migration...")
    try:
        result = subprocess.run(
            ["python", "-m", "alembic", "revision", "--autogenerate", "-m", "Initial migration - all tables"],
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)
        if result.stderr:
            print("Warnings:", result.stderr)
        print("\n✅ Initial migration created successfully!")
        print("\nNext steps:")
        print("1. Review the migration file in alembic/versions/")
        print("2. If you have existing data, you may want to mark this as a baseline:")
        print("   python -m alembic stamp head")
        print("3. Otherwise, apply the migration:")
        print("   python -m alembic upgrade head")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating migration: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        sys.exit(1)
    except FileNotFoundError:
        print("❌ Python not found. Please ensure Python is in your PATH.")
        sys.exit(1)

if __name__ == "__main__":
    main()

