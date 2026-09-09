// ===============================
// BACKEND CONNECTION
// ===============================

const API_URL = "https://sif-detection-backend.onrender.com";


// ===============================
// ANALYZE SAFETY REPORT
// ===============================

async function analyzeReport(reportText) {

    const response = await fetch(`${API_URL}/analyze`, {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            report: reportText
        })

    });


    const data = await response.json();

    return data;
}


// ===============================
// GET ALL REPORTS
// ===============================

async function getReports() {

    const response = await fetch(
        `${API_URL}/reports`
    );

    const data = await response.json();

    return data;
}


// ===============================
// GET ONE REPORT
// ===============================

async function getReport(reportId) {

    const response = await fetch(
        `${API_URL}/reports/${reportId}`
    );

    const data = await response.json();

    return data;
}


// ===============================
// GET STATISTICS
// ===============================

async function getStatistics() {

    const response = await fetch(
        `${API_URL}/statistics`
    );

    const data = await response.json();

    return data;
}


// ===============================
// DELETE REPORT
// ===============================

async function deleteReport(reportId) {

    const response = await fetch(
        `${API_URL}/reports/${reportId}`,
        {
            method: "DELETE"
        }
    );

    const data = await response.json();

    return data;
}