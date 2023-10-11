import requests
from bs4 import BeautifulSoup
from typing import List
import logging
import os

logger = logging.getLogger("yeet")
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
logger.addHandler(console_handler)



def extract_values(html_data: str, field: str) -> List[str]:
    """
    Extract values of a given field from the HTML data.
    
    Parameters:
        - html_data (str): The HTML data as a string.
        - field (str): The field to extract values from.
    
    Returns:
        - List[str]: List of extracted values.
    """
    soup = BeautifulSoup(html_data, 'html.parser')
    elements_with_field = soup.find_all(attrs={field: True})
    return [element[field] for element in elements_with_field]

def get_html(url: str) -> str:
    """
    Fetch the webpage content for a given URL.
    
    Parameters:
        - url (str): The URL of the webpage.
    
    Returns:
        - str: The content of the webpage.
    """
    response = requests.get(url)
    return response.text

def get_item_ids(starting_url: str) -> List[str]:
    """
    Extract item IDs from webpages starting from the given URL.
    
    Parameters:
        - starting_url (str): The starting URL to extract item IDs from.
    
    Returns:
        - List[str]: List of extracted item IDs.
    """
    url = starting_url + '&page=1'
    html_data = get_html(url)
    item_ids = set(extract_values(html_data, 'data-offerid'))
    page = 2
    logger.info(f"Found {len(item_ids)} new item id's. Total: {len(item_ids)}")

    while True:
        url = starting_url + '&page=' + str(page)
        html_data = get_html(url)
        extracted_ids = set(extract_values(html_data, 'data-offerid'))
        new_ids = extracted_ids - item_ids
        
        if not new_ids:
            break
        
        item_ids = item_ids.union(new_ids)
        page += 1
        logger.info(f"Found {len(new_ids)} new item id's. Total: {len(item_ids)}")

    return list(item_ids)

def save_to_file(item_ids: List[str], filename: str = "../out/item_ids.txt"):
    """
    Save item IDs to a specified file.
    
    Parameters:
        - item_ids (List[str]): List of item IDs.
        - filename (str): Name of the file to save to.
    """
    with open(filename, 'w') as file:
        for item_id in item_ids:
            file.write(f"{item_id}\n")


if __name__ == '__main__':
    logger.info("Starting...")

    if not os.path.exists('../out'):
        os.makedirs('../out')

    url = 'https://4lapy.ru/catalog/sobaki/korm-sobaki/sukhoy-korm-sobaki/?section_id=166'
    item_ids = get_item_ids(url)
    save_to_file(item_ids)
    logger.info("Done.")