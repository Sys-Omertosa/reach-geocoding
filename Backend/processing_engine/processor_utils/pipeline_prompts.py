file_1 = ""
file_2 = ""
file_3 = ""


json_prompt = """Convert the attached Pakistani disaster alert/information document to the specified CAP-derived JSON structure. Output only English text and ignore any Urdu text.
Try to understand images in detail and make the extracted JSON information informed by the content of the text and the images/maps/charts in the document. Don't miss any information.
Be wary of typos in the document, and correct if possible. Output only the JSON object, without any leading or trailing markdown.

# Field Definitions:
- **category**: Type of alert. The only valid values are: "Geo", "Met", "Safety", "Security", "Rescue", "Fire", "Health", "Env", "Transport", "Infra", "CBRNE", "Other"
- **event**: Brief name or title of the hazard or event (e.g., "Severe Thunderstorm", "Wildfire", "Flood Warning")
- **urgency**: Response time expected. The only valid values are: "Immediate", "Expected", "Future", "Past", "Unknown"
- **severity**: Severity of the event. The only valid values are: "Extreme", "Severe", "Moderate", "Minor", "Unknown"
- **description**: Description of the alert situation, hazards, and expected impacts in simple language
- **instruction**: Recommended actions for citizens (not government personnel) to take. If no citizen-centric instructions present but needed, generate your own with [AI-generated] tag at the end

- **effective_from**: ISO 8601 datetime when alert becomes active (e.g., "2024-03-15T14:30:00Z")
- **effective_until**: ISO 8601 datetime when alert expires
- **areas**: Array of affected locations with optional area-specific overrides

# Area Object Fields:
- **place_names**: Array of location names (cities, provinces, disctricts, province with directional term, etc.)
- **specific_effective_from**: (Optional) Override effective_from for this area(s)
- **specific_effective_until**: (Optional) Override effective_until for this area(s)
- **specific_urgency**: (Optional) Override urgency for this area(s)
- **specific_severity**: (Optional) Override severity for this area(s)
- **specific_instruction**: (Optional) Additional or override instructions for this area(s)

# Place Names:
- **Abbreviations**: Convert each abbreviation to its full form, like AJ&K to Azad Jammu and Kashmir.
- **Directional**: Extract directional for regions to a unified form, like "North-Eastern Balochistan". The only valid values are "North", "South", "East", "West", "Central", "North-Eastern", "North-Western", "South-Eastern" and "South-Western".
- **Overlap**: Try to avoid overlaps and be as specific as possible. For examples, if specific districts from a province relevant to the alert are mentioned alongside name of the entire province, use only specific districts.
- **Infrastructure**: When specific infrastructure is mentioned, convert it to the disctricts/tehsils containing it. For example:
    - "Tarbela Dam" to "Haripur"
    - "Motorways M2 and M5" to "Multan", "Bahawalpur", "Rahim Yar Khan", "Ghotki", "Sukkur", "Rawalpindi", "Chakwal", "Khushab", "Sargodha", "Sheikhupura", "Lahore"
- **Examples**: Some examples for the wrong and correct values:
    1.  Wrong: "Balochistan (Quetta, Ziarat, Zhob, Sherani, Chaman, Pishin, Qilla Abdullah, Qilla, Saifullah, Noushki)"
        Correct: "Quetta", "Ziarat", "Zhob", "Sherani", "Chaman", "Pishin", "Qilla Abdullah", "Qilla", "Saifullah", "Noushki"
    2.  Wrong: "Punjab (plain areas)"
        Correct: "Central Punjab", "South Punjab"
    3.  Wrong: "Upper Sindh"
        Correct: "North Sindg"
    4.  Wrong: "Potohar region"
        Correct: "Rawalpindi", "Attock", "Chakwal", "Jhelum"

# JSON Response Format:
{
  "category": "string",
  "event": "string",
  "urgency": "string",
  "severity": "string",
  "description": "string",
  "instruction": "string",
  "effective_from": "ISO 8601 datetime",
  "effective_until": "ISO 8601 datetime",
  "areas": [
    {
      "place_names": ["string"],
      "specific_effective_from": "ISO 8601 datetime or null",
      "specific_effective_until": "ISO 8601 datetime or null",
      "specific_urgency": "string or null",
      "specific_severity": "string or null",
      "specific_instruction": "string or null"
    }
  ]
}"""

