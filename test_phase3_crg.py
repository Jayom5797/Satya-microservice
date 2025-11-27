"""
Test Phase 3: CRG (Community Reliability Graph)
"""

def test_phase3_crg():
    """Test Phase 3: CRG"""
    print("\n" + "="*60)
    print("🕸️ Testing Phase 3: CRG (Community Reliability Graph)")
    print("="*60)
    
    try:
        from app.agents.crg import run_crg_agent
        
        evidence_list = [
            {
                'source_url': 'https://www.factcheck.org/2020/12/covid-vaccines-safe',
                'title': 'COVID Vaccines Are Safe',
                'reliability_score': 0.98,
                'retrieved_at': '2024-11-20T10:00:00Z'
            },
            {
                'source_url': 'https://www.reuters.com/article/fact-check-vaccines',
                'title': 'No Microchips in Vaccines',
                'reliability_score': 0.95,
                'retrieved_at': '2024-11-20T10:05:00Z'
            },
            {
                'source_url': 'https://www.bbc.com/news/health-vaccines',
                'title': 'Vaccine Safety Confirmed',
                'reliability_score': 0.90,
                'retrieved_at': '2024-11-20T10:10:00Z'
            }
        ]
        
        result = run_crg_agent(evidence_list)
        
        print(f"\n📊 Trust Analysis:")
        print(f"  Average Trust: {result['average_trust']:.3f}")
        print(f"  Trust Weight: {result['trust_weight']:.3f}")
        
        print(f"\n🔗 Trust Scores:")
        for url, score in list(result['trust_scores'].items())[:3]:
            domain = url.split('/')[2] if '/' in url else url
            print(f"  {domain}: {score:.3f}")
        
        print(f"\n📈 Network Stats:")
        stats = result['network_stats']
        print(f"  Total Sources: {stats.get('total_sources', 0)}")
        print(f"  Total Citations: {stats.get('total_citations', 0)}")
        print(f"  Avg Reliability: {stats.get('average_reliability', 0):.3f}")
        
        if result.get('top_trusted_sources'):
            print(f"\n⭐ Top Trusted Sources:")
            for source in result['top_trusted_sources'][:3]:
                print(f"  {source.get('domain', 'N/A')}: {source.get('trust_score', 0):.3f}")
        
        print("\n✅ Phase 3 (CRG) Test Passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Phase 3 Test Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🧪 SatyaMatrix Phase 3 Testing")
    print("="*60)
    
    phase3_passed = test_phase3_crg()
    
    print("\n" + "="*60)
    print("📊 Test Summary")
    print("="*60)
    print(f"Phase 3 (CRG): {'✅ PASSED' if phase3_passed else '❌ FAILED'}")
    print("="*60)
    
    if phase3_passed:
        print("\n🎉 Phase 3 test passed! CRG is working!")
    else:
        print("\n⚠️  Phase 3 test failed. Check errors above.")
