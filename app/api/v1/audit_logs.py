from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.db.models import AuditLog
from app.schemas.audit_log import AuditLogCreate, AuditLogRead

router = APIRouter()


@router.post("", response_model=AuditLogRead, status_code=201)
def create_audit_log(payload: AuditLogCreate, db: Session = Depends(get_db)):
    audit_log = AuditLog(
        action=payload.action,
        table_name=payload.table_name,
        record_id=payload.record_id,
        user_id=payload.user_id,
        payload=payload.payload,
    )
    db.add(audit_log)
    db.commit()
    db.refresh(audit_log)
    return audit_log


@router.get("", response_model=list[AuditLogRead])
def list_audit_logs(db: Session = Depends(get_db)):
    return db.query(AuditLog).order_by(AuditLog.created_at.desc()).all()


@router.get("/{audit_log_id}", response_model=AuditLogRead)
def get_audit_log(audit_log_id: int, db: Session = Depends(get_db)):
    audit_log = db.query(AuditLog).filter(AuditLog.id == audit_log_id).first()
    if not audit_log:
        raise HTTPException(status_code=404, detail="Audit log not found")
    return audit_log


# Pas de PUT/DELETE pour AuditLog - les logs d'audit ne doivent pas être modifiés !
