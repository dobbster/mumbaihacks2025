#!/usr/bin/env python3
"""Check Together AI API key and connection.

Run this script with: uv run python scripts/check_together_api.py
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Check if running in uv environment
try:
    import langchain_together
except ImportError:
    print("⚠️  Warning: langchain_together not found in current Python environment")
    print("\nTo fix this:")
    print("1. Run with uv: uv run python scripts/check_together_api.py")
    print("2. Or install dependencies: uv sync")
    print("3. Or activate uv environment first")
    sys.exit(1)

def check_together_api():
    """Check if Together AI API key is configured."""
    print("Checking Together AI Configuration")
    print("=" * 50)
    
    # Check environment variable
    api_key = os.getenv("TOGETHER_API_KEY")
    model = os.getenv("TOGETHER_EMBEDDING_MODEL", "BAAI/bge-base-en-v1.5")
    
    if not api_key:
        print("❌ TOGETHER_API_KEY not found in environment variables")
        print("\nTo fix this:")
        print("1. Get your API key from: https://api.together.xyz/")
        print("2. Set it in your .env file:")
        print("   TOGETHER_API_KEY=your_api_key_here")
        print("3. Or export it in your shell:")
        print("   export TOGETHER_API_KEY=your_api_key_here")
        return False
    
    print(f"✅ TOGETHER_API_KEY found (length: {len(api_key)})")
    print(f"✅ Model: {model}")
    
    # Try to import and test
    try:
        from langchain_together import TogetherEmbeddings
    except ImportError as e:
        print(f"❌ Failed to import langchain_together: {e}")
        print("\nTo fix this:")
        print("1. Make sure you're using uv: uv run python scripts/check_together_api.py")
        print("2. Or install dependencies: uv sync")
        print("3. Or add the package: uv add langchain-together")
        return False
    
    try:
        print("\nTesting Together AI connection...")
        embeddings = TogetherEmbeddings(
            model=model,
            together_api_key=api_key
        )
        
        # Test with a simple query
        test_text = "This is a test"
        print(f"Generating embedding for: '{test_text}'...")
        embedding = embeddings.embed_query(test_text)
        
        print(f"✅ Success! Generated embedding of dimension {len(embedding)}")
        return True
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Failed to connect to Together AI: {error_msg}")
        print("\nTroubleshooting:")
        if "Connection" in error_msg or "connection" in error_msg.lower():
            print("1. Check your internet connection")
            print("2. Verify Together AI API is accessible")
            print("3. Check if there's a firewall blocking the connection")
        print("4. Verify your API key is correct at https://api.together.xyz/")
        print("5. Check your API quota/limits")
        return False

if __name__ == "__main__":
    success = check_together_api()
    sys.exit(0 if success else 1)
