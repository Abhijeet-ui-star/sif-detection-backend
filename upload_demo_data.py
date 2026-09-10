import requests

API_URL = "https://sif-detection-backend.onrender.com/analyze"

demo_reports = [
    "Worker entered a confined space. Oxygen level is low and toxic gas is detected.",
    "Welding work was carried out near flammable material without proper fire protection.",
    "Maintenance worker performed lockout tagout but the equipment was not properly isolated.",
    "Worker was working at height without a safety harness.",
    "Worker was standing near a suspended load during a crane lifting operation.",
    "An electrical worker found an exposed live wire near the work area.",
    "Workers were carrying out excavation work without adequate trench protection.",
    "A vehicle was reversing in the work area without proper pedestrian control.",
    "Hydrogen sulfide gas was detected in the work area.",
    "Grinding operation was performed without following hot work precautions.",
    "Worker inspected the hand tools before starting the maintenance activity.",
    "Safety briefing was completed before starting the work.",
    "Worker used the required personal protective equipment during routine inspection.",
    "Work area was cleaned and housekeeping was maintained properly.",
    "Emergency exit was checked and found clear.",
    "Fire extinguisher inspection was completed and equipment was accessible.",
    "Worker followed the approved safe operating procedure during routine maintenance.",
    "Safety signage was clearly visible around the work area.",
    "Routine equipment inspection was completed with no significant safety issue.",
    "Workers attended the daily toolbox talk before starting the shift."
]

for i, report in enumerate(demo_reports, start=1):

    try:
        response = requests.post(
            API_URL,
            json={"report": report}
        )

        if response.status_code == 200:
            print(f"Report {i} uploaded successfully")
        else:
            print(f"Report {i} failed: {response.status_code}")
            print(response.text)

    except Exception as e:
        print(f"Report {i} error: {e}")

print("Finished uploading demo reports.")