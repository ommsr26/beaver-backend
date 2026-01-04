# 🗄️ Database Migrations Guide

## Overview

Beaver uses **Alembic** for database schema migrations, enabling safe, version-controlled database changes that work with both SQLite (development) and PostgreSQL (production).

## Quick Start

### First Time Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create initial migration:**
   ```bash
   python create_initial_migration.py
   ```
   
   This generates a migration file in `alembic/versions/` based on your current models.

3. **Review the migration:**
   Open the generated file in `alembic/versions/` and verify the changes.

4. **Apply the migration:**
   ```bash
   python -m alembic upgrade head
   ```

### Existing Database

If you already have a database with tables:

1. **Mark current state as baseline:**
   ```bash
   python -m alembic stamp head
   ```
   
   This tells Alembic that your current database matches the latest migration without actually running migrations.

2. **Future changes:**
   ```bash
   # Make changes to models in app/database/models.py
   python -m alembic revision --autogenerate -m "Description"
   python -m alembic upgrade head
   ```

## Common Commands

### Create a New Migration

```bash
# Auto-generate from model changes
python -m alembic revision --autogenerate -m "Add new field to accounts"

# Create empty migration (for data migrations)
python -m alembic revision -m "Migrate existing data"
```

### Apply Migrations

```bash
# Apply all pending migrations
python -m alembic upgrade head

# Apply up to a specific revision
python -m alembic upgrade <revision_id>

# Apply one migration at a time
python -m alembic upgrade +1
```

### Rollback Migrations

```bash
# Rollback one migration
python -m alembic downgrade -1

# Rollback to a specific revision
python -m alembic downgrade <revision_id>

# Rollback all migrations
python -m alembic downgrade base
```

### Check Status

```bash
# Show current migration version
python -m alembic current

# Show migration history
python -m alembic history

# Show pending migrations
python -m alembic heads
```

## Database Configuration

### SQLite (Development)

Default configuration - no setup needed:
```env
# DATABASE_URL not set, or:
DATABASE_URL=sqlite:///./beaver.db
```

### PostgreSQL (Production)

1. **Install PostgreSQL driver:**
   ```bash
   pip install psycopg2-binary
   ```

2. **Set database URL:**
   ```env
   DATABASE_URL=postgresql+psycopg2://user:password@localhost/beaver
   ```

3. **Create database:**
   ```sql
   CREATE DATABASE beaver;
   ```

4. **Run migrations:**
   ```bash
   python -m alembic upgrade head
   ```

## Migration Workflow

### Making Model Changes

1. **Edit models** in `app/database/models.py`

2. **Generate migration:**
   ```bash
   python -m alembic revision --autogenerate -m "Description"
   ```

3. **Review generated migration:**
   - Check `alembic/versions/` for the new file
   - Verify `upgrade()` and `downgrade()` functions
   - Ensure no data loss

4. **Test migration:**
   ```bash
   # Apply
   python -m alembic upgrade head
   
   # Rollback
   python -m alembic downgrade -1
   
   # Re-apply
   python -m alembic upgrade head
   ```

5. **Commit to version control:**
   ```bash
   git add alembic/versions/<migration_file>.py
   git commit -m "Add migration: Description"
   ```

## Migration Best Practices

### ✅ Do's

- **Always review auto-generated migrations** before applying
- **Test migrations** on a copy of production data
- **Write reversible migrations** (implement both `upgrade()` and `downgrade()`)
- **Use transactions** for data migrations
- **Add indexes** for frequently queried columns
- **Use nullable=True** for new columns on existing tables (add data, then make NOT NULL)

### ❌ Don'ts

- **Don't modify existing migration files** after they've been applied
- **Don't delete migration files** from version control
- **Don't skip migrations** - always apply in order
- **Don't use DROP TABLE** without careful consideration
- **Don't hardcode values** - use environment variables

## Example Migrations

### Adding a Column

```python
def upgrade():
    op.add_column('accounts', 
        sa.Column('new_field', sa.String(255), nullable=True)
    )

def downgrade():
    op.drop_column('accounts', 'new_field')
```

### Adding an Index

```python
def upgrade():
    op.create_index('ix_accounts_email', 'accounts', ['email'])

def downgrade():
    op.drop_index('ix_accounts_email', 'accounts')
```

### Data Migration

```python
def upgrade():
    # Add column
    op.add_column('accounts', sa.Column('status', sa.String(50), nullable=True))
    
    # Migrate data
    connection = op.get_bind()
    connection.execute(
        sa.text("UPDATE accounts SET status = 'active' WHERE status IS NULL")
    )
    
    # Make NOT NULL
    op.alter_column('accounts', 'status', nullable=False)

def downgrade():
    op.drop_column('accounts', 'status')
```

## Troubleshooting

### Migration Conflicts

If migrations are out of sync:

```bash
# Check current state
python -m alembic current

# Check heads
python -m alembic heads

# Merge branches (if needed)
python -m alembic merge -m "Merge branches" <rev1> <rev2>
```

### Failed Migration

If a migration fails:

1. **Check the error message**
2. **Rollback if needed:**
   ```bash
   python -m alembic downgrade -1
   ```
3. **Fix the migration file**
4. **Re-apply:**
   ```bash
   python -m alembic upgrade head
   ```

### SQLite vs PostgreSQL Differences

Some operations differ between databases:

- **ALTER TABLE ADD COLUMN**: Works differently in SQLite
- **DROP COLUMN**: Not supported in SQLite (requires table recreation)
- **Foreign Keys**: Must be enabled explicitly in SQLite

Alembic handles most differences automatically, but review migrations when switching databases.

## Production Deployment

### Pre-deployment Checklist

- [ ] All migrations tested locally
- [ ] Database backup created
- [ ] Migration rollback plan documented
- [ ] Environment variables configured
- [ ] Database connection tested

### Deployment Steps

1. **Backup database:**
   ```bash
   pg_dump beaver > backup_$(date +%Y%m%d).sql
   ```

2. **Run migrations:**
   ```bash
   python -m alembic upgrade head
   ```

3. **Verify:**
   ```bash
   python -m alembic current
   ```

4. **Monitor application logs** for errors

### Rollback Plan

If issues occur:

```bash
# Rollback to previous version
python -m alembic downgrade -1

# Or restore from backup
psql beaver < backup_YYYYMMDD.sql
```

## Migration Files Structure

```
alembic/
├── versions/
│   ├── 001_initial_migration.py
│   ├── 002_add_password_auth.py
│   └── ...
├── env.py              # Alembic configuration
└── script.py.mako      # Migration template
```

Each migration file contains:
- `revision` - Unique identifier
- `down_revision` - Previous migration
- `upgrade()` - Apply changes
- `downgrade()` - Rollback changes

## Additional Resources

- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [SQLAlchemy Migrations Guide](https://docs.sqlalchemy.org/en/20/core/metadata.html)
- [PostgreSQL Migration Best Practices](https://www.postgresql.org/docs/current/ddl-alter.html)

