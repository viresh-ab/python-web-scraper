import streamlit as st
import requests
from bs4 import BeautifulSoup

# Title
st.title("Python Web Scraper Tool")

# Input URL
url = st.text_input("Enter URL to scrape:")

if st.button("Scrape"):
    if url:
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            response.raise_for_status()  # Raise error if status != 200
            
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Extract all links
            links = [a.get('href') for a in soup.find_all('a') if a.get('href')]
            
            st.subheader("Scraped Links:")
            for link in links:
                st.write(link)
            
            st.success(f"Found {len(links)} links on the page!")
        
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching URL: {e}")
    else:
        st.warning("Please enter a URL.")
