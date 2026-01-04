# 🔄 Applying the Initial Migration

## Important: You Have an Existing Database

Since you already have a database with tables and data, you have two options:

## Option 1: Mark Current State as Baseline (Recommended for Existing Data)

If your database structure is already correct, mark it as the baseline:

```bash
# This tells Alembic that your current database matches the latest migration
# without actually running any migrations
alembic stamp head
```

**When to use this:**
- Your database already has all the tables
- You want to start tracking changes from now on
- You don't need to apply the type changes immediately

## Option 2: Apply the Migration (Upgrade Existing Database)

If you want to apply the PostgreSQL-compatibility changes:

```bash
# Review the migration first
# The migration will:
# - Convert Float → Numeric types
# - Add NOT NULL constraints
# - Update foreign keys with CASCADE
# - Change VARCHAR → Text for long strings

# Apply the migration
alembic upgrade head
```

**When to use this:**
- You want to upgrade your existing database to PostgreSQL-compatible types
- You're okay with the migration making these changes

**Note:** SQLite has limitations with ALTER TABLE. Some operations might be skipped on SQLite but will apply when you switch to PostgreSQL.

## Option 3: Fresh Start (For New Installations)

If starting fresh:

```bash
# Apply all migrations
alembic upgrade head
```

## Verify After Applying

```bash
# Check current version
alembic current

# Should show: bf1e532df22f (head)
```

## Testing the Migration

### Test Rollback (Optional)

```bash
# Rollback one migration
alembic downgrade -1

# Re-apply
alembic upgrade head
```

## Next Steps

After applying (or stamping):

1. **Future model changes:**
   ```bash
   alembic revision --autogenerate -m "Description"
   alembic upgrade head
   ```

2. **Switch to PostgreSQL:**
   ```env
   DATABASE_URL=postgresql+psycopg2://user:password@localhost/beaver
   ```
   ```bash
   alembic upgrade head
   ```

## Troubleshooting

### Migration Fails on SQLite

SQLite has limited ALTER TABLE support. If the migration fails:
- Use Option 1 (stamp head) instead
- The migration will work properly when you switch to PostgreSQL

### Foreign Key Errors

If you get foreign key constraint errors:
- Ensure foreign keys are enabled (they are by default in our setup)
- Check that referenced tables exist

### Type Conversion Errors

If numeric type conversions fail:
- The migration is designed to be safe
- Data should be preserved
- If issues occur, restore from backup and use Option 1

## Recommendation

**For your existing database with data:**
1. **Backup first:** `cp beaver.db beaver.db.backup`
2. **Try Option 1 (stamp head)** - Safest for existing data
3. **Or Option 2 (upgrade head)** - If you want the type improvements now

The migration system is now ready for future changes!

