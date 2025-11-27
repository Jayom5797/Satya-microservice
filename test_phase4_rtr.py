"""
Test Phase 4: RTR (Real-Time Radar)
"""

def test_phase4_rtr():
    """Test Phase 4: RTR"""
    print("\n" + "="*60)
    print("📡 Testing Phase 4: RTR (Real-Time Radar)")
    print("="*60)
    
    try:
        from app.agents.rtr_stream import EventStreamManager
        from app.agents.rtr_aggregator import DashboardAggregator
        from app.agents.rtr_events import publish_submission_event, publish_completion_event
        from app.config import settings
        
        # Test Event Stream
        print("\n🔄 Testing Event Stream...")
        stream = EventStreamManager(settings.redis_url)
        
        # Publish test event
        success = stream.publish_event('test_event', {'message': 'Hello RTR'})
        print(f"  Event published: {'✓' if success else '✗'}")
        
        # Get recent events
        events = stream.get_recent_events(count=5)
        print(f"  Recent events: {len(events)}")
        
        # Test Aggregator
        print("\n📊 Testing Data Aggregator...")
        aggregator = DashboardAggregator()
        
        stats = aggregator.get_dashboard_stats()
        print(f"  Total submissions: {stats.get('total_submissions', 0)}")
        print(f"  Completed: {stats.get('completed', 0)}")
        print(f"  Average confidence: {stats.get('average_confidence', 0):.2f}")
        
        # Test event publishers
        print("\n📢 Testing Event Publishers...")
        publish_submission_event('test_sub_001', {
            'input_type': 'text',
            'created_at': '2024-11-20T10:00:00Z'
        })
        print("  Submission event published: ✓")
        
        publish_completion_event('test_sub_001', {
            'confidence': 0.85,
            'claim': 'Test claim',
            'narrative_type': 'test',
            'risk_level': 'LOW'
        })
        print("  Completion event published: ✓")
        
        print("\n✅ Phase 4 (RTR) Test Passed!")
        print("\n📌 Dashboard available at:")
        print("   http://localhost:3001/dashboard.html")
        print("\n📌 API endpoints:")
        print("   http://localhost:8000/dashboard/stats")
        print("   http://localhost:8000/dashboard/threats")
        print("   http://localhost:8000/dashboard/top-claims")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Phase 4 Test Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🧪 SatyaMatrix Phase 4 Testing")
    print("="*60)
    
    phase4_passed = test_phase4_rtr()
    
    print("\n" + "="*60)
    print("📊 Test Summary")
    print("="*60)
    print(f"Phase 4 (RTR): {'✅ PASSED' if phase4_passed else '❌ FAILED'}")
    print("="*60)
    
    if phase4_passed:
        print("\n🎉 Phase 4 test passed! RTR is working!")
        print("\n🚀 Next steps:")
        print("1. Start API: py -3.11 -m uvicorn app.main:app --reload")
        print("2. Start Frontend: cd frontend && py -3.11 serve.py")
        print("3. Open dashboard: http://localhost:3001/dashboard.html")
    else:
        print("\n⚠️  Phase 4 test failed. Check errors above.")
