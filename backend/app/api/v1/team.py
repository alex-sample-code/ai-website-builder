"""
Team management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import UUID, uuid4
from datetime import datetime, timedelta
from app.database import get_db
from app.models.user import User
from app.models.team_invitation import TeamInvitation
from app.models.audit_log import AuditLog
from app.models.tenant import Tenant
from app.schemas.team import (
    TeamMemberResponse, TeamInviteRequest, TeamInviteResponse,
    TeamMemberRoleUpdate, AuditLogResponse
)
from app.auth.deps import get_current_user, get_current_tenant
import logging
import os
import boto3

logger = logging.getLogger(__name__)
router = APIRouter()

# SES client for sending invitation emails
ses_client = boto3.client('ses', region_name=os.getenv("AWS_REGION", "us-east-1"))
SENDER_EMAIL = os.getenv("SES_SENDER_EMAIL", "noreply@chinabjalex.com")


@router.get("/members", response_model=List[TeamMemberResponse])
async def list_team_members(
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all team members for the current tenant.
    """
    result = await db.execute(
        select(User).where(User.tenant_id == tenant.id).order_by(User.created_at)
    )
    members = result.scalars().all()
    return members


@router.post("/invite", response_model=TeamInviteResponse, status_code=status.HTTP_201_CREATED)
async def invite_team_member(
    invite_request: TeamInviteRequest,
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Invite a new team member via email.
    """
    # Only owners can invite
    if user.role != "owner":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only owners can invite team members"
        )

    # Check if user already exists
    existing_user = await db.execute(
        select(User).where(User.email == invite_request.email, User.tenant_id == tenant.id)
    )
    if existing_user.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists in this tenant"
        )

    # Check for existing pending invitation
    existing_invite = await db.execute(
        select(TeamInvitation).where(
            TeamInvitation.email == invite_request.email,
            TeamInvitation.tenant_id == tenant.id,
            TeamInvitation.status == "pending"
        )
    )
    if existing_invite.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invitation already sent to this email"
        )

    # Create invitation
    token = str(uuid4())
    expires_at = datetime.utcnow() + timedelta(days=7)

    invitation = TeamInvitation(
        tenant_id=tenant.id,
        email=invite_request.email,
        role=invite_request.role,
        token=token,
        status="pending",
        invited_by=user.id,
        expires_at=expires_at
    )

    db.add(invitation)
    await db.commit()
    await db.refresh(invitation)

    # Send invitation email via SES
    try:
        invitation_url = f"https://chinabjalex.com/invite/{token}"
        ses_client.send_email(
            Source=SENDER_EMAIL,
            Destination={'ToAddresses': [invite_request.email]},
            Message={
                'Subject': {'Data': f"You've been invited to join {tenant.name}"},
                'Body': {
                    'Html': {
                        'Data': f"""
                        <html>
                        <body>
                            <h2>Team Invitation</h2>
                            <p>{user.name or user.email} has invited you to join {tenant.name} as a {invite_request.role}.</p>
                            <p><a href="{invitation_url}">Click here to accept the invitation</a></p>
                            <p>This invitation expires in 7 days.</p>
                        </body>
                        </html>
                        """
                    }
                }
            }
        )
    except Exception as e:
        logger.error(f"Failed to send invitation email: {str(e)}")
        # Don't fail the request if email fails, invitation is still created

    # Log action
    audit_log = AuditLog(
        tenant_id=tenant.id,
        user_id=user.id,
        action="team.invite",
        resource_type="invitation",
        resource_id=invitation.id,
        details={"email": invite_request.email, "role": invite_request.role}
    )
    db.add(audit_log)
    await db.commit()

    logger.info(f"Team invitation sent: {invitation.id} by user {user.id}")

    return TeamInviteResponse(
        invitation_id=invitation.id,
        email=invitation.email,
        role=invitation.role,
        status=invitation.status,
        expires_at=invitation.expires_at
    )


@router.delete("/members/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_team_member(
    member_id: UUID,
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Remove a team member.
    """
    # Only owners can remove members
    if user.role != "owner":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only owners can remove team members"
        )

    # Cannot remove yourself
    if member_id == user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot remove yourself"
        )

    # Get member
    result = await db.execute(
        select(User).where(User.id == member_id, User.tenant_id == tenant.id)
    )
    member = result.scalar_one_or_none()

    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")

    # Delete member
    await db.delete(member)

    # Log action
    audit_log = AuditLog(
        tenant_id=tenant.id,
        user_id=user.id,
        action="team.remove",
        resource_type="user",
        resource_id=member_id,
        details={"email": member.email}
    )
    db.add(audit_log)

    await db.commit()

    logger.info(f"Team member removed: {member_id} by user {user.id}")
    return None


@router.put("/members/{member_id}/role", response_model=TeamMemberResponse)
async def change_member_role(
    member_id: UUID,
    role_update: TeamMemberRoleUpdate,
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Change a team member's role.
    """
    # Only owners can change roles
    if user.role != "owner":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only owners can change member roles"
        )

    # Cannot change your own role
    if member_id == user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot change your own role"
        )

    # Get member
    result = await db.execute(
        select(User).where(User.id == member_id, User.tenant_id == tenant.id)
    )
    member = result.scalar_one_or_none()

    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")

    old_role = member.role
    member.role = role_update.role

    # Log action
    audit_log = AuditLog(
        tenant_id=tenant.id,
        user_id=user.id,
        action="team.role_change",
        resource_type="user",
        resource_id=member_id,
        details={"email": member.email, "old_role": old_role, "new_role": role_update.role}
    )
    db.add(audit_log)

    await db.commit()
    await db.refresh(member)

    logger.info(f"Team member role changed: {member_id} from {old_role} to {role_update.role} by user {user.id}")
    return member


@router.get("/audit-logs", response_model=List[AuditLogResponse])
async def list_audit_logs(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Get audit logs for the tenant.
    """
    # Build query
    query = select(AuditLog).where(AuditLog.tenant_id == tenant.id)
    query = query.order_by(AuditLog.created_at.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)

    result = await db.execute(query)
    logs = result.scalars().all()
    return logs
