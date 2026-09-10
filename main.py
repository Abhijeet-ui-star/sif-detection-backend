from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import Base, engine, get_db
from models import SafetyReport
from sif_detector import analyze_report


# =========================================================
# DATABASE
# =========================================================

Base.metadata.create_all(bind=engine)


# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title="OIL SIF Detection Backend",
    description="Safety Observation and SIF Precursor Detection API",
    version="1.0.0"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# REQUEST MODEL
# =========================================================

class ReportRequest(BaseModel):
    report: str


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():
    return {
        "message": "OIL SIF Detection Backend is running"
    }


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


# =========================================================
# ANALYZE REPORT
# =========================================================

@app.post("/analyze")
def analyze_safety_report(
    data: ReportRequest,
    db: Session = Depends(get_db)
):

    if not data.report.strip():
        raise HTTPException(
            status_code=400,
            detail="Report cannot be empty"
        )

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
        "id": new_report.id,
        "report": new_report.report,
        "sif_potential": new_report.sif_potential,
        "risk_level": new_report.risk_level,
        "life_saving_rule": new_report.life_saving_rule,
        "hazard": new_report.hazard,
        "barrier_failure": new_report.barrier_failure,
        "confidence": new_report.confidence,
        "created_at": new_report.created_at
    }


# =========================================================
# GET ALL REPORTS
# =========================================================

@app.get("/reports")
def get_reports(
    db: Session = Depends(get_db)
):

    reports = (
        db.query(SafetyReport)
        .order_by(SafetyReport.id.desc())
        .all()
    )

    return reports


# =========================================================
# GET SINGLE REPORT
# =========================================================

@app.get("/reports/{report_id}")
def get_report(
    report_id: int,
    db: Session = Depends(get_db)
):

    report = (
        db.query(SafetyReport)
        .filter(SafetyReport.id == report_id)
        .first()
    )

    if report is None:
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )

    return report


# =========================================================
# DELETE REPORT
# =========================================================
# NOTE:
# This endpoint exists for administrator/backend use.
# The worker report.html does NOT show a delete button.
# =========================================================

@app.delete("/reports/{report_id}")
def delete_report(
    report_id: int,
    db: Session = Depends(get_db)
):

    report = (
        db.query(SafetyReport)
        .filter(SafetyReport.id == report_id)
        .first()
    )

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


# =========================================================
# STATISTICS
# =========================================================

@app.get("/statistics")
def get_statistics(
    db: Session = Depends(get_db)
):

    reports = db.query(SafetyReport).all()

    total_reports = len(reports)

    sif_reports = sum(
        1 for report in reports
        if report.sif_potential == "YES"
    )

    high_risk = sum(
        1 for report in reports
        if report.risk_level == "HIGH"
    )

    medium_risk = sum(
        1 for report in reports
        if report.risk_level == "MEDIUM"
    )

    low_risk = sum(
        1 for report in reports
        if report.risk_level == "LOW"
    )

    return {
        "total_reports": total_reports,
        "sif_reports": sif_reports,
        "high_risk": high_risk,
        "medium_risk": medium_risk,
        "low_risk": low_risk
    }