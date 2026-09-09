// Analyze safety report
async function analyzeSafetyReport() {

    const reportInput = document.getElementById("reportInput");

    const reportText = reportInput.value.trim();

    // Check empty report
    if (reportText === "") {
        showError("Please enter a safety observation.");
        return;
    }

    try {

        // Call backend API
        const data = await analyzeReport(reportText);

        // Check backend response
        if (!data.success) {
            showError("Unable to analyze the report.");
            return;
        }

        // Get result from backend
        const result = data.result;

        // Display result
        document.getElementById("sifPotential").textContent =
            result.sif_potential;

        document.getElementById("riskLevel").textContent =
            result.risk_level;

        document.getElementById("lifeSavingRule").textContent =
            result.life_saving_rule;

        document.getElementById("hazard").textContent =
            result.hazard;

        document.getElementById("barrierFailure").textContent =
            result.barrier_failure;

        document.getElementById("confidence").textContent =
            (result.confidence * 100) + "%";


        // Show result
        document.getElementById("resultSection").style.display = "block";

        // Hide previous error
        document.getElementById("errorSection").style.display = "none";

    }

    catch (error) {

        console.error(error);

        showError(
            "Unable to connect to backend. Please try again."
        );
    }
}


// Show error message
function showError(message) {

    document.getElementById("errorMessage").textContent =
        message;

    document.getElementById("errorSection").style.display =
        "block";

    document.getElementById("resultSection").style.display =
        "none";
}


// Go back to home page
function goHome() {

    window.location.href = "index.html";

}