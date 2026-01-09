"""
Debug script to test semantic evolution function directly
"""
import asyncio
from datetime import date
from backend.app.services.semantic_evolution_service import compute_semantic_evolution


async def main():
    print("Testing semantic evolution...")
    
    try:
        result = await compute_semantic_evolution(
            concept="seguridad publica",
            granularity="month",
            start_date=date(2025, 1, 31),
            end_date=date(2025, 12, 5),
            similarity_threshold=0.6
        )
        
        print("\n✅ Success!")
        print(f"\nConcept: {result['concept']}")
        print(f"Granularity: {result['granularity']}")
        print(f"Number of evolution points: {len(result['points'])}")
        print(f"Number of drift points: {len(result['drift'])}")
        
        if result['points']:
            print("\nFirst few evolution points:")
            for point in result['points'][:3]:
                print(f"  {point}")
        
        if result['drift']:
            print("\nFirst few drift points:")
            for drift in result['drift'][:3]:
                print(f"  {drift}")
        
        if result['max_drift']:
            print(f"\nMax drift: {result['max_drift']}")
    
    except Exception as e:
        print(f"\n❌ Error: {type(e).__name__}")
        print(f"Message: {str(e)}")
        import traceback
        print("\nFull traceback:")
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
