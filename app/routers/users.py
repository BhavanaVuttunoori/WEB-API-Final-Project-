from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.database import get_db
from app.models import User, Calculation
from app.schemas import (
    UserResponse,
    UserUpdate,
    PasswordChange,
    UserStatistics,
    CalculationResponse,
    Message
)
from app.auth import get_current_user, get_password_hash, verify_password

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Get current user's profile"""
    return current_user


@router.put("/me", response_model=UserResponse)
def update_user_profile(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update current user's profile"""
    # Update username if provided
    if user_update.username is not None:
        # Check if username is already taken
        existing_user = db.query(User).filter(
            User.username == user_update.username,
            User.id != current_user.id
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        current_user.username = user_update.username
    
    # Update email if provided
    if user_update.email is not None:
        # Check if email is already taken
        existing_user = db.query(User).filter(
            User.email == user_update.email,
            User.id != current_user.id
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already taken"
            )
        current_user.email = user_update.email
    
    db.commit()
    db.refresh(current_user)
    return current_user


@router.post("/me/change-password", response_model=Message)
def change_password(
    password_data: PasswordChange,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Change user's password"""
    # Verify current password
    if not verify_password(password_data.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect current password"
        )
    
    # Hash and update new password
    current_user.hashed_password = get_password_hash(password_data.new_password)
    db.commit()
    return {"message": "Password changed successfully"}


@router.get("/me/statistics", response_model=UserStatistics)
def get_user_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get statistics for current user's calculations"""
    # Get all calculations for user
    calculations = db.query(Calculation).filter(
        Calculation.user_id == current_user.id
    ).all()
    
    if not calculations:
        return UserStatistics(
            total_calculations=0,
            calculations_by_operation={},
            average_result=0.0,
            most_used_operation=None,
            recent_calculations=[]
        )
    
    # Calculate statistics
    total_calculations = len(calculations)
    
    # Count calculations by operation
    calculations_by_operation = {}
    for calc in calculations:
        op = calc.operation.value
        calculations_by_operation[op] = calculations_by_operation.get(op, 0) + 1
    
    # Calculate average result
    total_result = sum(calc.result for calc in calculations)
    average_result = total_result / total_calculations if total_calculations > 0 else 0.0
    
    # Find most used operation
    most_used_operation = max(
        calculations_by_operation,
        key=calculations_by_operation.get
    ) if calculations_by_operation else None
    
    # Get recent calculations (last 10)
    recent_calculations = db.query(Calculation).filter(
        Calculation.user_id == current_user.id
    ).order_by(Calculation.created_at.desc()).limit(10).all()
    
    return UserStatistics(
        total_calculations=total_calculations,
        calculations_by_operation=calculations_by_operation,
        average_result=round(average_result, 2),
        most_used_operation=most_used_operation,
        recent_calculations=recent_calculations
    )


@router.delete("/me", response_model=Message)
def delete_user_account(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete current user's account and all associated data"""
    db.delete(current_user)
    db.commit()
    return {"message": "Account deleted successfully"}
