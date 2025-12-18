from PIL import Image
from pathlib import Path
from processing_engine.processor_utils.doc_utils import to_base64

PARENT_DIR = Path(__file__).parent.parent
markdown_prompt = """Extract all text as-is from this image in markdown format. 
Preserve the structure, headings, lists, tables, diagrams and formatting as much as possible. 
Return only the English markdown without any preamble. Ignore Urdu text. Format tables as markdown or html.
Wrap contents from inside a diagram in "<!-- Diagram -->" comments before and after the diagram content.
"""

json_prompt = """Convert this markdown extracted from a VLM from a Pakistani disaster alert/information document to CAP-inspired JSON structure.
As this was extracted from a VLM, take the markdown structure and content with a grain of salt, and convert place names and 
abbreviations to their full form. Convert directional descriptions to a standard form like (North, Northern, Northern parts, Upper) ->(Northern).
Convert names of roads, highways, etc. to the districts and provinces containing them.

# Field Definitions:
- **category**: Type of alert. Valid values: "Geo", "Met", "Safety", "Security", "Rescue", "Fire", "Health", "Env", "Transport", "Infra", "CBRNE", "Other"
- **event**: Brief name of the hazard or event (e.g., "Severe Thunderstorm", "Wildfire", "Flood Warning")
- **urgency**: Response time expected. Valid values: "Immediate", "Expected", "Future", "Past", "Unknown"
- **severity**: Severity of the event. Valid values: "Extreme", "Severe", "Moderate", "Minor", "Unknown"
- **description**: Detailed description of the alert situation, hazards, and expected impacts
- **instruction**: Recommended actions for recipients to take
- **effective_from**: ISO 8601 datetime when alert becomes active (e.g., "2024-03-15T14:30:00Z")
- **effective_until**: ISO 8601 datetime when alert expires
- **areas**: Array of affected locations with optional area-specific overrides

# Area Object Fields:
- **place_names**: Array of location names (cities, regions, counties, etc.)
- **specific_effective_from**: (Optional) Override effective_from for this area
- **specific_effective_until**: (Optional) Override effective_until for this area
- **specific_urgency**: (Optional) Override urgency for this area
- **specific_severity**: (Optional) Override severity for this area
- **specific_instruction**: (Optional) Additional or override instructions for this area

# JSON Response Format:
```json
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
}
```

**Alert Text:**
{{text}}
"""

EXAMPLE_IMAGES = {
    "9PPqpSasTb07UWPKiyXV": to_base64(Image.open(PARENT_DIR / "examples/9PPqpSasTb07UWPKiyXV.jpg")),
    "cX5UVWicUxYs0Ub9642D": to_base64(Image.open(PARENT_DIR / "examples/cX5UVWicUxYs0Ub9642D.jpg")),
    "evgtuouxcEBpD4FSxL9w": to_base64(Image.open(PARENT_DIR / "examples/evgtuouxcEBpD4FSxL9w.jpg")),
    "InXkmGJqQbCXx7aRyjXA": to_base64(Image.open(PARENT_DIR / "examples/InXkmGJqQbCXx7aRyjXA.jpg")),
    "K6y19XCyAM7nXz8wVUyL": to_base64(Image.open(PARENT_DIR / "examples/K6y19XCyAM7nXz8wVUyL.jpg")),
    "UUMqxsp0XrFeQmUWc1Xo": to_base64(Image.open(PARENT_DIR / "examples/UUMqxsp0XrFeQmUWc1Xo.jpg")),
    "WMpJfGUze00GwXezWekr": to_base64(Image.open(PARENT_DIR / "examples/WMpJfGUze00GwXezWekr.jpg")),
}

