"""
Background Worker - Windows Compatible
Processes jobs from Redis queue without RQ Worker class
"""

import redis
import time
import pickle
from app.config import settings
from app.orchestrator import process_submission

# Connect to Redis
redis_conn = redis.from_url(settings.redis_url)

def get_job_from_queue(queue_name):
    """Manually fetch job from Redis queue"""
    # RQ stores jobs in lists with key format: rq:queue:{name}
    job_id = redis_conn.lpop(f'rq:queue:{queue_name}')
    
    if job_id:
        # Decode job_id if it's bytes
        if isinstance(job_id, bytes):
            job_id = job_id.decode('utf-8')
        
        # Get job data from Redis
        job_key = f'rq:job:{job_id}'
        job_data = redis_conn.hgetall(job_key)
        
        return job_id, job_data
    
    return None, None

def execute_job(job_id, job_data):
    """Execute the job function"""
    try:
        # Debug: print job data keys
        print(f"🔍 Job data keys: {list(job_data.keys())}")
        
        # Get the submission_id from job data
        # Try different field names
        data_field = job_data.get(b'data') or job_data.get('data')
        
        if not data_field:
            # Try to get args directly
            args_field = job_data.get(b'args') or job_data.get('args')
            if args_field:
                # Args might be pickled
                try:
                    args = pickle.loads(args_field)
                    if args and len(args) > 0:
                        submission_id = args[0]
                        print(f"✓ Extracted submission_id from args: {submission_id}")
                        result = process_submission(submission_id)
                        return result
                except:
                    pass
        
        if data_field:
            # Try to unpickle the job data
            try:
                unpickled = pickle.loads(data_field)
                print(f"🔍 Unpickled data type: {type(unpickled)}")
                print(f"🔍 Unpickled data: {unpickled}")
                
                # RQ stores data as (args, kwargs, func_name, ...)
                if isinstance(unpickled, tuple) and len(unpickled) >= 2:
                    args = unpickled[0]  # First element is args tuple
                    if args and len(args) > 0:
                        submission_id = args[0]
                        print(f"✓ Extracted submission_id: {submission_id}")
                        result = process_submission(submission_id)
                        return result
                        
            except Exception as e:
                print(f"⚠️  Unpickle error: {e}")
        
        # Fallback: try to get description field which might contain the submission_id
        desc_field = job_data.get(b'description') or job_data.get('description')
        if desc_field:
            if isinstance(desc_field, bytes):
                desc_field = desc_field.decode('utf-8')
            print(f"🔍 Job description: {desc_field}")
            
            # Extract submission_id from description like "app.orchestrator.process_submission('691f326087526dc3df693362')"
            import re
            match = re.search(r"process_submission\('([^']+)'\)", desc_field)
            if match:
                submission_id = match.group(1)
                print(f"✓ Extracted submission_id from description: {submission_id}")
                result = process_submission(submission_id)
                return result
        
        raise Exception("Could not extract submission_id from job data")
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise Exception(f"Job execution failed: {e}")

def update_job_status(job_id, status, result=None):
    """Update job status in Redis"""
    job_key = f'rq:job:{job_id}'
    
    redis_conn.hset(job_key, 'status', status)
    
    if result:
        redis_conn.hset(job_key, 'result', pickle.dumps(result))
    
    if status == 'finished':
        redis_conn.hset(job_key, 'ended_at', time.time())

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Starting Custom Worker (Windows Compatible)")
    print("=" * 60)
    print(f"📡 Redis: {settings.redis_url[:50]}...")
    print(f"📋 Queues: default, high, low")
    print("=" * 60)
    print("\n✓ Worker started successfully")
    print("✓ Listening for jobs...\n")
    
    queue_names = ['high', 'default', 'low']  # Priority order
    
    while True:
        try:
            job_found = False
            
            # Check each queue in priority order
            for queue_name in queue_names:
                job_id, job_data = get_job_from_queue(queue_name)
                
                if job_id and job_data:
                    job_found = True
                    
                    print(f"\n{'='*60}")
                    print(f"📝 Processing job: {job_id}")
                    print(f"{'='*60}\n")
                    
                    try:
                        # Update status to started
                        update_job_status(job_id, 'started')
                        
                        # Execute the job
                        result = execute_job(job_id, job_data)
                        
                        # Update status to finished
                        update_job_status(job_id, 'finished', result)
                        
                        print(f"\n{'='*60}")
                        print(f"✅ Job completed: {job_id}")
                        print(f"{'='*60}\n")
                        
                    except Exception as e:
                        print(f"\n{'='*60}")
                        print(f"❌ Job failed: {job_id}")
                        print(f"Error: {e}")
                        print(f"{'='*60}\n")
                        
                        # Update status to failed
                        update_job_status(job_id, 'failed')
                    
                    break  # Process one job at a time
            
            # If no job found, sleep briefly
            if not job_found:
                time.sleep(2)
            
        except KeyboardInterrupt:
            print("\n\n👋 Worker stopped by user")
            break
        except Exception as e:
            print(f"⚠️  Worker error: {e}")
            time.sleep(5)
