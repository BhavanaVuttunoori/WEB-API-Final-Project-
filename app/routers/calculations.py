from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import User, Calculation, OperationType
from app.schemas import (
    CalculationCreate,
    CalculationUpdate,
    CalculationResponse,
    Message
)
from app.auth import get_current_user

router = APIRouter(prefix="/api/calculations", tags=["Calculations"])


def perform_calculation(operation: OperationType, operand1: float, operand2: float) -> float:
    """Perform the calculation based on operation type"""
    if operation == OperationType.ADD:
        return operand1 + operand2
    elif operation == OperationType.SUBTRACT:
        return operand1 - operand2
    elif operation == OperationType.MULTIPLY:
        return operand1 * operand2
    elif operation == OperationType.DIVIDE:
        if operand2 == 0:
            raise ValueError("Cannot divide by zero")
        return operand1 / operand2
    elif operation == OperationType.POWER:
        return operand1 ** operand2
    elif operation == OperationType.MODULO:
        if operand2 == 0:
            raise ValueError("Cannot perform modulo by zero")
        return operand1 % operand2
    else:
        raise ValueError(f"Unknown operation: {operation}")


# CREATE - Add a new calculation
@router.post("/", response_model=CalculationResponse, status_code=status.HTTP_201_CREATED)
def create_calculation(
    calculation: CalculationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new calculation"""
    try:
        result = perform_calculation(
            calculation.operation,
            calculation.operand1,
            calculation.operand2
        )
        
        db_calculation = Calculation(
            user_id=current_user.id,
            operation=calculation.operation,
            operand1=calculation.operand1,
            operand2=calculation.operand2,
            result=result
        )
        db.add(db_calculation)
        db.commit()
        db.refresh(db_calculation)
        return db_calculation
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# READ - Browse all calculations for current user
@router.get("/", response_model=List[CalculationResponse])
def list_calculations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all calculations for the current user"""
    calculations = db.query(Calculation).filter(
        Calculation.user_id == current_user.id
    ).order_by(Calculation.created_at.desc()).offset(skip).limit(limit).all()
    return calculations


# READ - Get a specific calculation by ID
@router.get("/{calculation_id}", response_model=CalculationResponse)
def get_calculation(
    calculation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific calculation by ID"""
    calculation = db.query(Calculation).filter(
        Calculation.id == calculation_id,
        Calculation.user_id == current_user.id
    ).first()
    
    if not calculation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found"
        )
    return calculation


# UPDATE - Edit a calculation
@router.put("/{calculation_id}", response_model=CalculationResponse)
def update_calculation(
    calculation_id: int,
    calculation_update: CalculationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a calculation"""
    db_calculation = db.query(Calculation).filter(
        Calculation.id == calculation_id,
        Calculation.user_id == current_user.id
    ).first()
    
    if not db_calculation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found"
        )
    
    # Update fields if provided
    if calculation_update.operation is not None:
        db_calculation.operation = calculation_update.operation
    if calculation_update.operand1 is not None:
        db_calculation.operand1 = calculation_update.operand1
    if calculation_update.operand2 is not None:
        db_calculation.operand2 = calculation_update.operand2
    
    # Recalculate result
    try:
        db_calculation.result = perform_calculation(
            db_calculation.operation,
            db_calculation.operand1,
            db_calculation.operand2
        )
        db.commit()
        db.refresh(db_calculation)
        return db_calculation
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# DELETE - Delete a calculation
@router.delete("/{calculation_id}", response_model=Message)
def delete_calculation(
    calculation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a calculation"""
    db_calculation = db.query(Calculation).filter(
        Calculation.id == calculation_id,
        Calculation.user_id == current_user.id
    ).first()
    
    if not db_calculation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found"
        )
    
    db.delete(db_calculation)
    db.commit()
    return {"message": "Calculation deleted successfully"}
