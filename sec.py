import requests

# Use a placeholder for the API key
api_key = 'e07f5d6cd8dfbdb46d55166dd2f207de6bad35bcc056940de8974e5303f7c15e'

def fetch_sec_filings(ticker):
    url = f"https://api.sec-api.io?token={api_key}"
    query = {
        "query": {"query_string": {"query": f"ticker:{ticker} AND formType:\"10-K\""}},
        "from": "0",
        "size": "1",
        "sort": [{"filedAt": {"order": "desc"}}]
    }
    try:
        response = requests.post(url, json=query, timeout=10)
        if response.status_code == 200:
            filings = response.json()
            if filings['filings']:
                link_to_txt = filings['filings'][0].get('linkToTxt')
                if link_to_txt:
                    text_response = requests.get(link_to_txt, timeout=10)
                    if text_response.status_code == 200:
                        return text_response.text
                    else:
                        return f"Unable to fetch the document. Status code: {text_response.status_code}"
                else:
                    return "No link to text document found."
            else:
                return "No filings found."
        else:
            return f"Error fetching filings. Status code: {response.status_code}"
    except requests.RequestException as e:
        return f"Request failed: {e}"