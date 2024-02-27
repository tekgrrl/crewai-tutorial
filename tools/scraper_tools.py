import requests
from bs4 import BeautifulSoup
from langchain.tools import tool

class ScraperTools():
    
    @tool("Scraper Tool")
    def scrape(url: str):
        "Useful tool to scrape a website content, use to learn more about a given URL."

        headers = "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            # Parse the HTML content of the webpage
            soup = BeautifulSoup(response.content, 'html.parser')
        
           # Find all elements that are likely to contain text
            text_elements = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li'])

            all_text = []
            for element in text_elements:
                text = element.get_text(separator=' ', strip=True)
                if text:
                    all_text.append(text)

            #combine all text into one string
            combined_text = '\n '.join(all_text)
            return combined_text  
        else:
            print("Failed to retrieve the webpage")
            
        
        