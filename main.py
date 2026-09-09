from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

from sif_detector import analyze_report
from database import engine, SessionLocal
from models import Base, SafetyReport


# ==========================================
# CREATE DATABASE TABLES
# ==========================================

Base.metadata.create_all(bind=engine)


# ==========================================
# CREATE FASTAPI APPLICATION
# ==========================================

app = FastAPI(
    title="OIL SIF Detection API",
    description="AI/NLP API for detecting SIF precursors",
    version="1.0.0"
)


# ==========================================
# CORS CONFIGURATION
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# REQUEST FORMAT
# ==========================================

class ReportRequest(BaseModel):
    report: str


# ==========================================
# DATABASE SESSION
# ==========================================

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# ==========================================
# HOME API
# ==========================================

@app.get("/")
def home():

    return {
        "message": "OIL SIF Detection API is running"
    }


# ==========================================
# ANALYZE SAFETY REPORT
# ==========================================

@app.post("/analyze")
def analyze(
    data: ReportRequest,
    db: Session = Depends(get_db)
):

    # Check empty or very short reports
    if not data.report or len(data.report.strip()) < 10:

        raise HTTPException(
            status_code=400,
            detail="Invalid report. Please enter a proper safety observation."
        )


    # Safety-related keywords
    safety_keywords = [

        "worker",
        "work",
        "safety",
        "hazard",
        "risk",
        "gas",
        "oxygen",
        "fire",
        "welding",
        "confined",
        "height",
        "electrical",
        "lifting",
        "excavation",
        "vehicle",
        "lockout",
        "maintenance",
        "ppe",
        "equipment",
        "incident",
        "unsafe",
        "danger"

    ]


    report_lower = data.report.lower()


    # Reject unrelated text
    if not any(
        keyword in report_lower
        for keyword in safety_keywords
    ):

        raise HTTPException(
            status_code=400,
            detail="Invalid safety report. Please enter a safety-related observation."
        )


    # Analyze report
    result = analyze_report(data.report)


    # Save result to database
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


    # Return result
    return {

        "success": True,

        "result": result,

        "database_id": new_report.id

    }


# ==========================================
# GET ALL REPORTS
# ==========================================

@app.get("/reports")
def get_reports(
    db: Session = Depends(get_db)
):

    reports = db.query(
        SafetyReport
    ).order_by(
        SafetyReport.id.desc()
    ).all()


    return {

        "success": True,

        "count": len(reports),

        "reports": reports

    }


# ==========================================
# GET ONE REPORT
# ==========================================

@app.get("/reports/{report_id}")
def get_report(
    report_id: int,
    db: Session = Depends(get_db)
):

    report = db.query(
        SafetyReport
    ).filter(
        SafetyReport.id == report_id
    ).first()


    if report is None:

        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )


    return {

        "success": True,

        "report": report

    }


# ==========================================
# GET STATISTICS
# ==========================================

@app.get("/statistics")
def get_statistics(
    db: Session = Depends(get_db)
):

    reports = db.query(
        SafetyReport
    ).all()


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


# ==========================================
# DELETE REPORT
# ==========================================

@app.delete("/reports/{report_id}")
def delete_report(
    report_id: int,
    db: Session = Depends(get_db)
):

    report = db.query(
        SafetyReport
    ).filter(
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


# ==========================================
# HEALTH CHECK
# ==========================================

@app.get("/health")
def health_check(
    db: Session = Depends(get_db)
):

    try:

        db.query(
            SafetyReport
        ).count()


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