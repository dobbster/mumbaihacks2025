#!/usr/bin/env python3
"""Verify MongoDB connection and setup."""

import os
import sys
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

def verify_mongodb():
    """Verify MongoDB connection and database setup."""
    mongo_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    db_name = os.getenv("MONGODB_DB_NAME", "misinformation_detection")
    
    print(f"Connecting to MongoDB: {mongo_url}")
    print(f"Database: {db_name}")
    print("-" * 50)
    
    try:
        # Connect to MongoDB
        client = MongoClient(mongo_url, serverSelectionTimeoutMS=5000)
        
        # Test connection
        client.admin.command('ping')
        print("✅ MongoDB connection successful!")
        
        # Check database
        db = client[db_name]
        print(f"✅ Database '{db_name}' accessible")
        
        # Check collections
        collections = db.list_collection_names()
        print(f"✅ Found {len(collections)} collection(s): {collections}")
        
        # Check indexes on datapoints collection
        if 'datapoints' in collections:
            indexes = db.datapoints.list_indexes()
            index_names = [idx['name'] for idx in indexes]
            print(f"✅ Collection 'datapoints' has {len(index_names)} indexes: {index_names}")
        else:
            print("⚠️  Collection 'datapoints' not found (will be created on first insert)")
        
        # Check document count
        if 'datapoints' in collections:
            count = db.datapoints.count_documents({})
            print(f"✅ Collection 'datapoints' has {count} document(s)")
        
        print("-" * 50)
        print("✅ MongoDB setup verified successfully!")
        return True
        
    except ConnectionFailure as e:
        print(f"❌ MongoDB connection failed: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure MongoDB is running: docker-compose ps")
        print("2. Check MongoDB logs: docker-compose logs mongodb")
        print("3. Verify MONGODB_URL in your .env file")
        return False
        
    except ServerSelectionTimeoutError as e:
        print(f"❌ MongoDB server selection timeout: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure MongoDB container is running: docker-compose up -d")
        print("2. Check if port 27017 is accessible")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = verify_mongodb()
    sys.exit(0 if success else 1)
