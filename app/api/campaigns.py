# app/api/campaigns.py

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, and_, desc, asc, or_
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any

from app.core.database import get_db
from app.core.dependencies import get_current_user, get_current_business_user
from app.models.user import User
from app.models.campaign import Campaign
from app.models.post import ScheduledPost
from app.models.analytics import PostAnalytics
from app.schemas.campaign import (
    CampaignCreate,
    CampaignUpdate,
    CampaignResponse,
    CampaignDetailResponse,
    CampaignAnalytics,
    CampaignListResponse,
    CampaignStatusUpdate,
    CampaignPerformanceMetrics
)

router = APIRouter(prefix="/api/campaigns", tags=["Campaigns"])


@router.post("/", response_model=CampaignResponse, status_code=status.HTTP_201_CREATED)
def create_campaign(
    campaign: CampaignCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new campaign
    """
    # Validate dates
    if campaign.start_date >= campaign.end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start date must be before end date"
        )
    
    # Check if campaign with same name exists for this user
    existing = db.query(Campaign).filter(
        Campaign.user_id == current_user.id,
        Campaign.name == campaign.name
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Campaign with this name already exists"
        )
    
    # Create campaign
    db_campaign = Campaign(
        **campaign.dict(),
        user_id=current_user.id,
        status="active"  # Default status
    )
    
    db.add(db_campaign)
    db.commit()
    db.refresh(db_campaign)
    
    return db_campaign


@router.get("/", response_model=CampaignListResponse)
def get_campaigns(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[str] = Query(None, description="Filter by status"),
    platform: Optional[str] = Query(None, description="Filter by platform"),
    search: Optional[str] = Query(None, description="Search by name or description"),
    sort_by: Optional[str] = Query("created_at", description="Sort by: created_at, start_date, end_date, name"),
    sort_order: Optional[str] = Query("desc", description="Sort order: asc or desc")
):
    """
    Get all campaigns for the current user with filters
    """
    # Build query
    query = db.query(Campaign).filter(Campaign.user_id == current_user.id)
    
    # Apply filters
    if status:
        query = query.filter(Campaign.status == status)
    
    if platform:
        query = query.filter(Campaign.platform == platform)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Campaign.name.ilike(search_term),
                Campaign.description.ilike(search_term)
            )
        )
    
    # Apply sorting
    sort_column = getattr(Campaign, sort_by, Campaign.created_at)
    if sort_order == "asc":
        query = query.order_by(asc(sort_column))
    else:
        query = query.order_by(desc(sort_column))
    
    # Get total count
    total = query.count()
    
    # Get paginated results
    campaigns = query.offset(skip).limit(limit).all()
    
    # Get additional metrics for each campaign
    results = []
    for campaign in campaigns:
        # Count posts
        posts = db.query(ScheduledPost).filter(
            ScheduledPost.campaign_id == campaign.id
        ).all()
        
        published_posts = len([p for p in posts if p.status == "published"])
        scheduled_posts = len([p for p in posts if p.status == "scheduled"])
        
        # Get analytics
        analytics = db.query(PostAnalytics).filter(
            PostAnalytics.campaign_id == campaign.id
        ).all()
        
        likes = sum([a.likes for a in analytics])
        shares = sum([a.shares for a in analytics])
        comments = sum([a.comments for a in analytics])
        views = sum([a.views for a in analytics])
        total_engagement = likes + shares + comments
        
        results.append(CampaignResponse(
            id=campaign.id,
            name=campaign.name,
            description=campaign.description,
            platform=campaign.platform,
            start_date=campaign.start_date,
            end_date=campaign.end_date,
            status=campaign.status,
            created_at=campaign.created_at,
            user_id=campaign.user_id,
            total_posts=len(posts),
            published_posts=published_posts,
            scheduled_posts=scheduled_posts,
            likes=likes,
            shares=shares,
            comments=comments,
            views=views,
            total_engagement=total_engagement,
            engagement_rate=(total_engagement / views * 100) if views > 0 else 0
        ))
    
    return CampaignListResponse(
        total=total,
        skip=skip,
        limit=limit,
        campaigns=results
    )


@router.get("/{campaign_id}", response_model=CampaignDetailResponse)
def get_campaign(
    campaign_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get detailed campaign information
    """
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.user_id == current_user.id
    ).first()
    
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    # Get posts for this campaign
    posts = db.query(ScheduledPost).filter(
        ScheduledPost.campaign_id == campaign_id
    ).all()
    
    # Get analytics
    analytics = db.query(PostAnalytics).filter(
        PostAnalytics.campaign_id == campaign_id
    ).all()
    
    # Calculate metrics
    published_posts = [p for p in posts if p.status == "published"]
    scheduled_posts = [p for p in posts if p.status == "scheduled"]
    failed_posts = [p for p in posts if p.status == "failed"]
    draft_posts = [p for p in posts if p.status == "draft"]
    
    likes = sum([a.likes for a in analytics])
    shares = sum([a.shares for a in analytics])
    comments = sum([a.comments for a in analytics])
    views = sum([a.views for a in analytics])
    total_engagement = likes + shares + comments
    
    # Get engagement over time
    engagement_over_time = []
    if analytics:
        # Group by date
        date_groups = {}
        for a in analytics:
            date_key = a.recorded_at.strftime("%Y-%m-%d")
            if date_key not in date_groups:
                date_groups[date_key] = {"likes": 0, "shares": 0, "comments": 0, "views": 0}
            date_groups[date_key]["likes"] += a.likes
            date_groups[date_key]["shares"] += a.shares
            date_groups[date_key]["comments"] += a.comments
            date_groups[date_key]["views"] += a.views
        
        for date_key, metrics in date_groups.items():
            engagement = metrics["likes"] + metrics["shares"] + metrics["comments"]
            engagement_over_time.append({
                "date": date_key,
                "likes": metrics["likes"],
                "shares": metrics["shares"],
                "comments": metrics["comments"],
                "views": metrics["views"],
                "engagement": engagement
            })
    
    # Get post performance
    post_performance = []
    for post in posts:
        post_analytics = db.query(PostAnalytics).filter(
            PostAnalytics.post_id == post.id
        ).order_by(desc(PostAnalytics.recorded_at)).first()
        
        if post_analytics:
            post_performance.append({
                "post_id": post.id,
                "title": post.title,
                "platform": post.platform,
                "status": post.status,
                "scheduled_time": post.scheduled_time,
                "published_at": post.published_at,
                "likes": post_analytics.likes,
                "shares": post_analytics.shares,
                "comments": post_analytics.comments,
                "views": post_analytics.views,
                "engagement": post_analytics.likes + post_analytics.shares + post_analytics.comments
            })
    
    return CampaignDetailResponse(
        id=campaign.id,
        name=campaign.name,
        description=campaign.description,
        platform=campaign.platform,
        start_date=campaign.start_date,
        end_date=campaign.end_date,
        status=campaign.status,
        created_at=campaign.created_at,
        user_id=campaign.user_id,
        total_posts=len(posts),
        published_posts=len(published_posts),
        scheduled_posts=len(scheduled_posts),
        failed_posts=len(failed_posts),
        draft_posts=len(draft_posts),
        likes=likes,
        shares=shares,
        comments=comments,
        views=views,
        total_engagement=total_engagement,
        engagement_rate=(total_engagement / views * 100) if views > 0 else 0,
        engagement_over_time=engagement_over_time,
        post_performance=post_performance,
        progress=(len(published_posts) / len(posts) * 100) if posts else 0
    )


