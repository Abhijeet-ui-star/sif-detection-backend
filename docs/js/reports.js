// Load all reports from backend

async function loadReports() {

    const container =
        document.getElementById("reportsContainer");

    try {

        console.log("Loading reports...");

        const reports =
            await getReports();

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
                <p>
                    No safety reports found.
                </p>
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


            // Confidence

            const confidence =
                typeof report.confidence === "number"
                    ? Math.round(
                        report.confidence * 100
                    ) + "%"
                    : "N/A";


            // SIF status

            let sifStatus =
                report.sif_potential ?? "N/A";


            if (
                report.sif_potential === "YES"
            ) {

                sifStatus =
                    "🔴 YES - SIF";

            } else if (
                report.sif_potential === "NO"
            ) {

                sifStatus =
                    "🟢 NO - SIF";
            }


            // Risk status

            let riskStatus =
                report.risk_level ?? "N/A";


            if (
                report.risk_level === "HIGH"
            ) {

                riskStatus =
                    "🔴 HIGH";

            } else if (
                report.risk_level === "MEDIUM"
            ) {

                riskStatus =
                    "🟠 MEDIUM";

            } else if (
                report.risk_level === "LOW"
            ) {

                riskStatus =
                    "🟢 LOW";
            }


            // Report card

            reportCard.innerHTML = `

                <h3>
                    Report #${report.id}
                </h3>


                <p>

                    <strong>
                        SIF Potential:
                    </strong>

                    ${sifStatus}

                </p>


                <p>

                    <strong>
                        Risk Level:
                    </strong>

                    ${riskStatus}

                </p>


                <p>

                    <strong>
                        Observation:
                    </strong>

                    <br>

                    ${report.report ?? "N/A"}

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
                    onclick="
                        viewReportDetails(${report.id})
                    "
                >
                    View Details
                </button>

            `;


            container.appendChild(
                reportCard
            );

        });


    } catch (error) {

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