# FAP-Data-Extraction-Tool
The FDET project aimed to create a tool that automates the extraction of financial data from Sovereign Wealth Fund (SWF) annual reports, standardizes the information, allowing for easy benchmarking for el Fundo de Ahorro de Panamá’s (FAP) performance against peer funds.

It was developed in Python to support FAP’s research and reporting needs.

---

## Features
extraction.py: 
- Takes input PDFs of SWF annual reports
- Extracts the text from the PDFs
- Utilizes Gemini's API to extract the desired data

schema.py: 
- Provides a framework for the output of extraction.py 
- Gaurds against hallucination

conversion.py: 
- Takes the final_merged_output of all of the individual JSON files and transforms into CSV files for easy analysis and graphing

---

## Requirements  
- Python 3.10 or later
- Libraries listed in `requirements.txt`

---

## Installation
1. Install [Python](https://www.python.org/downloads/).  
2. Open this folder in **Visual Studio Code** (or another Python editor).  
3. In the terminal, install required libraries:
   ```bash
   pip install -r requirements.txt

---

## Configuration 

For extraction.py:
1. Create/locate your Gemini API Key 
	- For Gemini, go to Google AI Studio to get API Key
	- Paste in API Key (line 17)
	- It is possible to use any desired Generative AI Model with an API, but the 	code (setting up the "client", formatting of the "response", etc) will just 	need to be changed accordingly 
2. Download desired annual reports in PDF form and rename so that their full fund name is in the title (i.e. "fundo_de_ahorro_de_panama_2024.pdf")
3. Create a folder to store all of the annual reports (i.e. "pdfs")
	- Paste in path to folder at "downloads_path" (i.e. / "Downloads" / "FAP" / 	"pdfs") (line 58)
4. Edit "output_path" to the desired path where a folder will be created containing all of the individual JSON files for each PDF
5. Edit the file name for the final merged JSON (line 104)


---

## Troubleshooting 
Frequent errors: 
- 429 || RESOURCE_EXHAUSTED || You've exceeded the rate limit. -> You are sending too many requests per minute with the free tier Gemini API.
	- May need to either add a timer to batch requests but simplest 		workaround is to upgrade to a paid tier, costs should be less than $2 		for one run (recommend looking into free trials or credits)
- 500 || INTERNAL || An unexpected error occurred on Google's side. -> Your input context is too long.
	- Shorten "system_prompt" or switch models to increase context window 

For more on troubleshooting visit: Gemini API Docs \ API Troubleshooting 
https://ai.google.dev/gemini-api/docs/troubleshooting 

More notes:
- Read the "system_prompt" carefully as unclear, misleading, or inaccurate instruction can cause the model to crash 
- Check the schema.py to make sure the fields are accurate


