
// Load safety statistics

async function loadStatistics() {

    try {

        console.log("Loading statistics...");

        // Get statistics from backend
        const statistics = await getStatistics();

        console.log(
            "STATISTICS RESPONSE:",
            statistics
        );


        // Check backend response

        if (!statistics) {

            throw new Error(
                "No statistics received from backend."
            );

        }


        // Display Total Reports

        document.getElementById("totalReports")
            .textContent =
            statistics.total_reports ?? 0;


        // Display SIF Detected

        document.getElementById("sifDetected")
            .textContent =
            statistics.sif_reports ?? 0;


        // Display High Risk

        document.getElementById("highRisk")
            .textContent =
            statistics.high_risk ?? 0;


        // Display Low Risk

        document.getElementById("lowRisk")
            .textContent =
            statistics.low_risk ?? 0;


    }

    catch (error) {

        console.error(
            "Statistics error:",
            error
        );


        document.getElementById("totalReports")
            .textContent = "Error";

        document.getElementById("sifDetected")
            .textContent = "Error";

        document.getElementById("highRisk")
            .textContent = "Error";

        document.getElementById("lowRisk")
            .textContent = "Error";

    }

}


// Load statistics when page opens

loadStatistics();