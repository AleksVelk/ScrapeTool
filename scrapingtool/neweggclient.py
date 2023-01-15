import csv
import logging
import math
from json.decoder import JSONDecodeError
from typing import List, Union

import requests
from requests import HTTPError

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class NewEggClient:
    IMAGE_BASE_URL = "https://c1.neweggimages.com/ProductImageCompressAll300/"
    BASE_URL = "https://www.newegg.com/store/api/GetShopAllDeals"

    QUERY_PARAMS = {
        "pageIndex": 1,
        "pageSize": 60,
        "enableSpaItem": True
    }

    FIELD_NAMES = ['product_title', 'line_description', 'bullet_description', 'product_final_price', 'product_rating',
                   'product_seller_name', 'product_image_url']

    FILE_NAME = "product_extract"

    def __init__(
            self,
            username=None,
            password=None,
            query_parameters=QUERY_PARAMS,
            url=BASE_URL,
            csv_fields=FIELD_NAMES,
            no_of_products=100,
            file_name=FILE_NAME
    ):
        self.username = username
        self.password = password
        self.query_parameters = query_parameters
        self.url = url
        self.csv_fields = csv_fields
        self.no_of_products = no_of_products
        self.file_name = file_name

    def __call_search_api(self) -> Union[None, List[dict]]:
        """
        Make a GET request to the API
        Returns: List of dictionaries returned from the API
        """
        try:
            response = requests.get(self.url, params=self.query_parameters)
            response.raise_for_status()
            return response.json().get("ItemList")
        except HTTPError as e:
            logger.exception(f"call_search_api failed with HttpError, trace: {e} ")
        except JSONDecodeError as e:
            logger.exception(f"call_search_api failed with JsonDecoreError, trace: {e}")
        except (Exception,) as e:
            logger.exception(f"call_search_api failed, trace: {e}")

    def calculate_last_page_to_extract(self) -> Union[None, int]:
        """
        Calculate the last page to be extracted based on no_of_products / page_size
        Returns: The last page to be extracted
        """
        page_size = self.query_parameters.get("pageSize")
        last_page = None
        if self.no_of_products and page_size > 0:
            last_page = math.ceil(self.no_of_products / page_size)
        return last_page

    def get_products(self) -> List[dict]:
        """
        Call the API for each page until it reach the last page
        Returns: List of all products extracted from the API
        """
        last_page = self.calculate_last_page_to_extract()
        items = []
        try:
            if last_page:
                for i in range(1, last_page):
                    self.query_parameters["pageIndex"] = i
                    response = self.__call_search_api()
                    items.extend(response)
        except (Exception,) as e:
            logger.exception(f"get_product failed, trace: {e}")
        return items

    @classmethod
    def get_items_details(cls, items: List[dict]) -> List[dict]:
        """
        Generate a list of all products with relevant data points
        Args:
            items: list of products extracted from the API
        Returns: list of products with relevant data points
        """
        results = []
        for item in items:
            product_details = {}
            if description := item.get("Description"):
                if product_title := description.get("Title"):
                    product_details["product_title"] = product_title
                if line_description := description.get("LineDescription"):
                    product_details["line_description"] = line_description
                if bullet_description := description.get("BulletDescription"):
                    product_details["bullet_description"] = bullet_description

            if product_final_price := item.get("FinalPrice"):
                product_details["product_final_price"] = product_final_price

            if product_review := item.get("Review"):
                if product_rating := product_review.get("Rating"):
                    product_details["product_rating"] = product_rating

            if product_seller := item.get("Seller"):
                if product_seller_name := product_seller.get("SellerName"):
                    product_details["product_seller_name"] = product_seller_name

            if product_image := item.get("NewImage"):
                if image_name := product_image.get("ImageName"):
                    product_image_url = cls.IMAGE_BASE_URL + image_name
                    product_details["product_image_url"] = product_image_url

            results.append(product_details)
        return results

    @classmethod
    def save_to_csv(cls, items: List[dict], file_name: str) -> None:
        """
        Save the products to csv file to the root directory of the project
        Args:
            items: list of products extracted from the API
            file_name: csv file name
        """
        try:
            with open(f'data_files/{file_name}.csv', 'w', newline='', encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=cls.FIELD_NAMES)
                writer.writeheader()
                writer.writerows(items)
                logger.info(f"Successfully write {len(items)} products to product_extract.csv")
        except (Exception,) as e:
            logger.exception(f"save_to_csv failed: trace: {e}")

    def extract_save_products(self) -> None:
        """
        Wrapper method to encapsulate all the methods calls
        """
        extracted_products = self.get_products()
        items_relevant_data = NewEggClient.get_items_details(extracted_products)
        NewEggClient.save_to_csv(items_relevant_data, self.file_name)
