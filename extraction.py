
# === 1. FILE/LIBRARY INSTALLATION ===
# pip install pdfplumber pandas -q -U google-genai
import pdfplumber
from google import genai
import json
import logging
from pathlib import Path
import pandas as pd 
logging.getLogger("pdfminer").setLevel(logging.ERROR)
from schema import SWFReport
from pydantic import ValidationError
from google.genai.errors import ServerError

# === CONFIG === MUST MODIFY!!
GEMINI_API_KEY = "YOUR_GOOGLE_API_KEY_HERE"

# === GEMINI CLIENT ===
client = genai.Client(api_key=GEMINI_API_KEY)

# === GEMINI SYSTEM PROMPT ===
system_prompt = r"""
You are an information extractor. Output **only** strict JSON matching the schema.
Rules:
- Extract only explicitly stated info from the provided text for the specified fund. If a document contains multiple entities managed by the same institution (e.g., central bank, investment authority), extract data only for the sovereign wealth fund (SWF) that is explicitly recognized as the long-term investment vehicle for national savings, intergenerational wealth, or fiscal stabilization
- Never guess, infer, or hallucinate. Use null when missing.
- All numeric fields must be plain numbers (no % signs, commas, or units)
- Write in Standard American English with proper capitalization; translate outputs to English as appropriate. 
- Always use USD if available. 
- Do not include any text outside JSON. No comments.

Field notes:
- `fund_name.value`: "complete fund name (abbreviation)".
- `reporting_period.value`: "YYYY" for calendar year, or "YYYY\\YYYY", use only one forward slash for fiscal year.
- `reporting_period.clarification`: "calendar year" or "fiscal year ending <Month YYYY>".
- `assets_under_management` / `management_costs`: prefer USD if available; include `currency`.
- `investment_horizon.value`: "long-term" (10+ years) | "medium-term" (2-10 years) | "short-term" (2- years).
- `metrics`: include available metrics with values and time periods; in `metric_clarification` include key information if available such as calculation method, net/gross, confidence level, benchmark used, annualized, currency, etc.
- `annual_return_percent.metric_clarification`: state return type (net or gross) and currency. Prefer returns in USD if available. 
- include all available benchmarks for `benchmark_comparison` in English; set `comparison_result` to "outperformed" | "underperformed" | "matched"
- `benchmark_comparison.comments_or_reasoning` should explain the difference (market conditions, active management decisions, etc.)
- `benchmark_comparison.time_period` should match the following format: "1y" | "3yr" | "5yr" | "10yr" | "since inception"
- do not include benchmarks that require estimation. double check benchmark figures for accuracy. make sure that the `actual_fund_return` matches the corresponding `annual_return_percent.value` for the same time period and is not confused with the `benchmark_return`
- `asset_allocation` / `investment_geography`: if ranges are explicitly given, use midpoints only and clarify in `notes`; `total_percent` is the sum of all the values
- `asset_allocation`: map to the following standarized categories: 
  equities (public, listed, developed, emerging, global, etc)| fixed income ([corporate/sovereign] bonds, treasuries, [private] credit, [investment-grade/high-yield] debt, [mbs] mortgage-backed securites, etc)| commodities (gold, precious metals, energy commodities, etc)| digital assets (cryptocurrencies, tokenized assets, etc)| alternative investments ([private/unlisted] equity, venture capital, real estate, infastructure, hedge funds, private credit, direct lending, natural resources, illiquid assets, etc)| cash 
- `investment_geography.region`: map to the following regions, use other if several regions are grouped together in data: North America | South America | Europe | Asia | Africa | Oceania | Developed | Emerging | Global | Other
- specify in `investment_geography.notes` if the geographic allocation is based on assets or physical holdings or other criteria
- `management_costs.notes`: clarify calculations and specify the type of costs included 

Output must be valid JSON and match the provided response schema exactly.
"""

# === INPUT & OUTPUT PATHS === MODIFY IF DESIRED 
downloads_path = Path.home() / "Downloads" / "FAP" / "pdfs"
# Change to where the annual report PDFs are stored

output_path = downloads_path / "individual_outputs"
output_path.mkdir(exist_ok=True)  # create the folder if it doesn't exist
# Change to desired output folder name for individual JSON outputs 


# === ITERATING THROUGH PDF FILES IN INPUT FOLDER & CALLING GEMINI API ===

pdf_files = list(downloads_path.glob("*.pdf"))

results = []

for pdf_file in pdf_files:
    result = []
    fund_name = pdf_file.stem  
    print(f"Opening {pdf_file.name}...")  
    with pdfplumber.open(pdf_file) as pdf:
        pdf_text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                pdf_text += page_text + "\n"

        response = client.models.generate_content(
            model="gemini-2.5-pro", 
            contents= f"You are extracting structured data for a sovereign wealth fund. Fund Name: {fund_name}. Only extract data related to this fund from the following report text:" + pdf_text, 
            config={"response_mime_type": "application/json",
                "response_schema": SWFReport, 
                "system_instruction": system_prompt,
                "temperature": 0.1, 
                "top_p": 1 
                # MODIFY MODEL, CONTENTS, AND CONFIG IF DESIRED
            },
        )
        try:
            data = response.parsed.model_dump()
            data["source_pdf"] = pdf_file.name  
            results.append(data)
            result.append(data)
            print(f"Extracted data from {pdf_file.name}")
            # CREATING INDIVIDUAL OUTPUT JSONS 
            with open(output_path / f"{pdf_file.stem}.json", "w") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
        except json.JSONDecodeError:
            print(f"Failed to parse JSON for {pdf_file.name}")
            continue
        
# === CREATING FINAL MERGED OUTPUT JSON  ===        
# CHANGE NAME OF FINAL RESULTS HERE IF DESIRED       
with open("final_merged_output.json", "w") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
    

