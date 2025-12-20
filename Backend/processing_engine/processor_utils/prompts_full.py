from PIL import Image
from pathlib import Path
from processing_engine.processor_utils.doc_utils import to_base64

CURRENT_DIR = Path(__file__).parent
markdown_prompt = """Extract all text from this image in markdown format. 
Preserve the structure, headings, lists, tables, diagrams and formatting as much as possible. 
Return only the English markdown without any preamble. Format tables as markdown or html.
Wrap contents from inside a diagram in a "<!-- Diagram -->" comment.
"""

# Pre-load example images at module initialization
EXAMPLE_IMAGES = {
    "9PPqpSasTb07UWPKiyXV": to_base64(Image.open(CURRENT_DIR / "examples/9PPqpSasTb07UWPKiyXV.jpg")),
    "cX5UVWicUxYs0Ub9642D": to_base64(Image.open(CURRENT_DIR / "examples/cX5UVWicUxYs0Ub9642D.jpg")),
    "evgtuouxcEBpD4FSxL9w": to_base64(Image.open(CURRENT_DIR / "examples/evgtuouxcEBpD4FSxL9w.jpg")),
    "InXkmGJqQbCXx7aRyjXA": to_base64(Image.open(CURRENT_DIR / "examples/InXkmGJqQbCXx7aRyjXA.jpg")),
    "K6y19XCyAM7nXz8wVUyL": to_base64(Image.open(CURRENT_DIR / "examples/K6y19XCyAM7nXz8wVUyL.jpg")),
    "UUMqxsp0XrFeQmUWc1Xo": to_base64(Image.open(CURRENT_DIR / "examples/UUMqxsp0XrFeQmUWc1Xo.jpg")),
    "WMpJfGUze00GwXezWekr": to_base64(Image.open(CURRENT_DIR / "examples/WMpJfGUze00GwXezWekr.jpg")),
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
                                "url": f"data:image/jpeg;base64,{EXAMPLE_IMAGES['9PPqpSasTb07UWPKiyXV']}"
                            }
                        }
                    ]
                },
                {
                    "role": "assistant",
                    "content": """
# Weather Advisory (24th to 29th September, 2025) 
## National Emergency Operation Centre – National Disaster Management Authority

A weak westerly wave is expected to bring partly cloudy weather along with isolated light rainfall over northern parts of the country from 25th to 26th of September, 2025.

### Punjab: 
Mostly hot and dry weather is expected in all parts of the province from 24th to 29th of Sep. 2025. However, partly cloudy weather along with isolated light rainfall is expected in Pothohar region including Islamabad, Rawalpindi, Chakwal, Jhelum, Attock and surrounding areas on 25th of Sep, 2025.

### Balochistan:
Mostly hot and dry weather is expected in all parts of the province from 24th to 29th of September, 2025.

### Sindh: 
Mostly hot and dry weather is expected in all parts of the province from 24th to 29th of September, 2025.

### KP: 
Mostly hot and dry weather is expected during this week. However, Partly cloudy weather along with isolated rainfall is expected in Chitral, Dir, Swat, Malakand, Buner, Mansehra, Abbottabad, Haripur, Swabi, Nowshera, Peshawar and surrounding areas from 25th to 26th of Sep, 2025.

### GB & AJK: 
Mostly dry weather is expected during this week. However, Partly cloudy weather along with isolated rainfall is expected in Astore, Skardu, Hunza, Bagh, Haveli, Rawalakot, Neelum Valley, Muzaffarabad from 25th to 26th of Sep, 2025.
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
                                "url": f"data:image/jpeg;base64,{EXAMPLE_IMAGES['InXkmGJqQbCXx7aRyjXA']}"
                            }
                        }
                    ]
                },
                {
                    "role": "assistant",
                    "content": """
# **SMOG ADVISORY⚠️**  
November, 2025

## **Forecast**

Smog, a mixture of smoke and fog, Moderate to Dense smog is expected across major cities in Punjab from November, due to calm winds and dry stable weather conditions. Areas most affected may include **Lahore, Gujranwala, Sheikhupura, Kasur, Nankana Sahib, Faisalabad, Multan, Bahawalpur, Rahim Yar Khan, and Bahawalnagar**.

### **Possible Impacts**
- Poor air quality may cause breathing difficulties, cough, and eye irritation, especially in children, the elderly, and those with health conditions.
- Reduced visibility could disrupt travel and increase the risk of road accidents.

### **Precaution Measures**
- Limit outdoor exposure and wear a mask when going outside.
- Avoid early morning and late-night travel when smog is heaviest.
- Keep windows closed and use air purifiers or filters indoors if available.
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
                                "url": f"data:image/jpeg;base64,{EXAMPLE_IMAGES['WMpJfGUze00GwXezWekr']}"
                            }
                        }
                    ]
                },
                {
                    "role": "assistant",
                    "content": """
Page 5 of 6
***Annex-A***

<!-- Diagram -->
# GLOF Sites

**Map Labels (GLOF Sites):**
- Rabat Glacier
- Darkhot Glacier
- Sardar Gol Glacier
- Yarkhun Lusht Glacier
- Ishkoman Glacier
- karam ber Glacier
- Badswat glacier
- Passu Glacier
- Ultar Glacier
- Gulmit Glacier
- Gulkin Glacier
- Yazghil Glacier
- Brep Glacier
- Booni Glacier
- Mushi bar Glacier
- Hundur Galcier
- Hinarchi Glacier bagrote
- Tersat Hundur Gl.
- Yeshkuk Glaicer
- Boq Glacier
- Sonoghor Glacier
- Reshun Glacier
- Mian Koh Glacier 1&2
- Dir Gole Glacier Arkary
- Thalu II
- Thalu I
- Garum Chashma Glacier
- Chianter Glacier
- Chateboi Glacier

**Legend**
- 🔵 GLOF Sites
- **—** District Boundary

**Scale:** 0 - 20 - 40 - 80 - 120 km

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
                                "url": f"data:image/png;base64,{base64_image}"
                            }
                        }
                    ]
                },
            ]