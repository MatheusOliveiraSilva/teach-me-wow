import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from langchain_core.documents import Document

class AsyncWebFetcher:
    '''
    Fetches webpage content using Playwright, allowing JavaScript to render.
    '''
    async def fetch_page_content(self, url: str) -> str | None:
        '''
        Fetches a webpage using Playwright, allows JavaScript to render, and returns the HTML content.
        '''
        try:
            async with async_playwright() as p:
                print(f"[AsyncWebFetcher] Launching browser for URL: {url}...")
                browser = await p.chromium.launch()
                page = await browser.new_page()
                print(f"[AsyncWebFetcher] Fetching URL: {url}...")
                await page.goto(url, timeout=90000, wait_until='domcontentloaded') 
                print(f"[AsyncWebFetcher] Page DOMContentLoaded, getting content...")
                html_content = await page.content()
                await browser.close()
                print("[AsyncWebFetcher] Browser closed.")
                return html_content
        except Exception as e:
            print(f"[AsyncWebFetcher] Error fetching or rendering {url} with Playwright: {e}")
            return None

class WowheadGuideParser:
    '''
    Parses HTML content from a Wowhead guide page into Langchain Documents.
    '''
    def _clean_text(self, text: str) -> str:
        """
        Cleans the extracted text by removing unwanted UI elements, normalizing
        newlines and spaces.
        """
        import re

        # 1. Remove specific UI phrases (case-insensitive)
        text_to_remove = [
            r"Show Table of Contents",
            r"Use the ✘ markers next to selected builds and talents to populate the priority list.",
            # Add other common UI phrases you want to remove here
        ]
        for pattern in text_to_remove:
            text = re.sub(pattern, "", text, flags=re.IGNORECASE)

        # 2. Replace all line breaks (and multiple spaces around them) with a single space
        text = re.sub(r'\s*\n\s*', ' ', text)
        
        # 3. Replace multiple spaces with a single space
        text = re.sub(r'\s{2,}', ' ', text)
        
        # 4. Remove spaces at the beginning and end of the text
        text = text.strip()
        
        return text

    def parse_to_documents(self, html_content: str, url: str) -> list[Document]:
        '''
        Parses HTML content to extract relevant text and transform it into Langchain Documents.
        '''
        soup = BeautifulSoup(html_content, 'html.parser')
        documents = []
        page_title = soup.title.string if soup.title else "N/A"

        main_content_divs = soup.find_all('div', class_='text') 

        if not main_content_divs:
            print("[WowheadGuideParser] Warning: Could not find 'div.text'. Attempting to extract from body.")
            body = soup.find('body')
            if body:
                raw_text = body.get_text(separator='\n', strip=True) # get_text still useful for initial extraction
                cleaned_text = self._clean_text(raw_text)
                if cleaned_text:
                    documents.append(Document(page_content=cleaned_text, metadata={"source": url, "title": page_title}))
        else:
            print(f"[WowheadGuideParser] Found {len(main_content_divs)} 'div.text' elements. Processing them.")
            for i, content_div in enumerate(main_content_divs):
                if content_div.find(id='comments') or content_div.find_parent(id='comments'):
                    print(f"[WowheadGuideParser] Skipping div {i+1} as it seems to be a comments section.")
                    continue
                if content_div.find(id='forum-posts') or content_div.find_parent(id='forum-posts'):
                    print(f"[WowheadGuideParser] Skipping div {i+1} as it seems to be a forum posts section.")
                    continue
                
                section_title_tag = content_div.find(['h1', 'h2', 'h3'])
                section_title = section_title_tag.get_text(strip=True) if section_title_tag else f"Guide Section {i+1}"
                
                raw_text_content = content_div.get_text(separator='\n', strip=True) # Initial extraction
                cleaned_text_content = self._clean_text(raw_text_content) # Apply cleaning

                if cleaned_text_content:
                    # Re-evaluate short content filter after cleaning, as UI text has been removed
                    if len(cleaned_text_content) < 50: # Adjust the limit as needed
                        print(f"[WowheadGuideParser] Skipping div {i+1} due to very short content after cleaning: {cleaned_text_content[:50]}...")
                        continue

                    documents.append(Document(
                        page_content=cleaned_text_content,
                        metadata={"source": url, "section_title": section_title, "title": page_title}
                    ))
        
        if not documents:
            print("[WowheadGuideParser] No documents extracted. The page structure might be different or content filtered out.")

        return documents

class WowheadIngestionPipeline:
    '''
    Orchestrates the fetching and parsing of Wowhead guides.
    '''
    def __init__(self):
        self.fetcher = AsyncWebFetcher()
        self.parser = WowheadGuideParser()

    async def ingest_guide_from_url(self, url: str) -> list[Document]:
        '''
        Fetches a Wowhead guide page, parses it, and returns a list of Langchain Documents.
        '''
        print(f"[WowheadIngestionPipeline] Starting ingestion for URL: {url}")
        html_content = await self.fetcher.fetch_page_content(url)
        
        if html_content:
            print(f"[WowheadIngestionPipeline] Page content fetched. Parsing...")
            documents = self.parser.parse_to_documents(html_content, url)
            print(f"[WowheadIngestionPipeline] Extracted {len(documents)} documents from {url}.")
            return documents
        else:
            print(f"[WowheadIngestionPipeline] Failed to fetch content for {url}. Returning empty list.")
            return []

async def demonstration():
    target_url = "https://www.wowhead.com/guide/classes/shaman/elemental/rotation-cooldowns-pve-dps"
    
    pipeline = WowheadIngestionPipeline()
    documents = await pipeline.ingest_guide_from_url(target_url)
    
    for i, doc in enumerate(documents):
        print(f"--- Document {i+1} ---")
        print(f"Source: {doc.metadata.get('source')}")
        print(f"Title: {doc.metadata.get('title')}")
        print(f"Section Title: {doc.metadata.get('section_title', 'N/A')}")
        print(f"Content (preview): {doc.page_content[:300]}...") 
        print("-" * 20)

if __name__ == "__main__":
    asyncio.run(demonstration()) 