def markdown_messages(base64_image):
    """Prepares prompt for conversion of image to markdown, along with examples (few-shot prompting)"""
    return [
                {
                    "role": "system",
                    "content": "You are an OCR expert specializing in disaster alert documents. Extract all text exactly as it appears, preserving the reading order from top to bottom, left to right. Include text from maps, charts, and all visual elements."
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": markdown_prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{EXAMPLE_IMAGES['cX5UVWicUxYs0Ub9642D']}"
                            }
                        }
                    ]
                },
                {
                    "role": "assistant",
                    "content": """
Page 8 of 9
# **PRESS RELEASE**

**Government of Pakistan**
Ministry of Defence (Defence Division)
**Pakistan Meteorological Department**
**National Weather Forecasting Centre**
Sector H-8/2, Islamabad.

**Tel:** 051-9250363
**Fax:** 051-9250368

NWFC-5/10A1/2017/146
*Press Release:*

**Date:** 12th December, 2025
**Time:** 12:15 PST

# **Rain-Thunderstorm (snowfall over the hills) predicted in western and northern parts of the country during the weekend**
## **Foggy conditions are likely to intensify over plain areas of the country**

Met office predicted that a shallow western disturbance is likely to approach western parts of the country on 12th (night) December. Under the influence of this weather system:

- Light to moderate rain-thunderstorm (snowfall over the hills) is expected in Chitral, Dir, Swat, Shangla, Kohistan, Malakand, Manshera, Abbottabad, Haripur, Bunner, Gilgit-Baltistan (Diamir, Astore, Ghizer, Skardu, Hunza, Gilgit, Ghanche, Shigar), Kashmir (Neelum valley, Muzaffarabad, Pooneh, Haitian, Bagh, Haveli) from **13th to 15th December** with occasional gaps.
- Partly cloudy to cloudy conditions with light rain/snowfall is expected in Bajaur, Mohmand, Khyber, Orakzai, Kurram, Waziristan, Quetta, Ziarat, Zhob, Sherani, Chaman, Pishin, Qilla Abdullah, Qilla Saifullah and Noushki on **14th/15th December**. There are chances of drizzle in Islamabad/Rawalpindi, Peshawar, Potohar region and light rain/light snow in Murree & Galliyat on **Sunday/Monday**.
- **Moderate, at time dense foggy conditions** are likely to develop over plain areas of Punjab, Khyber Pakhtunkhwa and upper Sindh from **12th(night) to 16th December**.

**Another western disturbance is likely to influence western and upper parts of the country from 19th December**.

### Possible Impacts and advice:
- **Snowfall** may cause road closure/slippery conditions in Naran, Kaghan, Kalam, Malam Jabba, Chitral, Dir, Swat, Kohistan, Shangla, Astore, Hunza, Skardu, Quetta, Ziarat and Chaman during forecast period.
- **Possibility of the landslides** in vulnerable areas of upper **Khyber Pakhtunkhwa and Gilgit-Baltistan** during the period.
- **Foggy conditions** may reduce visibility significantly and disrupt traffic over motorways and highways. **Public is advised to remain cautious during the period.**
- **Day temperatures are likely to drop during the forecast period.**
- **Tourists and travelers** visiting mountainous areas are also advised to remain cautious during the period.
- **Farmers are advised** to manage their activities keeping in view the latest weather forecast.

**For daily weather updates please visit:** https://www.pmd.gov.pk/en/.
**Pak Weather application:** https://play.google.com/store/apps/details?id=com.pmd.kissan

### Distributions:
1.  MS to PM, Islamabad
2.  Secretary Defence, Ministry of Defence Rawalpindi
3.  Chief Sec Punjab, KP, GB, Kashmir, Balochistan & Sindh
4.  Secretary Irrigation Punjab, KP, GB, Kashmir, Balochistan & Sindh
5.  Secretary Agriculture Punjab, KP, GB, Kashmir, Balochistan & Sindh
6.  Chairman NDMA
7.  Chairman NHA
8.  IG Motorways
9.  DG’s PDMA & SDMA
10. Secretary Health, MOCC & Water Resources.
11. Secretary National Food Security and Research
12. Chairman FFC & IRSA
13. Director to Minister for MOOC
14. Chief Commissioner Islamabad
15. Commissioner Rawalpindi
16. Rescue 1122.
17. Directors RMC’s & Electronic and Print Media.

*Spokesperson*  
*Ph: 051-9250363-4*
"""
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": markdown_prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{EXAMPLE_IMAGES['evgtuouxcEBpD4FSxL9w']}"
                            }
                        }
                    ]
                },
                {
                    "role": "assistant",
                    "content": """
Page 1 of 7

**MOST IMMEDIATE**

F.2(E)/2025-NDMA (MW/ Weather Advisory)  
**Government of Pakistan Prime Minister’s Office**  
**National Disaster Management Authority (HQ)**  
Main Murree Road Near ITP Office, Islamabad  

Dated: 4 December 2025  

Subject: **LIGHT RAIN WITH SNOWFALL OVER THE MOUNTAINS IS EXPECTED IN NORTHERN AREAS ON 5TH DECEMBER 2025**  

A **shallow Westerly wave** is likely to affect **Northern areas** of the country from **4th (night) till 5th December, 2025**. Under the influence of this weather system: Mostly cloudy weather conditions are expected with **light rain-snowfall** over the mountains is expected at isolated places in **Gilgit-Baltistan**, **Kashmir** and **upper Khyber-Pakhtunkhwa** (Dir, Chitral, Swat, Kohistan, Shangla, Battagram) on **4th** (night) & **5th December 2025**. **Cold and dry** weather conditions are likely to continue in other parts of the country.  

2. **Smoggy/foggy** conditions are likely to continue in parts of **plain areas of Punjab** (Sialkot, Narowal, Lahore, Sheikhupura, Gujranwala, Gujrat, Jhelum, Faisalabad, Sahiwal, Multan, Khanewal, Layyah, Kot Addu and Bahawalpur) and **Khyber-Pakhtunkhwa** (Peshawar, Swabi, Mardan. D.I. Khan) **during night** and especially in **morning hours**.  

<!-- Diagram -->
#### **Light Rain with Snowfall over the Mountains is Expected in Northern Areas from 4th to 5th December and Smog Condition will Continue in Various Areas of the Country**  

**GB:**  
- Diamir  
- Astore  
- Ghizer  
- Skardu  
- Hunza  
- Gilgit  
- Ghanche  
- Shigar  

**KP:**  
- Dir  
- Chitral  
- Swat  
- Kohistan  
- Shangla  
- Battagram  

**AJ&K:**  
- Muzaffarabad  
- Neelum valley  
- Rawalakot  
- Poonch  
- Hattian  
- Bagh  
- Haveli  
- Sudhanoti  
- Kotli  
- Bhimber  
- Mirpur  

| Legend |     |
| ------ | --- |
| Rain   |     |
| Smog   |     |

For detailed guidelines please visit NDMA website: [https://www.ndma.gov.pk/guidelines](https://www.ndma.gov.pk/guidelines)
<!-- Diagram -->
"""
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": markdown_prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{EXAMPLE_IMAGES['K6y19XCyAM7nXz8wVUyL']}"
                            }
                        }
                    ]
                },
                {
                    "role": "assistant",
                    "content": """
Page 1 of 7

F. 2 (E)/2025-NDMA (MW/ Drought Watch Alert-I)  
**Government of Pakistan**  
**Prime Minister’s Office**  
**National Disaster Management Authority (HQ)**  
Main Murree Road Near ITP Office, Islamabad  

Dated: **31 October 2025**  

Subject: **Drought Watch**  

Balochistan experiences an arid to **Semi-Arid Climate**, characterized by highly variable rainfall, extreme temperature fluctuations, and prolonged dry spells. The **Southwestern** and **Southern** parts of the province are predominantly **dry**, receiving minimal influence from the summer monsoon. Most districts in **Western** and **Southwestern Balochistan** are dominated by winter rainfall, with annual precipitation ranging between **71** and **231 mm**.  

2. Overall, Western and Southwestern Balochistan have experienced below-normal rainfall **(-79%)** during the period from May to **October 2025**. In addition, the number of consecutive dry days (CDD) has increased markedly, indicating prolonged dry spells across the region. This **significant rainfall deficit** may contribute to the development of drought conditions in these areas. The rainfall departures and corresponding consecutive dry days for these regions are summarized as follows:-  

<!-- Diagram -->

<table>
  <caption>Cumulative Departure (%) of Rainfall from May to Oct 2025 (Balochistan)</caption>
  <tr>
    <th>Stations</th>
    <th>Percentage Departure (%)</th>
  </tr>
  <tr>
    <td>PASNI</td>
    <td>-41.8</td>
  </tr>
  <tr>
    <td>TURBAT</td>
    <td>-71.7</td>
  </tr>
  <tr>
    <td>QUETTA</td>
    <td>-83.3</td>
  </tr>
  <tr>
    <td>DALBANDIN</td>
    <td>-99.7</td>
  </tr>
  <tr>
    <td>NOKKUNDI</td>
    <td>-99.8</td>
  </tr>
  <tr>
    <td>JIWANI</td>
    <td>-100.0</td>
  </tr>
  <tr>
    <td>PANJGUR</td>
    <td>-100.0</td>
  </tr>
  <tr>
    <td>BALOCHISTAN</td>
    <td>-79.0</td>
  </tr>
</table>
Figure-1(a) Percentage Departure (%)

<table>
  <caption>Consecutive Dry Days from 21.01.2025 to 27-10-2025 (Balochistan)</caption>
  <tr>
    <th>Stations</th>
    <th>No. of Days</th>
  </tr>
  <tr>
    <td>PASNI</td>
    <td>47</td>
  </tr>
  <tr>
    <td>TURBAT</td>
    <td>68</td>
  </tr>
  <tr>
    <td>QUETTA</td>
    <td>70</td>
  </tr>
  <tr>
    <td>DALBANDIN</td>
    <td>242</td>
  </tr>
  <tr>
    <td>NOKKUNDI</td>
    <td>230</td>
  </tr>
  <tr>
    <td>JIWANI</td>
    <td>281</td>
  </tr>
  <tr>
    <td>PANJGUR</td>
    <td>201</td>
  </tr>
</table>
Figure-1(b) Consecutive Dry Days

<!-- Diagram -->
"""
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": markdown_prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{EXAMPLE_IMAGES['UUMqxsp0XrFeQmUWc1Xo']}"
                            }
                        }
                    ]
                },
                {
                    "role": "assistant",
                    "content": """
# HEATWAVE ALERT
June 18th to June 22nd, 2025

<!-- Diagram -->
**Air Pressure**

**Legend**  
- Provincial Boundary  
- District Boundary  
- Heat Index Value  
  - High: 41.01  
  - Low: 0.77  
<!-- Diagram -->

## FORECAST
- A heatwave spell is expected in the mentioned districts from **18th June, 2025** to **22nd June, 2025** with the Heat index likely to soar above 41°C.

## EXPOSED DISTRICTS
<table>
  <tr>
    <td>Turbat Feels Like 49°-50°C</td>
    <td>Peshawar Feels Like 43°-44°C</td>
    <td>Khairpur Feels Like 48°-50°C</td>
    <td>Multan Feels Like 45°-46°C</td>
  </tr>
  <tr>
    <td>Dadu Feels Like 47°-48°C</td>
    <td>Bannu Feels Like 44°-45°C</td>
    <td>Lahore Feels Like 44°-46°C</td>
    <td>Bahawalpur Feels Like 50°-52°C</td>
  </tr>
  <tr>
    <td>Mohenjo-Daro Feels Like 47°-48°C</td>
    <td>Karachi Feels Like 45°-46°C</td>
    <td>Rahimyar Khan Feels Like 48°-50°C</td>
    <td>D.I. Khan Feels Like 44°-45°C</td>
  </tr>
  <tr>
    <td>Malir Feels Like 44°-45°C</td>
    <td>Sibi Feels Like 46°-47°C</td>
    <td>Sargodha Feels Like 44°-45°C</td>
    <td>Jacobabad Feels Like 48°-49°C</td>
  </tr>
  <tr>
    <td>Korangi Feels Like 44°-46°C</td>
    <td>Gotki Feels Like 50°-52°C</td>
    <td>Faisalabad Feels Like 43°-44°C</td>
    <td>Lodhran Feels Like 46°-47°C</td>
  </tr>
</table>

## ESSENTIAL HEATWAVE PRECAUTIONS
- Drink plenty of water and other fluids to stay hydrated, especially during outdoor activities.
- Try to avoid outdoor activities during the hottest part of the day (11am-4pm).
- Check on vulnerable individuals, such as the elderly and children, to ensure their safety and well-being.
"""
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": markdown_prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            }
                        }
                    ]
                },
            ]

