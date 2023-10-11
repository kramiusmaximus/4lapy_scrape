import requests
import csv
import logging

logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)

def fetch_items(item_ids):
    URL = f"https://api.retailrocket.ru/api/1.0/partner/5b151eb597a528b658db601e/items/?itemsIds={','.join(map(str, item_ids))}&stock=True&format=json"
    
    response = requests.get(URL)
    response.raise_for_status()
    
    items = response.json()
    
    result = []
    for item in items:
        data = {
            "ItemId": item["ItemId"],
            "Name": item["Name"],
            "Url": item["Url"],
            "Price": item["Price"] if item["OldPrice"] == 0 else item["OldPrice"],
            "PromoPrice": -1 if item["OldPrice"] == 0 else item["Price"],
            "Brand": item["Vendor"]
        }

        result.append(data)
    
    return result

def load_item_ids(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines()]

def save_to_csv(data, filename):
    keys = data[0].keys()
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)


if __name__ == '__main__':
    logger.info('Starting...')
    
    item_ids = load_item_ids('item_ids.txt')
    logger.info(f'{len(item_ids)} item_ids loaded')

    items = fetch_items(item_ids)
    logger.info(f'{len(items)} items details fetched')

    save_to_csv(items, 'items.csv')
    logger.info('Done.')
