"""
Test SatyaMatrix Phases 1 & 2
"""

from datetime import datetime

def test_phase1_cmte():
    """Test Phase 1: CMTE"""
    print("\n" + "="*60)
    print("🔄 Testing Phase 1: CMTE (Claim Mutation Tracking)")
    print("="*60)
    
    try:
        from app.agents.cmte import run_cmte_agent
        
        claim_id = "test_claim_001"
        claim_text = "COVID vaccines contain tracking microchips"
        claim_data = {
            'timestamp': datetime.now().isoformat(),
            'source_url': 'https://example.com/post',
            'platform': 'twitter'
        }
        
        result = run_cmte_agent(claim_id, claim_text, claim_data)
        
        print(f"\n✓ Claim ID: {result['claim_id']}")
        print(f"✓ Similar Claims: {result['similar_claims_count']}")
        print(f"✓ Family Size: {len(result['mutation_family'])}")
        print(f"✓ Viral Score: {result.get('viral_score', 0)}/100")
        print(f"✓ Index Size: {result.get('index_size', 0)} claims")
        
        if result.get('patient_zero'):
            print(f"\n📍 Patient Zero:")
            print(f"  Text: {result['patient_zero'].get('text', 'N/A')}")
        
        if result.get('spread_prediction'):
            pred = result['spread_prediction']
            print(f"\n🔮 Spread Prediction:")
            print(f"  Current: {pred.get('current_count', 0)}")
            print(f"  Predicted (7 days): {pred.get('predicted_count', 0)}")
        
        print("\n✅ Phase 1 (CMTE) Test Passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Phase 1 Test Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_phase2_nri():
    """Test Phase 2: NRI"""
    print("\n" + "="*60)
    print("🧠 Testing Phase 2: NRI (Narrative Reasoning)")
    print("="*60)
    
    try:
        from app.agents.nri import run_nri_agent
        
        claim_text = "COVID vaccines contain tracking microchips"
        fact_check_result = {
            'explanation': 'This claim is false. No vaccines contain microchips.',
            'confidence': 0.95
        }
        
        result = run_nri_agent(claim_text, fact_check_result)
        
        # Narrative Analysis
        narrative = result['narrative_analysis']
        print(f"\n📊 Narrative Analysis:")
        print(f"  Type: {narrative.get('narrative_type')}")
        print(f"  Confidence: {narrative.get('confidence', 0):.2f}")
        print(f"  Emotional Triggers: {', '.join(narrative.get('emotional_triggers', []))}")
        print(f"  Target Audience: {narrative.get('target_audience')}")
        
        # Corrective Messaging
        messaging = result['corrective_messaging']
        print(f"\n📱 Corrective Messages:")
        print(f"  Short: {messaging.get('short_message', 'N/A')[:80]}...")
        print(f"  Style: {messaging.get('communication_style', 'N/A')}")
        
        # Risk Assessment
        risk = result['risk_assessment']
        print(f"\n⚠️  Risk Assessment:")
        print(f"  Level: {risk.get('risk_level')}")
        print(f"  Score: {risk.get('risk_score', 0):.2f}")
        print(f"  Recommendation: {risk.get('recommendation')}")
        
        print("\n✅ Phase 2 (NRI) Test Passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Phase 2 Test Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🧪 SatyaMatrix Phases 1 & 2 Testing")
    print("="*60)
    
    # Test Phase 1
    phase1_passed = test_phase1_cmte()
    
    # Test Phase 2
    phase2_passed = test_phase2_nri()
    
    # Summary
    print("\n" + "="*60)
    print("📊 Test Summary")
    print("="*60)
    print(f"Phase 1 (CMTE): {'✅ PASSED' if phase1_passed else '❌ FAILED'}")
    print(f"Phase 2 (NRI): {'✅ PASSED' if phase2_passed else '❌ FAILED'}")
    print("="*60)
    
    if phase1_passed and phase2_passed:
        print("\n🎉 All tests passed! Phases 1 & 2 are working!")
    else:
        print("\n⚠️  Some tests failed. Check errors above.")