def json_messages(markdown: str):
    return [
                {
                    "role": "system",
                    "content": """You are a disaster alert extraction specialist. 
                    Your task is to convert unstructured disaster alert documents into structured JSON following the CAP (Common Alerting Protocol) schema.
                    Extract all relevant information accurately, inferring values when explicitly stated. 
                    Use "Unknown" for urgency/severity only when truly indeterminate. Expand any place name abbreviations to their standard full form."""
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": markdown_prompt.replace("{{text}}", 
                                   """<!-- Page 1 -->
                                  Page 1 of 10

                                  **MOST IMMEDIATE / BY FAX**

                                  F.2 (E)/2024-NDMA (MW/ Special Advisory)
                                  **Government of Pakistan**
                                  **Prime Minister’s Office**
                                  **National Disaster Management Authority (HQ)**
                                  Main Murree Road Near ITP Office, Islamabad

                                  Dated: 15 August 2024

                                  Subject: **Heavy Rainfall-Wind / Thundershowers with Occasional Gaps from 16 August to 20 August 2024**  

                                  A low-pressure weather system presently producing rains in **upper parts** is likely to move southward bringing **strong monsoon currents** from Arabian sea to southern parts of the country from **16 August 2024** and this weather system is likely to persist in parts of country till **20 August 2024**. Under the influence of this weather system, **torrential rains** are also expected in **Balochistan** and **Sindh** from 16 August to 18 August. Under the said weather system following are the likely precipitation maps:

                                  <!-- Diagram -->
                                  ### Scattered Heavy Rainfall-Wind / Thundershowers with Occasional Gaps from 16 Aug to 20 Aug 2024

                                  **Punjab 16-20 Aug 2024**
                                  - Rawalpindi
                                  - Murree
                                  - Attock
                                  - Chakwal
                                  - Jhelum
                                  - Mandi Bahauddin
                                  - Gujrat
                                  - Gujranwala
                                  - Hafizabad
                                  - Wazirabad
                                  - Sahiwal
                                  - Jhang
                                  - T.T. Singh
                                  - Nankana Sahib
                                  - Chiniot
                                  - Faisalabad
                                  - Lahore
                                  - Sheikhupura
                                  - Sialkot
                                  - Narowal
                                  - Okara
                                  - Pakpattan
                                  - Kasur
                                  - Khushab
                                  - Sargodha
                                  - Bhakkar
                                  - Mianwali

                                  **ICT 16-20 Aug 2024**
                                  - Islamabad

                                  **Punjab 18-17 Aug 2024**
                                  - Bahawalpur
                                  - Bahawalnagar
                                  - D.G. Khan
                                  - Vehari
                                  - Multan
                                  - Khanewal
                                  - Lodhran
                                  - Muzaffargarh
                                  - Kot Addu
                                  - Rajanpur
                                  - R.Y. Khan
                                  - Layyah

                                  **Legend**
                                  - High
                                  - Moderate
                                  - Low
                                  <!-- Diagram -->

                                  <!-- Page 2 -->
                                  Page 2 of 10

                                  # Scattered Heavy Rainfall-Wind / Thundershowers with Occasional Gaps from 16 Aug to 20 Aug 2024

                                  <!-- Diagram -->
                                  **Khyber Pakhtunkhwa**
                                  - Dir
                                  - Swat
                                  - Kohistan
                                  - Malakand
                                  - Bajaur
                                  - Mohmand
                                  - Khyber
                                  - Mansehra
                                  - Abbottabad
                                  - Galyat
                                  - Haripur
                                  - Peshawar
                                  - Swabi
                                  - Nowshera
                                  - Mardan
                                  - Charsadda
                                  - Hangu
                                  - Kurram
                                  - Orakzai
                                  - Waziristan
                                  - Bannu
                                  - LakkiMarwat
                                  - DI Khan
                                  - Shangla
                                  - Battagram
                                  - Torghar
                                  - Tank

                                  **Legend**
                                  - High
                                  - Moderate
                                  - Low
                                  <!-- Diagram -->

                                  # Few Heavy Rainfall-Wind / Thundershowers with Occasional Gaps from 16 Aug to 20 Aug 2024

                                  <!-- Diagram -->
                                  **Gilgit Baltistan**
                                  16 to 18 Aug
                                  - Astore
                                  - Diamer
                                  - Ghanche
                                  - Gilgit
                                  - Shigar
                                  - Skardu

                                  **State of AJ&K**
                                  16 to 20 Aug
                                  - Bagh
                                  - Bhimber
                                  - Hattian
                                  - Haveli
                                  - Kotli
                                  - Mirpur
                                  - Poonch
                                  - Rawalakot
                                  - Neelum
                                  - Muzaffarabad

                                  **Legend**
                                  - High
                                  - Moderate
                                  - Low
                                  - No Rain
                                  <!-- Diagram -->

                                  <!-- Page 3 -->
                                  Page 3 of 10

                                  ## Rainfall-Wind / Thundershowers with Occasional Gaps and Few Heavy Falls from 16 Aug to 18 Aug 2024

                                  <!-- Diagram -->
                                  ### Sindh
                                  - Sukkur
                                  - Shikarpur
                                  - Kashmore
                                  - Khairpur
                                  - N-Feroze
                                  - Larkana
                                  - Dadu
                                  - Jacobabad
                                  - Karachi
                                  - Hyderabad
                                  - Thatta
                                  - Badin
                                  - T-Allahyar
                                  - T-M Khan
                                  - Tharparkar
                                  - Miti
                                  - Mirpur Khas
                                  - Umarkot
                                  - Sanghar

                                  **Legend**
                                  - High
                                  - Moderate
                                  - Low
                                  - No Rain
                                  <!-- Diagram -->

                                  ## Isolated Heavy Rainfall-Wind / Thundershowers with Occasional Gaps from 15 Aug to 18 Aug 2024

                                  <!-- Diagram -->
                                  ### Balochistan
                                  - Sibi
                                  - Harnai
                                  - Ziarat
                                  - Kohlu
                                  - Barkhan
                                  - Dera Bugti
                                  - Zhob
                                  - Musa Khel
                                  - Naseerabad
                                  - Jhal Magsi
                                  - Sohbatpur
                                  - Khuzdar
                                  - Kalat
                                  - Awaran
                                  - Gwadar
                                  - Lasbella
                                  - Loralai
                                  - Quetta
                                  - Sherani
                                  - K-Abdullah
                                  - K-Saifullah
                                  - Mastung
                                  - Harnai
                                  - Jaffarabad

                                  **Legend**
                                  - High
                                  - Moderate
                                  - Low
                                  - No Rain
                                  <!-- Diagram -->

                                  <!-- Page 4 -->
                                  Page 4 of 10

                                  2. Under the influence of this weather system, following are likely impacts:

                                  ### a. Punjab / Sindh / Islamabad Capital Territory
                                  1. Hill torrents may be triggered in D.G. Khan and Rajanpur.
                                  2. Rainfall with chances of heavy falls may generate flash / urban flooding in municipalities / local nullahs / streams and river tributaries.
                                  3. Windstorms may damage crops, loose structures, etc.
                                  4. Thunderstorms to increase risk of lightning strikes.
                                  5. Electricity / other utility services may get disrupted.
                                  6. General public is advised to be aware of loose structures like billboards, electrical poles, solar panels, hoardings, etc.

                                  ### b. KP, Galiyat, Murree, GB and State of AJ&K
                                  1. Rainfall may trigger landslides, mudslides or falling boulders potentially disrupting roads during this period in Upper Khyber Pakhtunkhwa, Galiyat, Murree, Gilgit Baltistan and State of AJ&K.
                                  2. Electricity / other utility services may get disrupted.
                                  3. Heavy Rainfall may generate flash flooding in local nullahs / streams and river tributaries.
                                  4. Windstorms may damage crops, loose structures, etc.
                                  5. Thunderstorms to increase risk of lightning strikes.
                                  6. General public is advised to be aware of loose structures like billboards, electrical poles, solar panels, hoardings, etc.
                                  7. Tourists are advised to remain cautious during the spell and check weather updates before traveling.

                                  ### c. Balochistan
                                  1. Rainfall may cause flash flooding in local nullahs.
                                  2. Hill torrents may be triggered in Sulaiman and the Kirthar Ranges.
                                  3. Landslides / mudslides may lead to potential road blockages.
                                  4. Windstorms may damage crops, loose structures, etc.
                                  5. Thunderstorms to increase risk of lightning strikes.
                                  6. Electricity / other utility services may get disrupted.
                                  7. General public is advised to be aware of loose structures like billboards, electrical poles, solar panels, hoardings, etc.

                                  8. In this regard, all concerned Federal Ministries / Departments, respective Provincial Governments, their line departments including PDMAs / GBDMA / SDMA 
                                  / ICT Administration, DDMAs/ local administrations, municipal authorities of major metropolises are advised to ensure following along with any other measures deemed necessary:

                                  ### a. Aspects for Mass Awareness / Enforcement

                                  <!-- Page 5 -->
                                  ## Page 5 of 10

                                  1. During thunderstorms and to avoid **lightning strike** do not do the following:-
                                      (a) Do not stand close to **telephone or electric pylons**.
                                      (b) Do not use landline telephones and any metal / wiring **that is not grounded**.
                                      (c) Do not take cover under trees.
                                      (d) Move away from **drainage canals and pondages**.
                                      (e) Move **indoors** or seek shelter in a dry place.

                                  2. Travellers / tourists **are advised** to:-
                                      (a) Plan travels to picnic and tourist spots considering weather and traffic conditions.
                                      (b) Properly dispose of garbage at designated areas to prevent clogging of drainage systems.
                                      (c) **Avoid overcrowding** picnic and tourist spots and ensure personal safety.
                                      (d) Keep children away from nullahs / potholes / drainage lines to avoid accidents.
                                      (e) Wear weather appropriate clothing.
                                      (f) Keep adequate supply of clean drinking water.

                                  3. Do not risk crossing any drain or road overtopping with water flow. Wait for flows to normalise and prioritise / ensure safety.

                                  4. Do not risk entering a ponded under-construction road.

                                  5. Do not take / allow children close to ponds / stagnant water, water drainage lines or any place where potholes are present.

                                  6. Sensitise all concerned on risks posed by venturing into water channels and crossing nullahs during flash floods.

                                  7. Do not handle / repair any electrical equipment, especially with exposed lines to preclude risk of electrocution during rainfall / thunderstorms and water pondage.

                                  8. Avoid staying in weak structures. In case of intense rain, seek shelter in safe places such as schools, government buildings, or any concrete buildings. 

                                  ### b. DDMAs / Local Administrations / DM Responders

                                  1. **Stoke pile** up to three weeks supply that includes ration, fuel and medicine at likely **choke points** / landslide vulnerable areas.

                                  2. Activation and deputation of duty staff for **round-the-clock monitoring** through Emergency Operation Centres (EOCs).

                                  3. Collect and share the **latest information** with line departments, provincial, and national authorities.

                                  <!-- Page 6 -->
                                  ## Page 6 of 10

                                  4. Disseminate advisories, alerts, and guidelines to all concerned.
                                  5. Generate Situation Reports (SITREPs) to cover any major incidents / developments.
                                  6. Civic Agencies and Rescue Services (1122 / Fire Brigade / Ambulance / Civil Defence) to remain alert and have sufficient emergency response personnel and equipment during the forecasted holiday period.
                                  7. Alert masses living in low-lying areas to exercise extra caution and activate community-based alert systems.
                                  8. Limit the number of tourists allowed entry to picnic and tourist spots to avoid overcrowding.
                                  9. Regulate traffic at picnic and tourist spots to ensure a smooth flow and prevent congestion.
                                  10. Provision of POL for backup generators at water pumping stations and timely pre-placement of dewatering pumps to respond to urban flooding in cities.   
                                  11. Secure loose structures including billboards / hoardings / solar panels from effects of windstorms / thundershowers.
                                  12. Under advised of local administration and LEAs, restrict seasonal nullah crossings.

                                  ### PDMAs / SDMA / GBDMA / ICT Administration

                                  1. Coordinate with respective PDMAs to align local efforts with provincial strategies and guidelines.
                                  2. Activate / ensure staffing of HR in EOCs for effective coordination and response.
                                  3. Establish a streamlined and efficient communication channel to ensure timely dissemination of weather forecasts, advisories, and alerts to local administrations and the public.
                                  4. Ensure flow of information among all stakeholders is accurate, timely, and effectively coordinated.
                                  5. Ensure enforcement / dissemination of mitigative / preparedness / response guidelines to all concerned.
                                  6. Ensure pre-placement of heavy earth moving machinery at chokepoints / at-risk regions for managing landslides and restoration of roads.
                                  7. Coordinate with Local Administrations / Line Departments to proactively provide necessary resources / HR and support during emergency situations.        

                                  <!-- Page 7 -->
                                  Page 7 of 10

                                  (8) Ensure adequate stocking of resources / machinery / relief within provincial and district capacities. Additionally, ensure availability of resources specific to ongoing seasonal hazards.

                                  (9) Conduct detailed risk / impact / vulnerability assessments at UC to District level and tailor disaster response mechanisms accordingly.

                                  (10) Maintain a comprehensive database of vulnerable populations and critical infrastructure within the jurisdiction.

                                  (11) Ensure rapid damage and needs assessments follow major incidents.

                                  **d. Federal Ministries / Departments**

                                  (1) Ensuring interagency coordination and information sharing for monitoring and handling emergencies.

                                  (2) Raise mass awareness through respective platforms relevant stakeholders about seasonal hazards.

                                  (3) Direct LEAs, NH&MP and line departments to regulate traffic flow, advised travellers / tourists regarding likely situations / dangers and safety measures.

                                  (4) Issue necessary instructions to departments, such as NHA, FWO and C&W for immediate restoration of roads in case of any blockage / obstruction / closures and preplacing of necessary emergency equipment at vulnerable / strategic locations.

                                  (5) Ensure strict and proactive monitoring of the movement around/ in close vicinity of nullahs and water channels to avert possibilities of drowning.      

                                  4. In case of any eventuality, twice-daily updates be shared with NDMA.

                                  5. With the request for wider circulation and public awareness.

                                  *(Hammad Sadiq Rana)*
                                  **Director (Response)**
                                  Tel No: 051-9030924
                                  Fax No: 051-9030729

                                  Distribution List is Attached Below

                                  <!-- Page 8 -->
                                  Page 8 of 10

                                  # DISTRIBUTION LIST

                                  **To:**
                                  - Secretary, Ministry of Interior, Islamabad
                                  - Secretary, Ministry of National Health Services, Regulation & Coordination, Islamabad
                                  - Secretary, Ministry of Information & Broadcasting, Islamabad
                                  - Secretary, Ministry of Climate Change, Islamabad
                                  - Secretary, Ministry of Communications, Islamabad
                                  - Secretary, Ministry of Water Resources, Islamabad
                                  - Secretary, Ministry of National Food Security & Research, Islamabad
                                  - Secretary, Ministry of Energy, Islamabad
                                  - Secretary, Aviation Division, Islamabad
                                  - Chief Secretary, Government of Balochistan, Quetta
                                  - Chief Secretary, Government of Khyber Pakhtunkhwa, Peshawar
                                  - Chief Secretary, Government of Punjab, Lahore
                                  - Chief Secretary, Government of Sindh, Karachi
                                  - Chief Secretary, Government of Gilgit Baltistan, Gilgit
                                  - Chief Secretary, State of AJ&K, Muzaffarabad
                                  - Director General, Pakistan Meteorological Department, Islamabad
                                  - Director General, Pakistan Civil Aviation Authority, Karachi
                                  - Chairman, Federal Flood Commission (FFC), Islamabad
                                  - Chairman, National Highway Authority (NHA), Islamabad
                                  - Chairman, WAPDA, Lahore
                                  - General Manager, Tarbela Dam Authority
                                  - General Manager, Mangla Dam Authority
                                  - Director General, PDMA Balochistan, Quetta
                                  - Director General, PDMA Khyber Pakhtunkhwa, Peshawar
                                  - Director General, PDMA Punjab, Lahore
                                  - Director General, PDMA Sindh, Karachi
                                  - Director General, GBDMA, Gilgit
                                  - Director General, SDMA AJ&K, Muzaffarabad
                                  - Director General, Rescue 1122 Balochistan, Quetta
                                  - Director General, Rescue 1122 Khyber Pakhtunkhwa, Peshawar
                                  - Director General, Rescue 1122 Punjab, Lahore
                                  - Director General, Rescue 1122 Sindh, Karachi
                                  - Director General, Rescue 1122 Gilgit Baltistan, Gilgit
                                  - Director General, Rescue 1122 AJ&K, Muzaffarabad
                                  - Chief Commissioner, Islamabad Capital Territory
                                  - Deputy Commissioner, Islamabad Capital Territory
                                  - Principal Information Officer, Press Information Department, Islamabad
                                  - Headquarters, Frontier Works Organization (FWO), Rawalpindi
                                  - Headquarters, National Highways & Motorway Police, Islamabad
                                  - Headquarters, National Electric Power Regulatory Authority, Islamabad
                                  - Headquarters, National Transmission & Dispatch Company (NTDC), Islamabad
                                  - Headquarters, Pakistan Railways, Lahore

                                  **Cc:**
                                  - Secretary to Prime Minister, Prime Minister’s Office, Islamabad
                                  - Secretary, Cabinet Division, Islamabad
                                  - Joint Crises Management Cell, Joint Staff Headquarters, Chaklala Cantt
                                  - Military Operations Directorate (MO-4), General Headquarters, Rawalpindi Cantt
                                  - ACNS (Operations), Naval Headquarters, Islamabad
                                  - ACAS (Operations), Air Headquarters, Islamabad
                                  - Headquarters, Pakistan Maritime Security Agency (PMSA), Karachi
                                  - Headquarters, Pakistan Coast Guards (PCG), Karachi

                                  <!-- Page 9 -->
                                  # PMD Press Release
                                  **Government of Pakistan**
                                  Ministry of Aviation (Aviation Division)
                                  **Pakistan Meteorological Department**
                                  Sector H-8/2, Islamabad.

                                  **Tel:** 051-9250364
                                  **Fax:** 051-9250368

                                  **NWF C-5(10)A1/2017/89**
                                  *Weather Advisory:*

                                  **Date:** 15th August, 2024
                                  **Time:** 16:30 PST

                                  **Tortential rains expected in Balochistan and Sindh from 16th to 18th August 2024 (with occasional gaps)**
                                  **Rainfalls will continue in upper parts till 20th August 2024 (with occasional gaps)**

                                  Met office informed that low pressure weather system presently producing rains in upper parts is likely to move southward bringing strong monsoon currents from Arabian sea to southern parts of the country from 16th evening. Under the influence of this weather system:

                                  **Balochistan:** Rain-wind/thunderstorm (with isolated heavy falls) is expected in Sibbi, Harnai, Ziarat, Kohlu, Barkhan, Dera Bugti, Zhob, Musa Khel, Naseerabad, Usta Muhammad, Jhal Magsi, Sohbatpur, Jaffarabad, Kalat, Skardur, Awaran, Kech, Panjgur, Gwadar (Levani, Pasni, Gwadar, Ornara), Hub and Lasbella. Loralai, Quetta, Sherani, Qila Saifullah, Qila Abdullah, Zhob, Loralai, Musakhel and Ziarat from 16th to 19th August with occasional gaps.

                                  **Sindh:** Rain-wind/thunderstorm (with few heavy falls) is expected in Sukkur, Shikarpur, Kashmore, Khipro, Nasirabad, Larkana, Dadu, Jacobabad, Karachi, Hyderabad, Thatta, Badin, Tando Allahyar, Tando Muhammad Khan, Tharparkar, Mithi, Mirpur Khas, Umarkot and Sanghar from 16th to 18th August with occasional gaps.

                                  **Kashmir:** Rain-wind/thunderstorm (with few heavy falls) are expected in Kashmir (Neelum valley, Muzaffarabad, Rawalakot, Poonch, Hattian, Bagh, Haveli, Sudhanoti, Kotli, Bhimbher) from 16th to 20th August with occasional gaps.

                                  Rain-wind/thunderstorm (with scattered heavy falls) is expected in Islamabad/Rawalpindi, Gujrat, Sialkot, Narowal, Lahore, Sheikhupura, Kasur, Okara, Pakpattan, Sahiwal, Khanewal, Vehari, Bahawalnagar, Bahawalpur, Rahimyar Khan, Dera Ghazi Khan, Multan, Layyah, Bhakkar, Mianwali, and Faisalabad from 16th to 20th August.

                                  Rain-wind/thunderstorm (with isolated heavy falls) is expected in Khyber Pakhtunkhwa (Dir, Swat, Kohistan, Shangla, Battagram, Buner, Kohat, Bannu, Mohmand, Khyber, Mansehra, Abbottabad, Haripur, Peshawar, Swabi, Nowshera, Mardan, Charsadda, Hangu, Karak, Lakki Marwat and Dera Ismail Khan) from 16th to 20th August with occasional gaps.

                                  Rain-wind/thunderstorm is expected in Gilgit-Baltistan (Diamir, Astore, Skardu, Gilgit, Ghanche, Shigar) from 16th to 18th August with occasional gaps.     

                                  ## Possible Impacts and advice:
                                  - Low lying areas inundation/Urban flooding in Balochistan and Sindh.
                                  - Torrential rains may generate Landlides/Flash Flooding in local nullahs/streams of KP, Gilgit-Baltistan, Kashmir and south Punjab.
                                  - Heavy downpour may cause water logging/Urban flooding in low lying areas of Karachi, Hyderabad, Peshawar, Lahore, Gujranwala, Faisalabad, Rawalpindi and Islamabad during the period.
                                  - Heavy downpour may cause landslides in hilly areas of Kashmir, Gilgit-Baltistan, Khyber Pakhtunkhwa and Galliyat.
                                  - Heavy downpours may damage loose structures like roof/walls of Kacha houses, electric poles, bill boards, vehicles, cause disruptions in the roads and solar panels etc during the period.
                                  - Travellers and tourists are advised to remain cautious and avoid unnecessary traveling to hilly areas and avoid any undertaking during the spell.

                                  **Note:** All concerned authorities are advised to remain **"ALERT"** and take necessary measures to avoid any untoward situation during the spell.

                                  For latest weather updates please visit: [https://www.pmd.gov.pk/en/](https://www.pmd.gov.pk/en/)

                                  **Spokesperson**
                                  Ph: 051-9250363-4

                                  **Distributions:**
                                  1. MS to PM, Islamabad
                                  2. Secretary Defence, Ministry of Defence Rawalpindi
                                  3. Chief Sec Punjab, KP, GB, Kashmir, Balochistan & Sindh
                                  4. Secretary Irrigation Punjab, KP, GB, Kashmir, Balochistan & Sindh
                                  5. Secretary Agriculture Punjab, KP, GB, Kashmir, Balochistan & Sindh
                                  6. Chairman NDMA
                                  7. Chairman NHA
                                  8. IG Motorways
                                  9. DG’s PDMA & SDMA
                                  10. Secretary Health, MOCC & Water Resources.
                                  11. Secretary National Food Security and Research
                                  12. Chairman FFC & IRSA
                                  13. Director to Minister for MOCC
                                  14. Chief Commissioner Islamabad
                                  15. Commissioner Rawalpindi
                                  16. Rescue 1122.
                                  17. Directors RMC’s & Electronic and Print Media.

                                  <!-- Page 10 -->
                                  Page 10 of 10

                                  **Government of Pakistan**
                                  Ministry of Aviation (Aviation Division)
                                  **Pakistan Meteorological Department**
                                  Sector H-8/2, Islamabad.

                                  NWFC-5(10A)/2017/89

                                  **Date:** 15th August, 2024
                                  **Time:** 16:30 PST
                                  """)
                        }
                    ]
                },
                {
                    "role": "assistant",
                    "content": [
                        {
                            "type": "text",
                            "text": 
                            """{
                                "category": "Met",
                                "event": "Heavy Monsoon Rainfall",
                                "urgency": "Expected",
                                "severity": "Severe",
                                "description": "A strong monsoon weather system will bring heavy to torrential rainfall, thunderstorms, and strong winds across Pakistan from August 16-20, 2024. Balochistan and Sindh will experience the most intense rainfall from August 16-18. The system will cause flash flooding in low-lying areas, urban flooding in major cities, landslides in mountainous regions, and hill torrents in vulnerable areas. Lightning strikes, windstorms, and disruption to utilities are expected.",
                                "instruction": "Avoid unnecessary travel, especially to hilly areas. Stay indoors during thunderstorms and away from trees, electric poles, and water channels. Do not cross flooded roads or enter ponded areas. Keep children away from drains and water bodies. Secure loose structures and avoid handling electrical equipment during rain. Stock emergency supplies including food, water, and medicine. Monitor weather updates and follow local authority guidance.",
                                "effective_from": "2024-08-15T19:00:00Z",
                                "effective_until": "2024-08-20T18:59:00Z",
                                "areas": [
                                  {
                                    "place_names": ["Rawalpindi", "Murree", "Attock", "Chakwal", "Jhelum", "Mandi Bahauddin", "Gujrat", "Gujranwala", "Hafizabad", "Wazirabad", "Sahiwal", "Jhang", "Toba Tek Singh", "Nankana Sahib", "Chiniot", "Faisalabad", "Lahore", "Sheikhupura", "Sialkot", "Narowal", "Okara", "Pakpattan", "Kasur", "Khushab", "Sargodha", "Bhakkar", "Mianwali"],
                                    "specific_effective_from": null,
                                    "specific_effective_until": null,
                                    "specific_urgency": null,
                                    "specific_severity": null,
                                    "specific_instruction": null
                                  },
                                  {
                                    "place_names": ["Bahawalpur", "Bahawalnagar", "Dera Ghazi Khan", "Vehari", "Multan", "Khanewal", "Lodhran", "Muzaffargarh", "Kot Addu", "Rajanpur", "Rahimyar Khan", "Layyah"],
                                    "specific_effective_from": "2024-08-15T19:00:00Z",
                                    "specific_effective_until": "2024-08-17T18:59:00Z",
                                    "specific_urgency": null,
                                    "specific_severity": null,
                                    "specific_instruction": "Hill torrents are expected in Dera Ghazi Khan and Rajanpur. Evacuate low-lying areas near hill torrents immediately."
                                  },
                                  {
                                    "place_names": ["Islamabad"],
                                    "specific_effective_from": null,
                                    "specific_effective_until": null,
                                    "specific_urgency": null,
                                    "specific_severity": null,
                                    "specific_instruction": "Expect urban flooding in low-lying areas. Avoid unnecessary travel during peak rainfall periods."
                                  },
                                  {
                                    "place_names": ["Dir", "Swat", "Kohistan", "Malakand", "Bajaur", "Mohmand", "Khyber", "Mansehra", "Abbottabad", "Galiyat", "Haripur", "Peshawar", "Swabi", "Nowshera", "Mardan", "Charsadda", "Hangu", "Kurram", "Orakzai", "Waziristan", "Bannu", "Lakki Marwat", "Dera Ismail Khan", "Shangla", "Battagram", "Torghar", "Tank"],
                                    "specific_effective_from": null,
                                    "specific_effective_until": null,
                                    "specific_urgency": null,
                                    "specific_severity": null,
                                    "specific_instruction": "Landslides and mudslides expected on mountain roads. Avoid travel to mountainous areas. Tourists should check weather before traveling."
                                  },
                                  {
                                    "place_names": ["Astore", "Diamer", "Ghanche", "Gilgit", "Shigar", "Skardu"],
                                    "specific_effective_from": "2024-08-15T19:00:00Z",
                                    "specific_effective_until": "2024-08-17T18:59:00Z",
                                    "specific_urgency": null,
                                    "specific_severity": "Moderate",
                                    "specific_instruction": "Landslides expected. Road blockages likely. Avoid unnecessary travel to high-altitude areas."
                                  },
                                  {
                                    "place_names": ["Bagh", "Bhimber", "Hattian", "Haveli", "Kotli", "Mirpur", "Poonch", "Rawalakot", "Neelum", "Muzaffarabad"],
                                    "specific_effective_from": null,
                                    "specific_effective_until": null,
                                    "specific_urgency": null,
                                    "specific_severity": null,
                                    "specific_instruction": "Flash flooding in streams and landslides expected. Tourists should exercise extreme caution."
                                  },
                                  {
                                    "place_names": ["Sukkur", "Shikarpur", "Kashmore", "Khairpur", "Naushahro Feroze", "Larkana", "Dadu", "Jacobabad", "Karachi", "Hyderabad", "Thatta", "Badin", "Tando Allahyar", "Tando Muhammad Khan", "Tharparkar", "Mithi", "Mirpur Khas", "Umarkot", "Sanghar"],
                                    "specific_effective_from": "2024-08-15T19:00:00Z",
                                    "specific_effective_until": "2024-08-17T18:59:00Z",
                                    "specific_urgency": null,
                                    "specific_severity": "Severe",
                                    "specific_instruction": "Torrential rains expected. High risk of urban flooding in Karachi and Hyderabad. Stay away from low-lying areas and nullahs."
                                  },
                                  {
                                    "place_names": ["Sibi", "Harnai", "Ziarat", "Kohlu", "Barkhan", "Dera Bugti", "Zhob", "Musa Khel", "Naseerabad", "Jhal Magsi", "Sohbatpur", "Khuzdar", "Kalat", "Awaran", "Gwadar", "Lasbella", "Loralai", "Quetta", "Sherani", "Qila Abdullah", "Qila Saifullah", "Mastung", "Jaffarabad"],
                                    "specific_effective_from": "2024-08-14T19:00:00Z",
                                    "specific_effective_until": "2024-08-17T18:59:00Z",
                                    "specific_urgency": null,
                                    "specific_severity": "Severe",
                                    "specific_instruction": "Torrential rains expected. Hill torrents likely in Sulaiman and Kirthar Ranges. Flash flooding in nullahs expected. Evacuate vulnerable areas immediately."
                                  }
                                ]
                              }"""
                        },
                    ]
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": markdown_prompt.replace("{{text}}","""
                              <!-- Page 1 -->
                              # **LANDSLIDE ADVISORY!**
                              **(8th April, 2024 to 15th April, 2024)**

                              ## **ANTICIPATED EXPOSURE**

                              | Risk Level           | Number of Towns | Infrastructure (km) | Roads (km) | Population |
                              | -------------------- | --------------- | ------------------- | ---------- | ---------- |
                              | Very High Risk Zones | 18              | 12,319              | 1014.95    | 7.1 Mn     |
                              | High Risk Zones      | 19              | 16,323              | 1431.99    | 7.3 Mn     |
                              | Medium Risk Zones    | 15              | 11,043              | 1424.71    | 6.1 Mn     |
                              | Low Risk Zones       | 23              | 15,555              | 1955.12    | 8.6 Mn     |

                              ## **LIKELY EXPOSED AREAS**
                              **Khyber Pakhtunkhwa**
                              - Chitral
                              - Battagram
                              - Torghar
                              - Swat
                              - Mansehra
                              - Kohistan
                              - Hunza
                              - Gilgit
                              - Skardu
                              - Nagar
                              - Muzaffarabad (AJ&K)
                              - Haveli (AJ&K)
                              - Balochistan
                              - Sherani
                              - Zhob
                              - Killah Saifullah
                              - Lorali
                              - Shangla
                              - Khber
                              - Abbottabad
                              - Ghanche
                              - Diamir
                              - Bhattian
                              - Musakhel
                              - Ziarat

                              **Gilgit-Baltistan**

                              ## **Landslide Vulnerable Zones**
                              <!-- Diagram -->
                              **Map of Pakistan with color-coded landslide risk zones:**
                              - **Hotspots 080424**
                              - **Landslide_Zonation**
                                - Low Risk Zone
                                - Medium Risk Zone
                                - High Risk Zone
                                - Very High Risk Zone
                              <!-- Diagram -->

                              ## **FORECAST**
                              - Reference to National Disaster Management Authority (NDMA), Dated 08-15 April, 2024, Heavy rainfall is expected in Gilgit-Baltistan, Khyber Pakhtunkhwa, Kashmir and in Balochistan from 08-15 April, 2024.
                              - As heavy to moderate rain may persist for some days, localized landslides may occur in very high to moderate risk zones (shown through Probable Landslide 
                              Areas (Hotspots080424)).
                              - Karakuram Highway along Hunza (approx 83kms), at Nagar (approx 49kms), at Gilgit (approx 42kms), at Diamir (approx 90kms), at Kohistan (approx 127kms), at Battagram (approx 44kms), at Mansehra (approx 44.6kms), at Abbottabad (approx 32.9kms) is at high risk of landslide.

                              ## **IMMEDIATE ACTION**
                              - It is advised to watch of Landslides, Slope failures, Rock falls and Ground Subsidence in high vulnerable zones (encircled) in map, avoid unnecessary travel.
                              - PDMAs, Rescue Services, Armed Forces and leading NGOs / CSOs to ensure availability of personnel / equipment in the indicated areas and be on stand-by for rapid response in case of any forecasted adverse weather systems.
                              - Stay updated on weather & roads condition through social media and local news.
                              """)
                        }
                      ]
                },
                {
                    "role": "assistant",
                    "content": [
                        {
                            "type": "text",
                            "text": """
                              {
                                "category": "Geo",
                                "event": "Landslide Warning",
                                "urgency": "Expected",
                                "severity": "Severe",
                                "description": "Heavy to moderate rainfall expected from April 8-15, 2024 will trigger landslides, slope failures, rockfalls, and ground subsidence across mountainous regions of Pakistan. The Karakoram Highway faces high risk of blockage, particularly in Hunza, Nagar, Gilgit, Diamer, Kohistan, Battagram, Mansehra, and Abbottabad sections. Over 29 million people and 2,400 km of roads are in medium to very high risk zones.",
                                "instruction": "Avoid unnecessary travel to mountainous areas. Stay away from steep slopes and cliffs during rainfall. Monitor weather and road conditions through local news and social media. Emergency services should maintain standby personnel and equipment in vulnerable areas for rapid response.",
                                "effective_from": "2024-04-07T19:00:00Z",
                                "effective_until": "2024-04-15T18:59:00Z",
                                "areas": [
                                  {
                                    "place_names": ["Chitral", "Swat", "Mansehra", "Kohistan", "Abbottabad", "Battagram", "Torghar", "Shangla", "Khyber", "Hunza", "Gilgit", "Skardu", "Nagar", "Ghanche", "Diamer", "Muzaffarabad", "Hattian"],
                                    "specific_effective_from": null,
                                    "specific_effective_until": null,
                                    "specific_urgency": "Immediate",
                                    "specific_severity": "Extreme",
                                    "specific_instruction": "Extreme landslide danger. Evacuate areas below unstable slopes immediately. Karakoram Highway sections at critical risk: Hunza (83 km), Nagar (49 km), Gilgit (42 km), Diamer (90 km), Kohistan (127 km), Battagram (44 km), Mansehra (45 km), Abbottabad (33 km). Avoid all travel on these routes during rainfall."
                                  },
                                  {
                                    "place_names": ["Haveli", "Sherani", "Zhob", "Qila Saifullah", "Loralai", "Musakhel", "Ziarat"],
                                    "specific_effective_from": null,
                                    "specific_effective_until": null,
                                    "specific_urgency": null,
                                    "specific_severity": "Severe",
                                    "specific_instruction": "High landslide risk. Watch for falling rocks and unstable slopes. Restrict travel during peak rainfall periods. Emergency teams on standby."
                                  },
                                  {
                                    "place_names": ["Medium Risk Zones - 15 towns across Khyber Pakhtunkhwa, Gilgit-Baltistan, Azad Jammu and Kashmir, and Balochistan"],
                                    "specific_effective_from": null,
                                    "specific_effective_until": null,
                                    "specific_urgency": null,
                                    "specific_severity": "Moderate",
                                    "specific_instruction": "Moderate landslide risk. Exercise caution on mountain roads. Avoid camping or parking near cliffs during rain."
                                  },
                                  {
                                    "place_names": ["Low Risk Zones - 23 towns across affected provinces"],
                                    "specific_effective_from": null,
                                    "specific_effective_until": null,
                                    "specific_urgency": "Expected",
                                    "specific_severity": "Minor",
                                    "specific_instruction": "Low landslide risk. Stay alert for weather updates and follow local authority guidance."
                                  }
                                ]
                              }"""
                        }
                      ]
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": markdown_prompt.replace("{{text}}","""<!-- Page 1 -->
                              # NDMA EXECUTIVE UPDATE – WINTER HAZARDS (15 Dec 2023)

                              <!-- Diagram -->
                              ![NDMA Rainfall Forecast (15 to 22 Dec, 2023)](Image showing rainfall forecast map)  
                              **NDMA Rainfall Forecast (15 to 22 Dec, 2023)**  
                              *Expected Precipitation: Isolated Precipitation / Cloudiness, No Precipitation*      
                              <!-- Diagram -->

                              <!-- Diagram -->
                              ![NDMA Snow Forecast (15 to 22 Dec, 2023)](Image showing snow forecast map)          
                              **NDMA Snow Forecast (15 to 22 Dec, 2023)**  
                              *Snowfall areas marked*
                              <!-- Diagram -->

                              <!-- Diagram -->
                              ![NDMA AQI Forecast (15 to 22 Dec, 2023)](Image showing AQI forecast map)  
                              **NDMA AQI Forecast (15 to 22 Dec, 2023)**
                              *AQI Scale: Good (0-50), Moderate (51-100), Unhealthy (101-150), Unhealthy for Sensitive Groups (151-200), Very Unhealthy (201-300), Hazardous (301-500)*   
                              <!-- Diagram -->

                              ## TOP RAIN / SNOW RECORDED LAST 24 HOURS (MM)
                              - Balochistan: Yes
                              - Khyber Pakhtunkhwa: Nil
                              - Punjab: Nil
                              - Sindh: Nil
                              - Gilgit-Baltistan: Nil
                              - State of AJ&K: Nil
                              - Islamabad Capital Territory: Nil

                              <!-- Diagram -->
                              ![Affected Roads by Fog/Smog (15 to 22 Dec, 2023)](Image showing roads affected by fog/smog)
                              **Affected Roads by Fog/Smog (15 to 22 Dec, 2023)**
                              *Roads marked in red and blue lines indicating affected routes*
                              <!-- Diagram -->

                              <!-- Diagram -->
                              ![Impact of Rain/Snow (15 to 22 Dec, 2023)](Image showing expected impact map)
                              **Impact of Rain/Snow (15 to 22 Dec, 2023)**
                              *Expected Impact: Low Impact, No Impact*
                              <!-- Diagram -->

                              <!-- Page 2 -->
                              ### **FORECASTED IMPACTS**
                              - No adverse weather systems expected during this week (8 - 15 Dec 23)

                              ### **WEATHER FOR NEXT 24 hours**
                              - **Balochistan:** Mainly dry weather while cold temperature conditions will persist in all parts of the province, Light Snow is expected in North-western of the Balochistan.
                              - **Khyber Pakhtunkhwa:** Cloudy weather along with isolated rainfall is expected in most areas. Moreover, cold temperature conditions with Fog during morning and night times is likely to persist in all parts of the province.
                              - **Punjab:** Cloudy weather along with isolated rainfall, while Fog/Smog conditions will persist during morning and night times in parts of the province.  
                              - **Sindh:** Dry weather with cool nights and foggy / misty mornings are expected to prevail over the province.
                              - **Gilgit Baltistan:** Cold weather is expected with light snow and rainfall at high elevated areas of the province.
                              - **State of AJ&K:** Cold weather with Cloudiness and isolated rainfall/snow in most parts of province.
                              - **Islamabad Capital Territory:** Cold and partly cloudy weather is likely to persist along with isolated rainfall.

                              ### **GUIDANCE ISSUED**
                              - PDMAs to undertake regular public awareness on all media channels / social media to maximise general public's knowledge on risks associated with winter season; colder temperatures, freezing rain, snowfall, fog, smog, etc.
                              - NHA / FWO / Local C&W Depts to ensure pre-placement of machinery and timely clearance of snow from roads / highways.
                              - Rescue Services, Armed Forces and leading NGOs / CSOs to ensure availability of personnel / equipment in the indicated areas & be on stand-by for rapid response in case of any forecasted adverse weather systems.

                              <!-- Diagram -->

                              ### **WEATHER OUTLOOK – TOURIST LOCATIONS – NEXT 7 DAYS**

                              | Locations     | Isolated Thunderstorm/Rain / Snowfall | Temperature (°C) |
                              |---------------|---------------------------------------|------------------|
                              | Murree        | Light Snow                            | -2 to 8          |
                              | Gallyat       | Snow                                  | -5 to 5          |
                              | Naran         | Snow                                  | -7 to 5          |
                              | Kaghan        | Snow                                  | -5 to 7          |
                              | MalamJabba    | Snow                                  | 4 to 9           |
                              | Kalam         | Snow                                  | -9 to 3          |
                              | Neelum        | Snow                                  | -9 to 4          |
                              | Naltar Valley | Snow                                  | -11 to 3         |
                              | Rattu         | Snow                                  | -8 to 1          |
                              | Skardu        | Snow                                  | -11 to 3         |

                              ### **Low Visibility Advisory**
                              - Drive cautiously on roads (M1, M2, M3, M4, M5 and M11) and link roads affected by fog/smog. Maintain a safe following distance and reduce speed to adapt to limited visibility.
                              - Avoid High Beams because they can reflect off fog/smog particles, worsening visibility. Stick to low beams instead. Use fog lights to improve visibility close to the ground.
                              - Stay tuned to weather updates and be aware of any changes in visibility conditions during your journey.

                              ### **TOURIST ADVISORY**
                              - Tourists visiting areas susceptible to snow are advised to remain vigilant as light snow is expected in the region.
                              - Tourists visiting northern areas of Pakistan are recommended to remain alert, as light snow, coupled with rainfall.
                              - Tourists should be prepared for chilly temperatures, particularly during the evenings and early mornings while visiting Northern Areas of Pakistan including Gilgit Baltistan, AJ&K & Upper parts of KPK.

                              <!-- Diagram -->
                              """)
                        }
                      ]
                },
                {
                    "role": "assistant",
                    "content": [
                        {
                            "type": "text",
                            "text": """
                              {
                                "category": "Met",
                                "event": "Winter Weather Advisory",
                                "urgency": "Expected",
                                "severity": "Moderate",
                                "description": "Light to moderate snow expected in northern mountainous regions including Gilgit-Baltistan, Azad Jammu and Kashmir, and upper Khyber Pakhtunkhwa from December 15-22, 2023. Dense fog and smog will reduce visibility on major motorways (M1, M2, M3, M4, M5, M11) during morning and night hours. Cold temperatures will persist across the country with freezing conditions in high-altitude areas. Air quality may reach unhealthy levels in some urban areas. Overall impact expected to be low with no major adverse weather systems forecast.",
                                "instruction": "Drive slowly on foggy motorways and maintain safe following distance. Use low beam headlights and fog lights - avoid high beams. Monitor weather updates before travel. Tourists visiting northern areas should prepare for snow and freezing temperatures, especially during evenings and early mornings. Avoid unnecessary travel to snow-affected mountain areas without proper equipment and preparation.",
                                "effective_from": "2023-12-14T19:00:00Z",
                                "effective_until": "2023-12-22T18:59:00Z",
                                "areas": [
                                  {
                                    "place_names": ["Murree", "Galiyat", "Naran", "Kaghan", "Malam Jabba", "Kalam", "Neelum", "Naltar Valley", "Rattu", "Skardu"],
                                    "specific_effective_from": null,
                                    "specific_effective_until": null,
                                    "specific_urgency": null,
                                    "specific_severity": "Moderate",
                                    "specific_instruction": "Snow expected with temperatures ranging from -11°C to 9°C. Tourist locations will experience freezing conditions. Carry warm clothing, emergency supplies, and check road conditions before travel. Roads may become slippery or blocked."
                                  },
                                  {
                                    "place_names": ["Gilgit-Baltistan"],
                                    "specific_effective_from": null,
                                    "specific_effective_until": null,
                                    "specific_urgency": null,
                                    "specific_severity": "Moderate",
                                    "specific_instruction": "Cold weather with light snow and rainfall at high elevations. Roads may experience temporary blockages."
                                  },
                                  {
                                    "place_names": ["Azad Jammu and Kashmir"],
                                    "specific_effective_from": null,
                                    "specific_effective_until": null,
                                    "specific_urgency": null,
                                    "specific_severity": "Moderate",
                                    "specific_instruction": "Cold weather with cloudiness and isolated rainfall or snow. Be prepared for slippery road conditions in elevated areas."
                                  },
                                  {
                                    "place_names": ["Northern Khyber Pakhtunkhwa", "Dir", "Swat", "Chitral", "Kohistan", "Malakand"],
                                    "specific_effective_from": null,
                                    "specific_effective_until": null,
                                    "specific_urgency": null,
                                    "specific_severity": "Moderate",
                                    "specific_instruction": "Cloudy weather with isolated rainfall. Cold temperatures with fog during morning and night. Snow possible at higher elevations."
                                  },
                                  {
                                    "place_names": ["Punjab", "Lahore", "Faisalabad", "Multan", "Rawalpindi"],
                                    "specific_effective_from": null,
                                    "specific_effective_until": null,
                                    "specific_urgency": null,
                                    "specific_severity": "Moderate",
                                    "specific_instruction": "Dense fog and smog during morning and night will severely reduce visibility on motorways. Drive with extreme caution, use low beams and fog lights, and avoid high speeds. Consider delaying travel during peak fog hours."
                                  },
                                  {
                                    "place_names": ["Islamabad"],
                                    "specific_effective_from": null,
                                    "specific_effective_until": null,
                                    "specific_urgency": null,
                                    "specific_severity": "Minor",
                                    "specific_instruction": "Cold and partly cloudy weather with isolated rainfall possible. Monitor conditions if traveling to nearby mountainous areas."
                                  },
                                  {
                                    "place_names": ["Sindh", "Karachi", "Hyderabad"],
                                    "specific_effective_from": null,
                                    "specific_effective_until": null,
                                    "specific_urgency": null,
                                    "specific_severity": "Minor",
                                    "specific_instruction": "Dry weather with cool nights and foggy or misty mornings. Reduce speed during morning commute due to reduced visibility."
                                  },
                                  {
                                    "place_names": ["Northwestern Balochistan", "Quetta", "Ziarat"],
                                    "specific_effective_from": null,
                                    "specific_effective_until": null,
                                    "specific_urgency": null,
                                    "specific_severity": "Minor",
                                    "specific_instruction": "Mainly dry weather with cold temperatures. Light snow possible in northwestern areas. Prepare for cold conditions."
                                  }
                                ]
                              }"""
                        }
                      ]
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": markdown_prompt.replace("{{text}}", markdown)
                        }
                    ]
                }
            ]