import requests
from bs4 import BeautifulSoup
import csv

# Danh sách các URL của các trang sách cần quét
urls = [
    'https://books.toscrape.com/catalogue/category/books_1/page-1.html',
    # 'https://books.toscrape.com/catalogue/category/books_1/page-2.html',
    # 'https://books.toscrape.com/catalogue/category/books_1/page-3.html',
    # 'https://books.toscrape.com/catalogue/category/books_1/page-4.html',
    # 'https://books.toscrape.com/catalogue/category/books_1/page-5.html',
    # 'https://books.toscrape.com/catalogue/category/books_1/page-6.html',
    # 'https://books.toscrape.com/catalogue/category/books_1/page-7.html',
    # 'https://books.toscrape.com/catalogue/category/books_1/page-8.html',
    # 'https://books.toscrape.com/catalogue/category/books_1/page-9.html',
    # 'https://books.toscrape.com/catalogue/category/books_1/page-10.html',
    # 'https://books.toscrape.com/catalogue/category/books_1/page-11.html',
    # 'https://books.toscrape.com/catalogue/category/books_1/page-12.html',
    # 'https://books.toscrape.com/catalogue/category/books_1/page-13.html',
    # 'https://books.toscrape.com/catalogue/category/books_1/page-14.html',
    # 'https://books.toscrape.com/catalogue/category/books_1/page-15.html',
    # 'https://books.toscrape.com/catalogue/category/books_1/page-16.html',
    # 'https://books.toscrape.com/catalogue/category/books_1/page-17.html',
    # 'https://books.toscrape.com/catalogue/category/books_1/page-18.html',
    # 'https://books.toscrape.com/catalogue/category/books_1/page-19.html',
    # 'https://books.toscrape.com/catalogue/category/books_1/page-20.html',
    # 'https://books.toscrape.com/catalogue/category/books_1/page-21.html',
    # 'https://books.toscrape.com/catalogue/category/books_1/page-22.html',
    # 'https://books.toscrape.com/catalogue/category/books_1/page-23.html',
    # 'https://books.toscrape.com/catalogue/category/books_1/page-24.html',
    # 'https://books.toscrape.com/catalogue/category/books_1/page-25.html',
    # 'https://books.toscrape.com/catalogue/category/books_1/page-26.html',
    # 'https://books.toscrape.com/catalogue/category/books_1/page-27.html',
    # 'https://books.toscrape.com/catalogue/category/books_1/page-28.html',
    # 'https://books.toscrape.com/catalogue/category/books_1/page-29.html',
    # 'https://books.toscrape.com/catalogue/category/books_1/page-30.html',
    # 'https://books.toscrape.com/catalogue/category/books_1/page-31.html',
    # 'https://books.toscrape.com/catalogue/category/books_1/page-32.html',
    # 'https://books.toscrape.com/catalogue/category/books_1/page-33.html',
    # 'https://books.toscrape.com/catalogue/category/books_1/page-34.html',
    # 'https://books.toscrape.com/catalogue/category/books_1/page-35.html',
    # 'https://books.toscrape.com/catalogue/category/books_1/page-36.html',
    # 'https://books.toscrape.com/catalogue/category/books_1/page-37.html',
    # 'https://books.toscrape.com/catalogue/category/books_1/page-38.html',
    # 'https://books.toscrape.com/catalogue/category/books_1/page-39.html',
    # 'https://books.toscrape.com/catalogue/category/books_1/page-40.html',
    # 'https://books.toscrape.com/catalogue/category/books_1/page-41.html',
    # 'https://books.toscrape.com/catalogue/category/books_1/page-42.html',
    # 'https://books.toscrape.com/catalogue/category/books_1/page-43.html',
    # 'https://books.toscrape.com/catalogue/category/books_1/page-44.html',
    # 'https://books.toscrape.com/catalogue/category/books_1/page-45.html',
    # 'https://books.toscrape.com/catalogue/category/books_1/page-46.html',
    # 'https://books.toscrape.com/catalogue/category/books_1/page-47.html',
    # 'https://books.toscrape.com/catalogue/category/books_1/page-48.html',
    # 'https://books.toscrape.com/catalogue/category/books_1/page-49.html',
    # 'https://books.toscrape.com/catalogue/category/books_1/page-50.html',
    # Thêm các URL khác vào đây
]

base_url = 'https://books.toscrape.com/'
exchange_rate = 3000  # Giả định tỷ giá 1 GBP = 30,000 VND

# Danh sách lưu thông tin sách từ tất cả các URL
all_books = []

# Lặp qua từng URL để quét dữ liệu
for url in urls:
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')

    for item in soup.find_all('article', class_='product_pod'):
        title = item.find('h3').find('a')['title']  # Lấy tiêu đề sách từ thẻ <a> trong <h3>
        price_text = item.find('p', class_='price_color').text  # Lấy giá từ thẻ <p> có class 'price_color'
        
        # Lọc lấy giá trị số từ giá và chuyển đổi sang VND
        price_gbp = float(price_text.replace('Â£', ''))
        price_vnd = price_gbp * exchange_rate

        # Lấy URL hình ảnh từ thẻ <img> trong thẻ <article>
        img_url = item.find('img')['src']
        full_img_url = base_url + img_url.replace('../', '')  # Chuyển đổi thành URL đầy đủ
        
        # Lưu thông tin sách vào danh sách
        all_books.append({
            'Title': title,
            'Price (VND)': f'{price_vnd:,.0f} VND',  # Định dạng giá VND với dấu phẩy
            'Image URL': full_img_url
        })

# Ghi tất cả dữ liệu vào file CSV
with open('all_books.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['Title', 'Price (VND)', 'Image URL'])
    writer.writeheader()  # Ghi dòng tiêu đề
    writer.writerows(all_books)  # Ghi dữ liệu tất cả các sách

print("Dữ liệu đã được ghi vào file all_books.csv")
