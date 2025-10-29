import requests
import pandas as pd
import math
from scrapy import Selector
import os
import csv


# Create main directories if they don't exist
os.makedirs('book_data', exist_ok=True)
os.makedirs('book_images', exist_ok=True)

# Dictionary to track CSV files and writers for each category
category_files = {}
category_writers = {}


i = 1

while i < 51 :

    url_pages = "https://books.toscrape.com/catalogue/page-"+str(i)+".html"


    url = "https://books.toscrape.com"
    response = requests.get(url_pages)


    sel = Selector(text=response.text)
    articles = sel.css("article.product_pod")


    for article in articles :    
        title = article.css("h3 a::text").get()
        price = article.css("div.product_price p.price_color::text").get()
        stock = article.css("div.product_price p.availability::text")[1].get()
        image = article.css("div.image_container img::attr(src)").get()
        product = article.css("div.image_container a::attr(href)").get()
        


        url_second_page = (url+"/catalogue/"+product)
        response2 = requests.get(url_second_page)
        sel2 = Selector(text=response2.text)




        rows = sel2.css("tr")
        for row in rows[:1]:
            upc = row.css("td::text").getall()
    
        category = sel2.css("ul.breadcrumb a[href]::text")[2].get()

        # Clean category name for folder/file names
        clean_category = category.replace(" ", "_").replace("/", "_").replace("\\", "_")

        # Create category directory for images if it doesn't exist
        category_image_dir = f"book_images/{clean_category}"
        os.makedirs(category_image_dir, exist_ok=True)

         # Set up CSV file for this category if not already done
        if clean_category not in category_files:
            csv_file = open(f'book_data/{clean_category}.csv', 'w', newline='', encoding='utf-8')
            writer = csv.writer(csv_file)

        # Write header - NOW INCLUDES RATING
            writer.writerow(['Title', 'Price', 'Stock', 'UPC', 'Category', 'Rating', 'Image_Path', 'Product_URL'])
            category_files[clean_category] = csv_file
            category_writers[clean_category] = writer

        # Download image
        image_url = url + "/" + image
        image_response = requests.get(image_url)
        
        # Create image filename (using UPC for uniqueness)
        upc_str = upc[0] if upc else "unknown"
        image_filename = f"{upc_str}.jpg"
        image_path = os.path.join(category_image_dir, image_filename)
        
        # Save image
        with open(image_path, 'wb') as f:
            f.write(image_response.content)



        # Get rating - IMPROVED VERSION
        rating_class = sel2.css("p.star-rating::attr(class)").get()
        rating_text = "Unknown"
        
        if 'One' in rating_class:
            rating_text = 'One Star'
        elif 'Two' in rating_class:
            rating_text = 'Two Stars'
        elif 'Three' in rating_class:
            rating_text = 'Three Stars'
        elif 'Four' in rating_class:
            rating_text = 'Four Stars'
        elif 'Five' in rating_class:
            rating_text = 'Five Stars'


         # Write to CSV - NOW INCLUDES RATING
        writer = category_writers[clean_category]
        writer.writerow([
            title, 
            price, 
            stock, 
            upc[0] if upc else "", 
            category, 
            rating_text,  # You can use rating_text instead if you prefer text
            image_path, 
            url_second_page
        ])

    
        print(title)
        print(price)
        print(stock)
        #print(rating)
        print(url+"/"+image)
        print(url_second_page) #product
        print('UPC: '+'upc'.join(upc))
        print(category)
    
    i = i + 1

# Close all CSV files
for file in category_files.values():
    file.close()

print("Scraping completed! Check the 'book_data' and 'book_images' folders.")
