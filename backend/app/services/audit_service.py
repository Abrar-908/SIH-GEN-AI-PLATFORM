from sqlalchemy.orm import Session
from app.models.models import AuditLog

class AuditService:
    @staticmethod
    def log(db: Session, action: str, source: str = None, details: str = None, status: str = "Success", user_name: str = "Analyst", user_role: str = "Analyst"):
        try:
            entry = AuditLog(
                user_name=user_name,
                user_role=user_role,
                action=action,
                source=source,
                details=details,
                status=status
            )
            db.add(entry)
            db.commit()
            return entry
        except Exception as e:
            db.rollback()
            return None
