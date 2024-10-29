import requests
from bs4 import BeautifulSoup
import csv
import time

# Đọc danh sách URL từ file txt
with open('urls.txt', 'r') as file:
    urls = [line.strip() for line in file if line.strip() and not line.startswith('#')]  # Đọc và loại bỏ dòng trống và dòng chú thích

# Thêm User-Agent để tránh bị chặn
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
}

# Hàm để crawl thông tin sách từ một URL
def crawl_books(url):
    books = []
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    for item in soup.find_all('div', class_='product-item'):
        book_info = {}
        
        title_tag = item.find('h3', class_='pro-name')
        if title_tag:
            title = title_tag.text.strip()
            detail_url = "https://www.vinabook.com" + title_tag.find('a')['href']
            
            # Gửi yêu cầu đến trang chi tiết của sách
            detail_response = requests.get(detail_url, headers=headers)
            detail_soup = BeautifulSoup(detail_response.text, 'html.parser')

            for row in detail_soup.find_all('tr'):
                header = row.find('th').text.strip() if row.find('th') else None
                value = row.find('td').text.strip() if row.find('td') else None
                
                if header and value:
                    book_info[header] = value

            price = detail_soup.select_one('span.pro-price').text.strip() if detail_soup.select_one('span.pro-price') else 'N/A'
            description = detail_soup.select_one('div.product-description').text.strip() if detail_soup.select_one('div.product-description') else 'N/A'
            image_url = detail_soup.find('img', {'class': 'product-image-feature'})['src'] if detail_soup.find('img', {'class': 'product-image-feature'}) else 'N/A'
            
            if image_url.startswith("//"):
                image_url = "https:" + image_url
            elif image_url.startswith("/"):
                image_url = "https://www.vinabook.com" + image_url
            
            books.append({
                'Title': title,
                'Author': book_info.get("Tác giả"),
                'Price': price,
                'Language': book_info.get("Ngôn Ngữ"),
                'Weight': book_info.get("Trọng lượng (gr)"),
                'Publisher': book_info.get("NXB"),
                'Publish Year': book_info.get("Năm XB"),
                'Description': description,
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

# Ghi từng danh mục vào file CSV riêng
for collection_name, books in all_books.items():
    csv_file_name = f"{collection_name}.csv"
    with open(csv_file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['Title', 'Author', 'Price', 'Language', 'Publish Year', 'Publisher', 'Weight', 'Description', 'Image URL', 'Detail URL'])
        writer.writeheader()
        writer.writerows(books)

    print(f"Dữ liệu đã được ghi vào file {csv_file_name}")
