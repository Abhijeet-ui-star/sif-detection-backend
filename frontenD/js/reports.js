// Load all reports from backend
async function loadReports() {

    const container = document.getElementById("reportsContainer");

    try {

        const reports = await getReports();

        // Check if reports exist
        if (!Array.isArray(reports) || reports.length === 0) {

            container.innerHTML = `
                <p>No safety reports found.</p>
            `;

            return;
        }

        // Clear loading message
        container.innerHTML = "";

        // Create cards for each report
        reports.forEach(report => {

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


// Load reports when page opens
loadReports();