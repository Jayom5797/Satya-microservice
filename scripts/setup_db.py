import sys
sys.path.append('.')

from app.database import init_db, test_connection, db

def setup_database():
    """Initialize database with collections and indexes"""
    print("🔧 Setting up database...")
    print("=" * 50)
    
    # Test connection
    if not test_connection():
        print("\n❌ Cannot connect to database. Check your MONGODB_URI in .env")
        print("\nMake sure:")
        print("1. MongoDB Atlas cluster is running")
        print("2. IP address is whitelisted")
        print("3. Connection string is correct in .env")
        return False
    
    print()
    
    # Create indexes
    init_db()
    
    print()
    
    # Verify collections
    collections = db.list_collection_names()
    if collections:
        print(f"📦 Existing collections: {', '.join(collections)}")
    else:
        print("📦 No collections yet (will be created on first insert)")
    
    print()
    print("=" * 50)
    print("✅ Database setup complete!")
    print("\nYou can now start the API server:")
    print("  uvicorn app.main:app --reload")
    return True

if __name__ == "__main__":
    setup_database()
