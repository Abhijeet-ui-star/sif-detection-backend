// Load all reports from backend

async function loadReports() {

    const container =
        document.getElementById("reportsContainer");


    try {

        console.log("Loading reports...");


        // Get reports from backend

        const reports = await getReports();


        console.log(
            "REPORTS RESPONSE:",
            reports
        );


        // Check backend response

        if (!Array.isArray(reports)) {

            throw new Error(
                "Invalid reports response from backend."
            );

        }


        // No reports

        if (reports.length === 0) {

            container.innerHTML = `
                <p>No safety reports found.</p>
            `;

            return;

        }


        // Clear loading message

        container.innerHTML = "";


        // Create report cards

        reports.forEach(report => {

            const reportCard =
                document.createElement("div");


            reportCard.className =
                "feature-card";

            reportCard.style.marginTop =
                "20px";


            const confidence =
                typeof report.confidence === "number"
                    ? Math.round(report.confidence * 100) + "%"
                    : "N/A";


            reportCard.innerHTML = `

                <h3>
                    Report #${report.id}
                </h3>


                <p>

                    <strong>
                        Observation:
                    </strong>

                    <br>

                    ${report.report ?? "N/A"}

                </p>


                <p>

                    <strong>
                        SIF Potential:
                    </strong>

                    ${report.sif_potential ?? "N/A"}

                </p>


                <p>

                    <strong>
                        Risk Level:
                    </strong>

                    ${report.risk_level ?? "N/A"}

                </p>


                <p>

                    <strong>
                        Life Saving Rule:
                    </strong>

                    ${report.life_saving_rule ?? "N/A"}

                </p>


                <p>

                    <strong>
                        Hazard:
                    </strong>

                    ${report.hazard ?? "N/A"}

                </p>


                <p>

                    <strong>
                        Barrier Failure:
                    </strong>

                    ${report.barrier_failure ?? "N/A"}

                </p>


                <p>

                    <strong>
                        Confidence:
                    </strong>

                    ${confidence}

                </p>


                <p>

                    <strong>
                        Date:
                    </strong>

                    ${report.created_at ?? "N/A"}

                </p>


                <button
                    onclick="viewReportDetails(${report.id})"
                >
                    View Details
                </button>

            `;


            container.appendChild(
                reportCard
            );

        });

    }


    catch (error) {

        console.error(
            "Reports error:",
            error
        );


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