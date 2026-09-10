async function analyzeSafetyReport() {

    const reportInput =
        document.getElementById("reportInput");

    const reportText =
        reportInput.value.trim();


    if (reportText === "") {

        showError(
            "Please enter a safety observation."
        );

        return;
    }


    try {

        document.getElementById("errorSection")
            .style.display = "none";

        document.getElementById("resultSection")
            .style.display = "block";


        // Loading state

        document.getElementById("sifPotential")
            .textContent = "Analyzing...";

        document.getElementById("riskLevel")
            .textContent = "Analyzing...";

        document.getElementById("lifeSavingRule")
            .textContent = "Analyzing...";

        document.getElementById("hazard")
            .textContent = "Analyzing...";

        document.getElementById("barrierFailure")
            .textContent = "Analyzing...";

        document.getElementById("confidence")
            .textContent = "Analyzing...";


        document.getElementById("confidenceBar")
            .style.width = "0%";


        // Send report to backend

        const data =
            await analyzeReport(reportText);


        console.log(
            "BACKEND RESPONSE:",
            data
        );


        // Validate response

        if (
            !data ||
            !data.sif_potential
        ) {

            throw new Error(
                "Invalid response from backend."
            );
        }


        // Display results

        document.getElementById("sifPotential")
            .textContent =
            data.sif_potential ?? "N/A";


        document.getElementById("riskLevel")
            .textContent =
            data.risk_level ?? "N/A";


        document.getElementById("lifeSavingRule")
            .textContent =
            data.life_saving_rule ?? "N/A";


        document.getElementById("hazard")
            .textContent =
            data.hazard ?? "N/A";


        document.getElementById("barrierFailure")
            .textContent =
            data.barrier_failure ?? "N/A";


        // Confidence

        if (
            typeof data.confidence === "number"
        ) {

            const confidence =
                Math.round(
                    data.confidence * 100
                );


            document.getElementById("confidence")
                .textContent =
                confidence + "%";


            document.getElementById("confidenceBar")
                .style.width =
                confidence + "%";

        } else {

            document.getElementById("confidence")
                .textContent =
                "N/A";

            document.getElementById("confidenceBar")
                .style.width =
                "0%";
        }


        // Keep result visible

        document.getElementById("resultSection")
            .style.display = "block";

        document.getElementById("errorSection")
            .style.display = "none";


    } catch (error) {

        console.error(
            "Analysis error:",
            error
        );

        showError(
            "Unable to connect to backend. Please try again."
        );
    }
}


function showError(message) {

    document.getElementById("errorMessage")
        .textContent = message;

    document.getElementById("errorSection")
        .style.display = "block";

    document.getElementById("resultSection")
        .style.display = "none";
}


function goHome() {

    window.location.href =
        "index.html";
}