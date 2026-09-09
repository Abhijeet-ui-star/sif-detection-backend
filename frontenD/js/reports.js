// Load all reports from backend
async function loadReports() {

    const container = document.getElementById("reportsContainer");

    try {

        const data = await getReports();

        if (!data.success) {
            throw new Error("Unable to load reports");
        }

        // Check if reports exist
        if (data.reports.length === 0) {

            container.innerHTML = `
                <p>No safety reports found.</p>
            `;

            return;
        }

        // Clear loading message
        container.innerHTML = "";

        // Create cards for each report
        data.reports.forEach(report => {

            const reportCard = document.createElement("div");

            reportCard.className = "feature-card";
            reportCard.style.marginTop = "20px";

            reportCard.innerHTML = `
                <h3>Report #${report.id}</h3>

                <p>
                    <strong>Observation:</strong><br>
                    ${report.report}
                </p>

                <p>
                    <strong>SIF Potential:</strong>
                    ${report.sif_potential}
                </p>

                <p>
                    <strong>Risk Level:</strong>
                    ${report.risk_level}
                </p>

                <p>
                    <strong>Life Saving Rule:</strong>
                    ${report.life_saving_rule}
                </p>

                <p>
                    <strong>Hazard:</strong>
                    ${report.hazard}
                </p>

                <p>
                    <strong>Barrier Failure:</strong>
                    ${report.barrier_failure}
                </p>

                <p>
                    <strong>Confidence:</strong>
                    ${(report.confidence * 100).toFixed(0)}%
                </p>

                <p>
                    <strong>Date:</strong>
                    ${report.created_at}
                </p>

                <button onclick="viewReportDetails(${report.id})">
                    View Details
                </button>

                <button onclick="deleteReportFromPage(${report.id})">
                    Delete Report
                </button>
            `;

            container.appendChild(reportCard);

        });

    } catch (error) {

        console.error("Reports error:", error);

        container.innerHTML = `
            <p>
                Unable to load reports.
                Please check the backend connection.
            </p>
        `;
    }
}


// View report details
function viewReportDetails(reportId) {

    window.location.href =
        "report-details.html?id=" + reportId;
}


// Delete report
async function deleteReportFromPage(reportId) {

    const confirmDelete = confirm(
        "Are you sure you want to delete this report?"
    );

    if (!confirmDelete) {
        return;
    }

    try {

        const data = await deleteReport(reportId);

        if (data.success) {

            alert("Report deleted successfully.");

            loadReports();

        } else {

            alert("Unable to delete report.");

        }

    } catch (error) {

        console.error("Delete error:", error);

        alert("Backend connection error.");

    }
}


// Load reports when page opens
loadReports();