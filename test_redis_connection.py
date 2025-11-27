"""
Quick Redis Connection Test
"""

import redis

# Your Redis endpoint
REDIS_URL = "redis://redis-14368.c99.us-east-1-4.ec2.cloud.redislabs.com:14368"

print("=" * 60)
print("Testing Redis Connection")
print("=" * 60)
print()

try:
    # Try connecting without password
    print("Attempting connection without password...")
    r = redis.from_url(REDIS_URL)
    r.ping()
    print("✅ SUCCESS! No password needed!")
    print()
    
    # Test set/get
    r.set('test', 'Hello from Python!')
    value = r.get('test')
    print(f"✅ Test successful: {value.decode()}")
    print()
    print("Your Redis is working!")
    
except redis.exceptions.AuthenticationError:
    print("❌ Authentication required - password needed")
    print()
    print("To find your password:")
    print("1. In Redis dashboard, look for 'Security' tab")
    print("2. Or check 'Data Access Control' in left sidebar")
    print("3. Look for 'Default user password'")
    print()
    
except redis.exceptions.ConnectionError as e:
    print(f"❌ Connection failed: {e}")
    print()
    print("Check:")
    print("1. Internet connection")
    print("2. Redis endpoint is correct")
    print("3. Database is active in Redis dashboard")
    print()
    
except Exception as e:
    print(f"❌ Error: {e}")
    print()

print("=" * 60)
