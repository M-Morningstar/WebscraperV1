import pandas as pd, country_converter as coco, os, re
import getHtmlContent as getHtmlContent, Product as Product, asyncio

productList = []

def fillProducts():
    directory = '.'

    # Pattern to match directories starting with 'B' and have 10 characters
    dir_pattern = re.compile(r'^B.{9}$')
    # Pattern to match HTML files with the given naming scheme
    file_pattern = re.compile(r'^[a-z]+_[A-Z]+\.html$')

    directories = [d for d in os.listdir(directory) if os.path.isdir(d) and dir_pattern.match(d)]

    cc = coco.CountryConverter()

    for dir_name in directories:
        dir_path = os.path.join(directory, dir_name)
        # List all files in the directory
        files = os.listdir(dir_path)
        # Filter files matching the file pattern
        matchingFiles = [f for f in files if file_pattern.match(f)]

        for filename in matchingFiles:
            print(f"Retrieving Data From The Source... ({filename} in {dir_name})")
            filepath = os.path.join(dir_path, filename)
            product = Product.Product()
            product.fillProductInfo(filepath)
            productList.append(product.convertToDict())

asyncio.run(getHtmlContent.main())

fillProducts()

df = pd.DataFrame(productList)
df.to_csv('amazonProducts.csv')
print('Program finished successfuly')
