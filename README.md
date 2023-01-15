## About ScrapingTool

This is a python scraping tool specifically design for extracting data from www.newegg.com.
It uses the API provided by the website with route /store/api/ to get the data from the system and stores it in CSV file.

Data points to be scraped:
* product title
* product description
* product final pricing
* product rating
* Seller name
* Main Image URL 
* Description of the product

## Prerequisites

## Usage

```Python
from neweggclient import NewEggClient
client = NewEggClient(no_of_products=500, file_name="extract_products_500")
client.extract_save_products()
```

Generated file is stored under 
```/src/scraping_tool/data_files/{file_name}.csv```



