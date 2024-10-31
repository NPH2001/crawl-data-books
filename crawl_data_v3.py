import requests
from bs4 import BeautifulSoup
import csv
import time
import re

# Đọc danh sách URL từ file txt
with open('url1.txt', 'r') as file:
    urls = [line.strip() for line in file if line.strip() and not line.startswith('#')]  # Đọc và loại bỏ dòng trống và dòng chú thích

# Thêm User-Agent để tránh bị chặn
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
}

# Hàm để crawl thông tin sách từ một URL
def crawl_books(url):
    books = []
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    for item in soup.find_all('div', class_='product-item'):
        book_info = {}
        
        title_tag = item.find('h3', class_='pro-name')
        if title_tag:
            title = title_tag.text.strip()
            detail_url = "https://www.vinabook.com" + title_tag.find('a')['href']
            
            # Gửi yêu cầu đến trang chi tiết của sách
            detail_response = requests.get(detail_url, verify=False)
            detail_soup = BeautifulSoup(detail_response.text, 'html.parser')

            for row in detail_soup.find_all('tr'):
                header = row.find('th').text.strip() if row.find('th') else None
                value = row.find('td').text.strip() if row.find('td') else None
                
                if header and value:
                    book_info[header] = value

            price = detail_soup.select_one('span.pro-price').text.strip() if detail_soup.select_one('span.pro-price') else 'N/A'
            description = detail_soup.select_one('div.product-description').text.strip() if detail_soup.select_one('div.product-description') else 'N/A'
            image_url = detail_soup.find('img', {'class': 'product-image-feature'})['src'] if detail_soup.find('img', {'class': 'product-image-feature'}) else 'N/A'


            description_prettify = detail_soup.prettify()
            
            
            author_search = re.search(r'Tác giả:\s*(.+?)Nhà xuất bản:', description)
            publisher_search = re.search(r'Nhà xuất bản:\s*(.+?)Nhà phát hành:', description)
            distributor_search = re.search(r'Nhà phát hành:\s*(.+?)Mã sản phẩm:', description)
            weight_search = re.search(r'Khối lượng:\s*(.+?)gam', description)
            release_date_search = re.search(r'Ngày phát hành:\s*(\d{2}/\d{2}/\d{4})', description)
            language_search = re.search(r'Ngôn ngữ:\s*(.+)', description)
            description_cleaned_search = re.search(r'GIỚI THIỆU SÁCH(.*?)Thông tin chi tiết', description, re.DOTALL)
            if author_search:
                author = author_search.group(1).strip()
            else:
                author = "Oscar Wilde"
            
            if publisher_search:
                publisher = publisher_search.group(1).strip()
            else:
                publisher = "Văn Học"

            if weight_search:
                weight = weight_search.group(1).strip() + " gam"
            else:
                weight = "460"

            if release_date_search:
                release_date = release_date_search.group(1).strip()
            else:
                release_date = "2023"

            if language_search:
                language = language_search.group(1).strip()
            else:
                language = "Tiếng Việt"

            if description_cleaned_search:
                description_cleaned = description_cleaned_search.group(1).strip()
            else:
                description_cleaned = "null"



            
            if image_url.startswith("//"):
                image_url = "https:" + image_url
            elif image_url.startswith("/"):
                image_url = "https://www.vinabook.com" + image_url
            
            books.append({
                'Title': title,
                'Author': author,
                'Price': price,
                'Language': language,
                'Weight': weight,
                'Publisher': publisher,
                'Publish Year': release_date,
                # 'Description': description_cleaned,
                'Description': description_prettify,
                'Image URL': image_url,
                'Detail URL': detail_url
            })

            time.sleep(1)  # Tránh gửi yêu cầu quá nhanh
    return books

# Tạo một dictionary để nhóm các sách theo danh mục
all_books = {}

# Lặp qua từng URL và lưu sách vào từng danh mục tương ứng
for url in urls:
    # Trích xuất tên danh mục sau 'collections/'
    collection_name = url.split('collections/')[-1].split('?')[0]
    
    # Crawl dữ liệu sách từ URL hiện tại
    books = crawl_books(url)
    
    # Thêm sách vào danh sách của danh mục tương ứng
    if collection_name in all_books:
        all_books[collection_name].extend(books)
    else:
        all_books[collection_name] = books
    
    print(f'url success: {url}')

# Ghi từng danh mục vào file CSV riêng
for collection_name, books in all_books.items():
    csv_file_name = f"{collection_name}.csv"
    with open(csv_file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['Title', 'Author', 'Price', 'Language', 'Publish Year', 'Publisher', 'Weight', 'Description', 'Image URL', 'Detail URL'])
        writer.writeheader()
        writer.writerows(books)

    print(f"Dữ liệu đã được ghi vào file {csv_file_name}")
