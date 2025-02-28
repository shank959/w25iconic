from portkey_ai import Portkey
import json
import yfinance as yf
from financials import get_financials

"""
Replace info of priviate_company with real questionnaire fields
Feel free to refine prompting
"""


# Initialize Portkey client
portkey = Portkey(
    api_key="oG2qS1nYSc7eMJeqI9k604TPmLTH",
    virtual_key="perplexity-ai-v-b38f29",
)

# Define the private company’s characteristics
private_company = {
    "revenue": "500M",  
    "ebitda_margin": "20%", 
    "growth_rate": "15%",  
    "business_description": "A SaaS company providing AI-driven data analytics solutions for financial institutions.",
    "primary_naics_code": "511210", 
    "geographic_focus": "North America"
}

# Construct the AI prompt
prompt = f"""
Given a private company with the following characteristics:
{private_company}

Please return a JSON object containing 5 most relevant public company comparables. Format the response as follows, without giving any introduction:
{{
    "comparable_companies": [
        {{
            "ticker": "[STOCK TICKER]",
            "company_name": "[FULL LEGAL NAME]",
            "selection_rationale": "[1-2 sentences on why this company is a good comparable, including business model similarity, size relevance, and growth profile]"
        }}
    ]
}}
Prioritize companies that:
1. Share similar business models and revenue streams
2. Operate in similar geographic markets
3. Have similar growth profiles
4. Are pure-play companies in the same industry


"""

completion = portkey.chat.completions.create(
    messages=[{"role": "user", "content": prompt}],
    model="sonar-pro",
    max_tokens=512
)

content = completion['choices'][0].message.content.strip()
content = content.replace("\n", "").replace("\t", "").strip()

parsed_json = json.loads(content)


comparable_companies = parsed_json.get("comparable_companies", [])
# print(comparable_companies)
list_of_company = []
for company in comparable_companies:
    print(f"Ticker: {company['ticker']}")
    list_of_company.append(company['ticker'])
    print(f"Company Name: {company['company_name']}")
    print(f"Rationale: {company['selection_rationale']}\n")

print(list_of_company)


# EXTRACT RELEVANT FINANCIAL METRICS FROM COMPARABLE COMPANY LIST
metric_list = get_financials(list_of_company)
print(metric_list)