@router.put("/{campaign_id}", response_model=CampaignResponse)
def update_campaign(
    campaign_id: int,
    campaign_update: CampaignUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update campaign details
    """
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.user_id == current_user.id
    ).first()
    
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    # Validate dates if both are provided
    if campaign_update.start_date and campaign_update.end_date:
        if campaign_update.start_date >= campaign_update.end_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Start date must be before end date"
            )
    elif campaign_update.start_date and campaign.end_date:
        if campaign_update.start_date >= campaign.end_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Start date must be before end date"
            )
    elif campaign_update.end_date and campaign.start_date:
        if campaign.start_date >= campaign_update.end_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Start date must be before end date"
            )
    
    # Update fields
    update_data = campaign_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(campaign, field, value)
    
    db.commit()
    db.refresh(campaign)
    
    return campaign


@router.patch("/{campaign_id}/status", response_model=CampaignResponse)
def update_campaign_status(
    campaign_id: int,
    status_update: CampaignStatusUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update campaign status
    """
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.user_id == current_user.id
    ).first()
    
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    # Validate status transition
    valid_statuses = ["draft", "active", "paused", "completed", "cancelled"]
    if status_update.status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
        )
    
    campaign.status = status_update.status
    db.commit()
    db.refresh(campaign)
    
    return campaign


@router.delete("/{campaign_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_campaign(
    campaign_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    force: bool = Query(False, description="Force delete even if posts exist")
):
    """
    Delete a campaign
    """
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.user_id == current_user.id
    ).first()
    
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    # Check if campaign has posts
    posts = db.query(ScheduledPost).filter(
        ScheduledPost.campaign_id == campaign_id
    ).count()
    
    if posts > 0 and not force:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Campaign has {posts} posts. Use force=true to delete anyway"
        )
    
    # Delete campaign (cascade will handle related data)
    db.delete(campaign)
    db.commit()
    
    return None


