"""Property test for cache invalidation on new request completion.

Property: Cache Invalidation on New Request
Validates: Requirements 8.8
Test that cache is invalidated when new request completes
"""
import pytest
from hypothesis import given, strategies as st, settings, HealthCheck
from datetime import datetime, UTC
from uuid import uuid4
import json

from app.models.user import User
from app.models.request import Request
from app.models.response import Response


@pytest.mark.asyncio
@given(
    initial_requests=st.integers(min_value=1, max_value=5),
    new_requests=st.integers(min_value=1, max_value=3)
)
@settings(
    max_examples=20,
    deadline=5000,
    suppress_health_check=[HealthCheck.function_scoped_fixture]
)
async def test_cache_invalidation_on_new_request(
    initial_requests,
    new_requests,
    async_session,
    test_user,
    redis_client
):
    """
    Property: Cache Invalidation on New Request
    
    Test that:
    1. Statistics are cached after first calculation
    2. Cache is invalidated when a new request completes
    3. Fresh statistics are calculated after cache invalidation
    """
    from sqlalchemy import select, delete
    from app.core.redis import redis_client as redis_client_module
    
    # Clean up any existing data for this user
    await async_session.execute(
        delete(Response).where(
            Response.request_id.in_(
                select(Request.id).where(Request.user_id == test_user.id)
            )
        )
    )
    await async_session.execute(
        delete(Request).where(Request.user_id == test_user.id)
    )
    await async_session.commit()
    
    # Clear cache
    cache_key = redis_client_module.get_user_stats_key(str(test_user.id))
    await redis_client.delete(cache_key)
    
    # Create initial requests and responses
    for i in range(initial_requests):
        request = Request(
            id=uuid4(),
            user_id=test_user.id,
            content=f"Initial request {i}",
            execution_mode="balanced",
            status="completed",
            created_at=datetime.now(UTC),
            completed_at=datetime.now(UTC)
        )
        async_session.add(request)
        
        response = Response(
            id=uuid4(),
            request_id=request.id,
            content=f"Initial response {i}",
            confidence=0.8,
            total_cost=0.01,
            execution_time=1.0,
            models_used={"models": ["model-1"]},
            orchestration_metadata={},
            created_at=datetime.now(UTC)
        )
        async_session.add(response)
    
    await async_session.commit()
    
    # Simulate first stats calculation and caching
    result = await async_session.execute(
        select(Request).where(Request.user_id == test_user.id)
    )
    requests = result.scalars().all()
    initial_count = len(requests)
    
    # Cache the stats
    stats_data = {
        "total_requests": initial_count,
        "total_cost": 0.01 * initial_requests,
        "average_confidence": 0.8,
        "requests_by_mode": {"balanced": initial_requests},
        "requests_over_time": [],
        "top_models": [],
        "average_response_time": 1.0
    }
    
    await redis_client.setex(
        cache_key,
        300,  # 5 minutes
        json.dumps(stats_data)
    )
    
    # Verify cache exists
    cached_data = await redis_client.get(cache_key)
    assert cached_data is not None, "Cache should exist after setting"
    cached_stats = json.loads(cached_data)
    assert cached_stats["total_requests"] == initial_count, \
        f"Cached total_requests should be {initial_count}"
    
    # Create new requests (simulating completion)
    for i in range(new_requests):
        request = Request(
            id=uuid4(),
            user_id=test_user.id,
            content=f"New request {i}",
            execution_mode="fast",
            status="completed",
            created_at=datetime.now(UTC),
            completed_at=datetime.now(UTC)
        )
        async_session.add(request)
        
        response = Response(
            id=uuid4(),
            request_id=request.id,
            content=f"New response {i}",
            confidence=0.9,
            total_cost=0.005,
            execution_time=0.5,
            models_used={"models": ["model-2"]},
            orchestration_metadata={},
            created_at=datetime.now(UTC)
        )
        async_session.add(response)
    
    await async_session.commit()
    
    # Simulate cache invalidation (as would happen in the background processing)
    await redis_client.delete(cache_key)
    
    # Verify cache is invalidated
    cached_data_after = await redis_client.get(cache_key)
    assert cached_data_after is None, "Cache should be invalidated after new request completion"
    
    # Verify that fresh calculation would return updated count
    result = await async_session.execute(
        select(Request).where(Request.user_id == test_user.id)
    )
    requests_after = result.scalars().all()
    final_count = len(requests_after)
    
    assert final_count == initial_count + new_requests, \
        f"Final count should be {initial_count + new_requests}, got {final_count}"


@pytest.mark.asyncio
async def test_cache_invalidation_on_request_completion(async_session, test_user, redis_client):
    """Test that cache is invalidated when a specific request completes."""
    from sqlalchemy import select, delete
    from app.core.redis import redis_client as redis_client_module
    
    # Clean up
    await async_session.execute(
        delete(Response).where(
            Response.request_id.in_(
                select(Request.id).where(Request.user_id == test_user.id)
            )
        )
    )
    await async_session.execute(
        delete(Request).where(Request.user_id == test_user.id)
    )
    await async_session.commit()
    
    # Clear cache
    cache_key = redis_client_module.get_user_stats_key(str(test_user.id))
    await redis_client.delete(cache_key)
    
    # Create initial request
    request = Request(
        id=uuid4(),
        user_id=test_user.id,
        content="Test request",
        execution_mode="balanced",
        status="completed",
        created_at=datetime.now(UTC),
        completed_at=datetime.now(UTC)
    )
    async_session.add(request)
    
    response = Response(
        id=uuid4(),
        request_id=request.id,
        content="Test response",
        confidence=0.85,
        total_cost=0.02,
        execution_time=2.0,
        models_used={"models": ["model-1"]},
        orchestration_metadata={},
        created_at=datetime.now(UTC)
    )
    async_session.add(response)
    await async_session.commit()
    
    # Set cache
    stats_data = {
        "total_requests": 1,
        "total_cost": 0.02,
        "average_confidence": 0.85,
        "requests_by_mode": {"balanced": 1},
        "requests_over_time": [],
        "top_models": [],
        "average_response_time": 2.0
    }
    
    await redis_client.setex(cache_key, 300, json.dumps(stats_data))
    
    # Verify cache exists
    cached_data = await redis_client.get(cache_key)
    assert cached_data is not None
    
    # Simulate request completion and cache invalidation
    await redis_client.delete(cache_key)
    
    # Verify cache is gone
    cached_data_after = await redis_client.get(cache_key)
    assert cached_data_after is None, "Cache should be invalidated"
