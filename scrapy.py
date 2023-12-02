from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd

def scrape_podcast_details(url):
    # Set up the Selenium WebDriver in headless mode
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    # Navigate to the podcast link
    driver.get(url)
    time.sleep(2)  # Add a short delay to allow content to load

    # Get the page source after waiting for dynamic content to load
    page_source = driver.page_source

    # Parsing the HTML
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find the div with class "product-header__title" for the podcast name
    title_element = soup.find('span', class_='product-header__title')

    # Find the span with class "product-header__identity" for the producer name
    producer_element = soup.find('span', class_='product-header__identity')

    # Extract and return the podcast name and producer name if found
    if title_element:
        podcast_name = title_element.text.strip()
    else:
        podcast_name = "N/A"

    if producer_element:
        producer_name = producer_element.text.strip()
    else:
        producer_name = "N/A"

    # Close the WebDriver
    driver.quit()

    return {'Podcast Name': podcast_name, 'Producer Name': producer_name, 'Podcast Link': url}

def scrape_website_with_selenium(url):
    # Set up the Selenium WebDriver in headless mode
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    # Navigate to the URL
    driver.get(url)

    # Scroll to the top of the page to ensure you capture content from the beginning
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(2)  # Add a short delay to allow content to load

    # Get the page source after waiting for dynamic content to load
    page_source = driver.page_source

    # Parsing the HTML
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find the section with the specified class
    target_section = soup.find('section', class_='section section-catalog section-pad-top initialized')

    # Check if the section is found
    if target_section:
        # Find the div with class "section-content" inside the target section
        section_content = target_section.find('div', class_='section-content')

        # Check if the section content is found
        if section_content:
            top_charts = section_content.find('div', class_='top-charts')

            if top_charts:
                # Find the ul with class 'marquee-list'
                marquee_list = top_charts.find('ul', class_='marquee-list clone')

                # Extract podcast items
                podcasts = marquee_list.find_all('li')

                # Initialize a list to store podcast details
                podcast_details_list = []

                # Extract podcast links and additional details
                for podcast in podcasts:
                    # Find the <a> tag inside each <li> and extract the 'href' attribute
                    link_tag = podcast.find('a', class_='marquee-link')
                    if link_tag:
                        podcast_link = link_tag.get('href')
                        podcast_details = scrape_podcast_details(podcast_link)
                        podcast_details_list.append(podcast_details)
                    else:
                        print("No <a> tag with class 'marquee-link' found inside the <li>.")

                    # Limit to 100 podcast links
                    if len(podcast_details_list) == 100:
                        break

                # Create a DataFrame using pandas
                df = pd.DataFrame(podcast_details_list)

                # Save the DataFrame to an Excel file
                df.to_excel('podcast_details.xlsx', index=False)
                print("Podcast details saved to 'podcast_details.xlsx'.")
            else:
                print("No div with class 'top_charts' found inside the target section.")
        else:
            print("No div with class 'section-content' found inside the target section.")
    else:
        print("No div with the specified class found.")

    # Close the WebDriver
    driver.quit()

# Example Usage:
if __name__ == "__main__":
    target_url = 'https://www.apple.com/apple-podcasts/'
    scrape_website_with_selenium(target_url)
