#!/usr/bin/env python3
"""
Simple test script to verify the Music Catalog API functionality.
"""

import asyncio
import aiohttp
import json

API_BASE_URL = "http://localhost:8000"

async def test_api_endpoints():
    """Test the main API endpoints."""
    
    async with aiohttp.ClientSession() as session:
        print("🎵 Testing Music Catalog API...")
        
        # Test 1: Health check (docs endpoint)
        try:
            async with session.get(f"{API_BASE_URL}/docs") as response:
                if response.status == 200:
                    print("✅ API documentation is accessible")
                else:
                    print(f"❌ API docs failed with status: {response.status}")
        except Exception as e:
            print(f"❌ Failed to connect to API: {e}")
            return
        
        # Test 2: Add a new track
        test_track = {
            "title": "Bohemian Rhapsody",
            "artist": "Queen"
        }
        
        try:
            async with session.post(
                f"{API_BASE_URL}/",
                json=test_track,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    track_data = await response.json()
                    print(f"✅ Successfully added track: {track_data.get('title')} by {track_data.get('artist')}")
                    track_id = track_data.get('id')
                    
                    # Test 3: Retrieve the track
                    if track_id:
                        async with session.get(f"{API_BASE_URL}/{track_id}") as get_response:
                            if get_response.status == 200:
                                retrieved_track = await get_response.json()
                                print(f"✅ Successfully retrieved track with {len(retrieved_track.get('lyrics', []))} lyrics lines")
                            else:
                                print(f"❌ Failed to retrieve track: {get_response.status}")
                    
                elif response.status == 409:
                    print("ℹ️  Track already exists in catalog")
                else:
                    error_data = await response.json()
                    print(f"❌ Failed to add track: {response.status} - {error_data.get('message', 'Unknown error')}")
        except Exception as e:
            print(f"❌ Error testing track operations: {e}")
        
        # Test 4: Search functionality
        search_query = {
            "search_terms": ["Queen", "rock"]
        }
        
        try:
            async with session.post(
                f"{API_BASE_URL}/search",
                json=search_query,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    search_results = await response.json()
                    print(f"✅ Search returned {len(search_results)} results")
                else:
                    print(f"❌ Search failed with status: {response.status}")
        except Exception as e:
            print(f"❌ Error testing search: {e}")

if __name__ == "__main__":
    print("Starting API tests...")
    asyncio.run(test_api_endpoints())
    print("Tests completed!")
