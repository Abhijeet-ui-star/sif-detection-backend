async function analyzeSafetyReport() {

    const reportInput = document.getElementById("reportInput");
    const reportText = reportInput.value.trim();

    // Empty report check
    if (reportText === "") {
        showError("Please enter a safety observation.");
        return;
    }

    try {

        // Show result section
        document.getElementById("resultSection").style.display = "block";
        document.getElementById("errorSection").style.display = "none";

        // Loading
        document.getElementById("sifPotential").textContent = "Analyzing...";
        document.getElementById("riskLevel").textContent = "Analyzing...";
        document.getElementById("lifeSavingRule").textContent = "Analyzing...";
        document.getElementById("hazard").textContent = "Analyzing...";
        document.getElementById("barrierFailure").textContent = "Analyzing...";
        document.getElementById("confidence").textContent = "Analyzing...";

        // Call backend through api.js
        const result = await analyzeReport(reportText);

        // Display result
        document.getElementById("sifPotential").textContent =
            result.sif_potential ?? "N/A";

        document.getElementById("riskLevel").textContent =
            result.risk_level ?? "N/A";

        document.getElementById("lifeSavingRule").textContent =
            result.life_saving_rule ?? "N/A";

        document.getElementById("hazard").textContent =
            result.hazard ?? "N/A";

        document.getElementById("barrierFailure").textContent =
            result.barrier_failure ?? "N/A";

        // Confidence
        if (typeof result.confidence === "number") {
            document.getElementById("confidence").textContent =
                Math.round(result.confidence * 100) + "%";
        } else {
            document.getElementById("confidence").textContent = "N/A";
        }

        // Show result
        document.getElementById("resultSection").style.display = "block";

    } catch (error) {

        console.error("Analysis error:", error);

        showError(
            "Unable to connect to backend. Make sure FastAPI server is running."
        );
    }
}


// =====================================================
// SHOW ERROR
// =====================================================

function showError(message) {

    document.getElementById("errorMessage").textContent = message;

    document.getElementById("errorSection").style.display = "block";

    document.getElementById("resultSection").style.display = "none";
}


// =====================================================
// GO HOME
// =====================================================

function goHome() {
    window.location.href = "./index.html";
}