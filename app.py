import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import BytesIO

# Title
st.title("Python Web Scraper Tool")

# Input URL
url = st.text_input("Enter URL to scrape:")

if st.button("Scrape"):
    if url:
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Extract all links with text
            links = [{"text": a.get_text(strip=True), "href": a.get('href')} 
                     for a in soup.find_all('a') if a.get('href')]
            
            if not links:
                st.warning("No links found on this page.")
            else:
                st.subheader("Scraped Links:")
                for link in links:
                    st.write(f"{link['text']} → {link['href']}")
                
                st.success(f"Found {len(links)} links on the page!")

                # Create DataFrame
                df = pd.DataFrame(links)

                # Save DataFrame to Excel in memory
                output = BytesIO()
                
                # Use XlsxWriter if available, fallback to openpyxl
                try:
                    engine = 'xlsxwriter'
                    with pd.ExcelWriter(output, engine=engine) as writer:
                        df.to_excel(writer, index=False, sheet_name='Links')
                except ModuleNotFoundError:
                    engine = 'openpyxl'
                    with pd.ExcelWriter(output, engine=engine) as writer:
                        df.to_excel(writer, index=False, sheet_name='Links')

                processed_data = output.getvalue()

                # Download button
                st.download_button(
                    label="Download Excel file",
                    data=processed_data,
                    file_name="scraped_links.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching URL: {e}")
    else:
        st.warning("Please enter a URL.")
