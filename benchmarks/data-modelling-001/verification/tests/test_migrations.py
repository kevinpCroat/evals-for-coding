"""
Test migrations - verify Alembic migration runs successfully
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import pytest
import tempfile
import shutil
from pathlib import Path


def test_alembic_config_exists():
    """Test that alembic.ini exists"""
    base_dir = Path(__file__).parent.parent.parent
    alembic_ini = base_dir / 'alembic.ini'
    assert alembic_ini.exists(), "alembic.ini not found"


def test_alembic_directory_exists():
    """Test that alembic directory structure exists"""
    base_dir = Path(__file__).parent.parent.parent
    alembic_dir = base_dir / 'alembic'
    assert alembic_dir.exists(), "alembic/ directory not found"
    assert (alembic_dir / 'env.py').exists(), "alembic/env.py not found"
    assert (alembic_dir / 'script.py.mako').exists(), "alembic/script.py.mako not found"


def test_alembic_versions_directory():
    """Test that alembic versions directory exists"""
    base_dir = Path(__file__).parent.parent.parent
    versions_dir = base_dir / 'alembic' / 'versions'
    assert versions_dir.exists(), "alembic/versions/ directory not found"


def test_initial_migration_exists():
    """Test that initial migration file exists"""
    base_dir = Path(__file__).parent.parent.parent
    versions_dir = base_dir / 'alembic' / 'versions'

    # Look for any migration file (should be at least one)
    migration_files = list(versions_dir.glob('*.py'))
    migration_files = [f for f in migration_files if f.name != '__pycache__']

    assert len(migration_files) > 0, "No migration files found in alembic/versions/"


def test_migration_runs_successfully():
    """Test that the migration can run and create all tables"""
    import subprocess

    base_dir = Path(__file__).parent.parent.parent

    # Create a temporary directory for test database
    with tempfile.TemporaryDirectory() as tmpdir:
        test_db = Path(tmpdir) / 'test.db'

        # Create a temporary alembic.ini pointing to test database
        alembic_ini = base_dir / 'alembic.ini'
        test_ini = Path(tmpdir) / 'alembic.ini'

        # Read original alembic.ini
        with open(alembic_ini, 'r') as f:
            config = f.read()

        # Replace database URL with test database
        config = config.replace(
            'sqlalchemy.url = sqlite:///blog.db',
            f'sqlalchemy.url = sqlite:///{test_db}'
        )

        # Write test config
        with open(test_ini, 'w') as f:
            f.write(config)

        # Run alembic upgrade
        try:
            result = subprocess.run(
                ['alembic', '-c', str(test_ini), 'upgrade', 'head'],
                cwd=str(base_dir),
                capture_output=True,
                text=True,
                timeout=30
            )

            # Check if migration succeeded
            if result.returncode != 0:
                pytest.fail(f"Migration failed:\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}")

            # Verify database was created
            assert test_db.exists(), "Database file was not created by migration"

            # Verify tables were created
            import sqlite3
            conn = sqlite3.connect(test_db)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            conn.close()

            expected_tables = ['users', 'articles', 'categories', 'tags', 'comments',
                             'article_tags', 'user_follows', 'alembic_version']

            for table in expected_tables:
                assert table in tables, f"Table {table} not created by migration"

        except subprocess.TimeoutExpired:
            pytest.fail("Migration timed out after 30 seconds")
        except FileNotFoundError:
            pytest.skip("Alembic not installed - skipping migration test")


def test_migration_has_upgrade_and_downgrade():
    """Test that migration has both upgrade and downgrade functions"""
    base_dir = Path(__file__).parent.parent.parent
    versions_dir = base_dir / 'alembic' / 'versions'

    migration_files = [f for f in versions_dir.glob('*.py') if f.name != '__pycache__']

    for migration_file in migration_files:
        with open(migration_file, 'r') as f:
            content = f.read()

        assert 'def upgrade()' in content, f"{migration_file.name} missing upgrade() function"
        assert 'def downgrade()' in content, f"{migration_file.name} missing downgrade() function"
