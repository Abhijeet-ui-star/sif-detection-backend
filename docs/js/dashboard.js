// Load safety statistics
async function loadStatistics() {

    try {

        // Get statistics from backend
        const statistics = await getStatistics();

        // Display statistics
        document.getElementById("totalReports").textContent =
            statistics.total_reports ?? 0;

        document.getElementById("sifDetected").textContent =
            statistics.sif_reports ?? 0;

        document.getElementById("highRisk").textContent =
            statistics.high_risk ?? 0;

        document.getElementById("lowRisk").textContent =
            statistics.low_risk ?? 0;

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