@router.get("/{campaign_id}/analytics", response_model=CampaignAnalytics)
def get_campaign_analytics(
    campaign_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    days: Optional[int] = Query(30, ge=1, le=365)
):
    """
    Get detailed analytics for a specific campaign
    """
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.user_id == current_user.id
    ).first()
    
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # Get posts
    posts = db.query(ScheduledPost).filter(
        ScheduledPost.campaign_id == campaign_id,
        ScheduledPost.created_at >= start_date
    ).all()
    
    # Get analytics
    analytics = db.query(PostAnalytics).filter(
        PostAnalytics.campaign_id == campaign_id,
        PostAnalytics.recorded_at >= start_date
    ).order_by(desc(PostAnalytics.recorded_at)).all()
    
    # Calculate metrics
    total_posts = len(posts)
    published_posts = len([p for p in posts if p.status == "published"])
    scheduled_posts = len([p for p in posts if p.status == "scheduled"])
    failed_posts = len([p for p in posts if p.status == "failed"])
    draft_posts = len([p for p in posts if p.status == "draft"])
    
    likes = sum([a.likes for a in analytics])
    shares = sum([a.shares for a in analytics])
    comments = sum([a.comments for a in analytics])
    views = sum([a.views for a in analytics])
    total_engagement = likes + shares + comments
    
    engagement_rate = (total_engagement / views * 100) if views > 0 else 0
    
    # Daily performance
    daily_performance = []
    date_groups = {}
    for a in analytics:
        date_key = a.recorded_at.strftime("%Y-%m-%d")
        if date_key not in date_groups:
            date_groups[date_key] = {
                "date": date_key,
                "likes": 0,
                "shares": 0,
                "comments": 0,
                "views": 0
            }
        date_groups[date_key]["likes"] += a.likes
        date_groups[date_key]["shares"] += a.shares
        date_groups[date_key]["comments"] += a.comments
        date_groups[date_key]["views"] += a.views
    
    for date_key, metrics in date_groups.items():
        engagement = metrics["likes"] + metrics["shares"] + metrics["comments"]
        daily_performance.append({
            "date": date_key,
            "likes": metrics["likes"],
            "shares": metrics["shares"],
            "comments": metrics["comments"],
            "views": metrics["views"],
            "engagement": engagement,
            "engagement_rate": (engagement / metrics["views"] * 100) if metrics["views"] > 0 else 0
        })
    
    # Platform breakdown
    platform_stats = {}
    for post in posts:
        if post.platform not in platform_stats:
            platform_stats[post.platform] = {
                "platform": post.platform,
                "total_posts": 0,
                "published_posts": 0,
                "likes": 0,
                "shares": 0,
                "comments": 0,
                "views": 0,
                "engagement": 0
            }
        
        platform_stats[post.platform]["total_posts"] += 1
        if post.status == "published":
            platform_stats[post.platform]["published_posts"] += 1
    
    # Add analytics to platform stats
    post_ids = [p.id for p in posts]
    platform_analytics = db.query(PostAnalytics).filter(
        PostAnalytics.post_id.in_(post_ids) if post_ids else False,
        PostAnalytics.recorded_at >= start_date
    ).all()
    
    for a in platform_analytics:
        # Find the post's platform
        post = next((p for p in posts if p.id == a.post_id), None)
        if post and post.platform in platform_stats:
            platform_stats[post.platform]["likes"] += a.likes
            platform_stats[post.platform]["shares"] += a.shares
            platform_stats[post.platform]["comments"] += a.comments
            platform_stats[post.platform]["views"] += a.views
            platform_stats[post.platform]["engagement"] += a.likes + a.shares + a.comments
    
    return CampaignAnalytics(
        campaign_id=campaign_id,
        campaign_name=campaign.name,
        platform=campaign.platform,
        start_date=campaign.start_date,
        end_date=campaign.end_date,
        status=campaign.status,
        total_posts=total_posts,
        published_posts=published_posts,
        scheduled_posts=scheduled_posts,
        failed_posts=failed_posts,
        draft_posts=draft_posts,
        likes=likes,
        shares=shares,
        comments=comments,
        views=views,
        total_engagement=total_engagement,
        engagement_rate=engagement_rate,
        daily_performance=daily_performance,
        platform_breakdown=list(platform_stats.values()),
        period_days=days
    )


@router.get("/{campaign_id}/posts")
def get_campaign_posts(
    campaign_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    status: Optional[str] = Query(None, description="Filter by post status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100)
):
    """
    Get all posts for a specific campaign
    """
    # Verify campaign belongs to current user
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.user_id == current_user.id
    ).first()
    
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    # Get posts
    query = db.query(ScheduledPost).filter(
        ScheduledPost.campaign_id == campaign_id
    )
    
    if status:
        query = query.filter(ScheduledPost.status == status)
    
    total = query.count()
    posts = query.offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "posts": [
            {
                "id": post.id,
                "title": post.title,
                "platform": post.platform,
                "status": post.status,
                "scheduled_time": post.scheduled_time,
                "published_at": post.published_at,
                "created_at": post.created_at
            }
            for post in posts
        ]
    }


