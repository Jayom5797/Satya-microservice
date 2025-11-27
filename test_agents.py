"""
Test all Phase 2 agents
"""

from app.agents.classify import classify_agent
from app.agents.extract import extraction_agent
from app.agents.format import format_agent
from datetime import datetime

print("=" * 60)
print("🧪 Testing Phase 2 Agents")
print("=" * 60)
print()

# Test Agent 1: Classify
print("🔍 Agent 1: Classify")
print("-" * 60)
result = classify_agent.run({
    'input_type': 'text',
    'input_ref': 'Government will provide free electricity next month'
})
print(f"✓ Input type: {result['input_type']}")
print(f"✓ Metadata: {result['metadata']}")
print()

# Test Agent 2: Extract
print("🔍 Agent 2: Extract Claim")
print("-" * 60)
result = extraction_agent.run('text', 'Government will provide free electricity next month. This was announced by the Prime Minister yesterday.')
print(f"✓ Success: {result['success']}")
print(f"✓ Claim: {result['claim_text']}")
print(f"✓ Extracted from: {result['extracted_from']}")
print()

# Test Agent 3: Format
print("🔍 Agent 3: Format & Normalize")
print("-" * 60)
result = format_agent.run(
    'Government will provide free electricity next month',
    reference_date=datetime(2025, 11, 20)
)
print(f"✓ Normalized: {result['normalized_claim']}")
print(f"✓ Entities: {result['entities']}")
print(f"✓ Entity types: {result['entity_types']}")
print(f"✓ Has spaCy: {result['metadata']['has_spacy']}")
print()

print("=" * 60)
print("✅ All agents working!")
print("=" * 60)
