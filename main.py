from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from sif_detector import analyze_report
from database import engine, SessionLocal
from models import Base, SafetyReport


# Create database tables
Base.metadata.create_all(bind=engine)


# Create FastAPI application
app = FastAPI(
    title="OIL SIF Detection API",
    description="AI/NLP API for detecting SIF precursors",
    version="1.0.0"
)


# Request format
class ReportRequest(BaseModel):
    report: str


# Database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Home API
@app.get("/")
def home():
    return {
        "message": "OIL SIF Detection API is running"
    }


# Analyze safety report
@app.post("/analyze")
def analyze(
    data: ReportRequest,
    db: Session = Depends(get_db)
):

    result = analyze_report(data.report)

    new_report = SafetyReport(
        report=data.report,
        sif_potential=result["sif_potential"],
        risk_level=result["risk_level"],
        life_saving_rule=result["life_saving_rule"],
        hazard=result["hazard"],
        barrier_failure=result["barrier_failure"],
        confidence=result["confidence"]
    )

    db.add(new_report)
    db.commit()
    db.refresh(new_report)

    return {
        "success": True,
        "result": result,
        "database_id": new_report.id
    }


# Get all analysis history
@app.get("/reports")
def get_reports(
    db: Session = Depends(get_db)
):

    reports = db.query(SafetyReport).order_by(
        SafetyReport.id.desc()
    ).all()

    return {
        "success": True,
        "count": len(reports),
        "reports": reports
    }


# Get one report by ID
@app.get("/reports/{report_id}")
def get_report(
    report_id: int,
    db: Session = Depends(get_db)
):

    report = db.query(SafetyReport).filter(
        SafetyReport.id == report_id
    ).first()

    # If report does not exist
    if report is None:
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )

    return {
        "success": True,
        "report": report
    }


# Get dashboard statistics
@app.get("/statistics")
def get_statistics(
    db: Session = Depends(get_db)
):

    reports = db.query(SafetyReport).all()

    total_reports = len(reports)

    sif_detected = sum(
        1
        for report in reports
        if report.sif_potential == "YES"
    )

    high_risk = sum(
        1
        for report in reports
        if report.risk_level == "HIGH"
    )

    low_risk = sum(
        1
        for report in reports
        if report.risk_level == "LOW"
    )

    return {
        "success": True,
        "statistics": {
            "total_reports": total_reports,
            "sif_detected": sif_detected,
            "high_risk": high_risk,
            "low_risk": low_risk
        }
    }

    # Delete a report
@app.delete("/reports/{report_id}")
def delete_report(
    report_id: int,
    db: Session = Depends(get_db)
):

    report = db.query(SafetyReport).filter(
        SafetyReport.id == report_id
    ).first()

    if report is None:
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )

    db.delete(report)
    db.commit()

    return {
        "success": True,
        "message": "Report deleted successfully",
        "deleted_id": report_id
    }

    # Backend health check
@app.get("/health")
def health_check(db: Session = Depends(get_db)):

    try:
        db.query(SafetyReport).count()

        return {
            "success": True,
            "status": "healthy",
            "database": "connected",
            "message": "Backend is running successfully"
        }

    except Exception:
        return {
            "success": False,
            "status": "unhealthy",
            "database": "error",
            "message": "Database connection failed"
        }