@router.get("/analytics/overview")
def get_all_campaigns_analytics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    days: Optional[int] = Query(30, ge=1, le=365)
):
    """
    Get overview analytics for all campaigns
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    campaigns = db.query(Campaign).filter(
        Campaign.user_id == current_user.id,
        Campaign.created_at >= start_date
    ).all()
    
    results = []
    for campaign in campaigns:
        # Get posts count
        posts = db.query(ScheduledPost).filter(
            ScheduledPost.campaign_id == campaign.id
        ).count()
        
        # Get analytics
        analytics = db.query(PostAnalytics).filter(
            PostAnalytics.campaign_id == campaign.id,
            PostAnalytics.recorded_at >= start_date
        ).all()
        
        if analytics:
            likes = sum([a.likes for a in analytics])
            shares = sum([a.shares for a in analytics])
            comments = sum([a.comments for a in analytics])
            views = sum([a.views for a in analytics])
            engagement = likes + shares + comments
            engagement_rate = (engagement / views * 100) if views > 0 else 0
        else:
            likes = shares = comments = views = engagement = engagement_rate = 0
        
        results.append({
            "campaign_id": campaign.id,
            "campaign_name": campaign.name,
            "platform": campaign.platform,
            "status": campaign.status,
            "total_posts": posts,
            "likes": likes,
            "shares": shares,
            "comments": comments,
            "views": views,
            "engagement": engagement,
            "engagement_rate": engagement_rate
        })
    
    # Sort by engagement
    results.sort(key=lambda x: x["engagement"], reverse=True)
    
    return {
        "total_campaigns": len(results),
        "active_campaigns": len([c for c in results if c["status"] == "active"]),
        "completed_campaigns": len([c for c in results if c["status"] == "completed"]),
        "campaigns": results,
        "period_days": days
    }


@router.get("/stats/performance", response_model=CampaignPerformanceMetrics)
def get_campaign_performance_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    days: Optional[int] = Query(30, ge=1, le=365)
):
    """
    Get overall campaign performance statistics
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # Get all campaigns for the user
    campaigns = db.query(Campaign).filter(
        Campaign.user_id == current_user.id,
        Campaign.created_at >= start_date
    ).all()
    
    total_campaigns = len(campaigns)
    active_campaigns = len([c for c in campaigns if c.status == "active"])
    completed_campaigns = len([c for c in campaigns if c.status == "completed"])
    paused_campaigns = len([c for c in campaigns if c.status == "paused"])
    cancelled_campaigns = len([c for c in campaigns if c.status == "cancelled"])
    
    # Calculate average engagement across all campaigns
    all_analytics = []
    for campaign in campaigns:
        analytics = db.query(PostAnalytics).filter(
            PostAnalytics.campaign_id == campaign.id,
            PostAnalytics.recorded_at >= start_date
        ).all()
        all_analytics.extend(analytics)
    
    total_likes = sum([a.likes for a in all_analytics])
    total_shares = sum([a.shares for a in all_analytics])
    total_comments = sum([a.comments for a in all_analytics])
    total_views = sum([a.views for a in all_analytics])
    total_engagement = total_likes + total_shares + total_comments
    
    # Get best performing campaign
    best_campaign = None
    best_engagement = 0
    
    for campaign in campaigns:
        analytics = db.query(PostAnalytics).filter(
            PostAnalytics.campaign_id == campaign.id,
            PostAnalytics.recorded_at >= start_date
        ).all()
        
        engagement = sum([a.likes + a.shares + a.comments for a in analytics])
        if engagement > best_engagement:
            best_engagement = engagement
            best_campaign = {
                "campaign_id": campaign.id,
                "name": campaign.name,
                "engagement": engagement,
                "likes": sum([a.likes for a in analytics]),
                "shares": sum([a.shares for a in analytics]),
                "comments": sum([a.comments for a in analytics]),
                "views": sum([a.views for a in analytics])
            }
    
    return CampaignPerformanceMetrics(
        total_campaigns=total_campaigns,
        active_campaigns=active_campaigns,
        completed_campaigns=completed_campaigns,
        paused_campaigns=paused_campaigns,
        cancelled_campaigns=cancelled_campaigns,
        total_likes=total_likes,
        total_shares=total_shares,
        total_comments=total_comments,
        total_views=total_views,
        total_engagement=total_engagement,
        average_engagement_per_campaign=total_engagement / total_campaigns if total_campaigns > 0 else 0,
        best_performing_campaign=best_campaign,
        period_days=days
    )