// Load safety statistics
async function loadStatistics() {

    try {

        // Get statistics from backend
        const data = await getStatistics();

        if (!data.success) {
            throw new Error("Unable to load statistics");
        }

        const statistics = data.statistics;

        // Display statistics
        document.getElementById("totalReports").textContent =
            statistics.total_reports;

        document.getElementById("sifDetected").textContent =
            statistics.sif_detected;

        document.getElementById("highRisk").textContent =
            statistics.high_risk;

        document.getElementById("lowRisk").textContent =
            statistics.low_risk;

    }

    catch (error) {

        console.error("Statistics error:", error);

        document.getElementById("totalReports").textContent = "Error";
        document.getElementById("sifDetected").textContent = "Error";
        document.getElementById("highRisk").textContent = "Error";
        document.getElementById("lowRisk").textContent = "Error";
    }
}


// Run when page loads
loadStatistics();