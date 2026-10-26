
import json
import os

import streamlit as st
from google import genai
from google.genai import types

from backend.app.main import PROMPT, demo


st.set_page_config(
    page_title="BuildSense AI",
    page_icon="🏗️",
    layout="wide",
)

st.title("🏗️ BuildSense AI")
st.subheader("AI-powered construction site intelligence")
st.write(
    "Upload site images and enter project details to review "
    "potential safety concerns, cracks, planning estimates, "
    "and site recommendations."
)

with st.sidebar:
    st.header("Project details")

    description = st.text_area(
        "Site description",
        placeholder="Describe the construction site and current work...",
    )

    area = st.number_input(
        "Built-up area (sq ft)",
        min_value=0.0,
        value=1000.0,
        step=100.0,
    )

    rate = st.number_input(
        "Estimated construction rate (INR/sq ft)",
        min_value=0.0,
        value=1800.0,
        step=100.0,
    )

    floors = st.number_input(
        "Number of floors",
        min_value=1,
        value=1,
        step=1,
    )

    st.caption("Cost and duration outputs are rough estimates.")

uploaded_images = st.file_uploader(
    "Upload construction-site images",
    type=["png", "jpg", "jpeg", "webp"],
    accept_multiple_files=True,
    help="Use clear overall views and close-up images where relevant.",
)

if uploaded_images:
    st.write(f"Images uploaded: {len(uploaded_images)}")
    cols = st.columns(min(len(uploaded_images), 3))

    for i, image_file in enumerate(uploaded_images):
        with cols[i % len(cols)]:
            st.image(
                image_file,
                caption=image_file.name,
                use_container_width=True,
            )

analyze_clicked = st.button(
    "Analyze construction site",
    type="primary",
    use_container_width=True,
)

if analyze_clicked:
    if not description.strip() and not uploaded_images:
        st.warning("Please enter a site description or upload an image.")
        st.stop()

    project = {
        "built_up_area_sqft": area,
        "cost_per_sqft_inr": rate,
        "floors": floors,
    }

    api_key = os.getenv("GEMINI_API_KEY", "").strip()

    if not api_key:
        try:
            api_key = st.secrets.get("GEMINI_API_KEY", "").strip()
        except Exception:
            api_key = ""

    if not api_key:
        st.info(
            "Gemini is not configured. Showing the existing demo-mode "
            "result; uploaded images will not be analyzed by AI."
        )
        result = demo(description, project)

    else:
        parts = [
            types.Part.from_text(
                text=(
                    f"Project data: {json.dumps(project)}\n"
                    f"Site description: {description}"
                )
            )
        ]

        too_large = [
            image_file.name
            for image_file in uploaded_images
            if image_file.size > 10 * 1024 * 1024
        ]

        if too_large:
            st.error(
                "Each image must be 10 MB or smaller: "
                + ", ".join(too_large)
            )
            st.stop()

        for image_file in uploaded_images:
            parts.append(
                types.Part.from_bytes(
                    data=image_file.getvalue(),
                    mime_type=image_file.type,
                )
            )

        try:
            with st.spinner("Analyzing the construction site..."):
                client = genai.Client(api_key=api_key)

                response = client.models.generate_content(
                    model=os.getenv(
                        "GEMINI_MODEL",
                        "gemini-2.5-flash",
                    ),
                    contents=[
                        types.Content(role="user", parts=parts)
                    ],
                    config=types.GenerateContentConfig(
                        system_instruction=PROMPT,
                        response_mime_type="application/json",
                        temperature=0.2,
                    ),
                )

                result = json.loads(response.text)
                result["mode"] = "gemini"

        except Exception:
            st.error(
                "AI analysis failed. Check your Gemini API key, "
                "model configuration, and deployment logs."
            )
            st.stop()

    st.divider()
    st.header("Analysis results")

    st.caption(f"Analysis mode: {result.get('mode', 'unknown')}")

    st.subheader("Project summary")
    st.write(result.get("summary", "No summary provided."))

    safety = result.get("safety", {})
    st.subheader("🦺 Safety assessment")
    st.write("Overall risk:", safety.get("overall_risk", "Unknown"))

    for finding in safety.get("findings", []):
        with st.expander(
            f"{finding.get('severity', 'Unknown').upper()}: "
            f"{finding.get('issue', 'Finding')}"
        ):
            st.write("Evidence:", finding.get("evidence", "Not provided"))
            st.write(
                "Recommended action:",
                finding.get("recommended_action", "Not provided"),
            )

    cracks = result.get("cracks", {})
    st.subheader("🧱 Crack assessment")
    st.write("Observed:", cracks.get("observed", "Not assessed"))
    st.write("Type:", cracks.get("crack_type", "Not assessed"))
    st.write("Severity:", cracks.get("severity", "Not assessed"))

    st.write("Probable causes:")
    st.write(cracks.get("probable_causes", []))

    st.write("Recommended actions:")
    st.write(cracks.get("recommended_actions", []))
    st.caption(cracks.get("disclaimer", "Not a structural diagnosis."))

    planning = result.get("planning", {})
    st.subheader("📋 Construction planning")
    st.write(planning.get("project_summary", ""))
    st.write(
        "Estimated duration (days):",
        planning.get("estimated_duration_days", "Not available"),
    )
    st.write("Milestones:", planning.get("milestones", []))

    materials = planning.get("materials", [])
    if materials:
        st.dataframe(materials, use_container_width=True)

    total_cost = planning.get("estimated_total_cost_inr")
    if total_cost is not None:
        st.metric("Estimated construction cost", f"₹{total_cost:,.0f}")

    valuation = result.get("valuation", {})
    st.subheader("🏠 Property valuation")
    value = valuation.get("estimated_value_inr")

    if value is not None:
        st.metric("Estimated value", f"₹{value:,.0f}")
    else:
        st.info("A property value could not be reliably estimated.")

    st.write("Confidence:", valuation.get("confidence", "Unknown"))
    st.write(valuation.get("note", ""))

    advice = result.get("site_advice", {})
    st.subheader("📍 Site recommendations")
    for item in advice.get("advice", []):
        st.write(f"- {item}")

    st.write("Weather:", advice.get("weather_note", ""))

    limitations = result.get("limitations", [])
    if limitations:
        st.subheader("Limitations")
        for item in limitations:
            st.write(f"- {item}")

    st.download_button(
        "Download analysis as JSON",
        data=json.dumps(result, indent=2, ensure_ascii=False),
        file_name="buildsense_analysis.json",
        mime="application/json",
    )
