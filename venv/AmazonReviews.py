import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup
import ssl
import json
from MongoDBUtil import MongoPersist

class AmazonReview:

    def reviewWrap(self, url):

        # For ignoring SSL certificate errors
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        m = MongoPersist()
        #url='https://www.amazon.com/dp/B07DNMHBRC/ref=sspa_dk_detail_2?psc=1&pd_rd_i=B07DNMHBRC&pd_rd_wg=70Lx2&pd_rd_r=30WME7MF7PT99664YZC9&pd_rd_w=Vf2js&smid=A12LTVP7KBAA4'
       # url = 'https://www.amazon.in/OnePlus-Mirror-Black-128GB-Storage/dp/B07DJD1Y3Q/ref=sr_1_1?crid=C1MIII97CLX2&keywords=one+plus6t+mobiles&qid=1553094939&s=gateway&sprefix=one+plus%2Caps%2C1115&sr=8-1'
       # html = urllib.request.urlopen(url, context=ctx).read()
        #htmlfile = open('output_file.html','r+')
        #html = htmlfile.read()
        try:
           # url = 'https://www.amazon.in/OnePlus-Mirror-Black-128GB-Storage/dp/B07DJD1Y3Q/ref=sr_1_1?crid=C1MIII97CLX2&keywords=one+plus6t+mobiles&qid=1553094939&s=gateway&sprefix=one+plus%2Caps%2C1115&sr=8-1'
            html = urllib.request.urlopen(url, context=ctx).read()
            htmlfile = open('output_file.html','r+')
            html = htmlfile.read()
            soup = BeautifulSoup(html, 'html.parser')
        except:
            html = m.searchContent('www.Amazon.com','OnePlus 6T (Mirror Black, 6GB RAM, 128GB Storage)')
            soup = BeautifulSoup(html['htmlContent'], 'html.parser')
        #soup = BeautifulSoup(html, 'html.parser')
        #soup = BeautifulSoup(html['htmlContent'], 'html.parser')
        html = soup.prettify('utf-8')
        product_json = {}
        # This block of code will help extract the Prodcut Title of the item
        for spans in soup.findAll('span', attrs={'id': 'productTitle'}):
            name_of_product = spans.text.strip()
            product_json['name'] = name_of_product
            break
        # This block of code will help extract the price of the item in dollars
        for divs in soup.findAll('div'):
            try:
                price = str(divs['data-asin-price'])
                product_json['price'] = '$' + price
                break
            except:
                pass
        # This block of code will help extract the image of the item in dollars

        for divs in soup.findAll('div', attrs={'id': 'rwImages_hidden'}):
            for img_tag in divs.findAll('img', attrs={'style': 'display:none;'
                                        }):
                product_json['img-url'] = img_tag['src']
                break
        # This block of code will help extract the average star rating of the product
        for i_tags in soup.findAll('i',
                                   attrs={'data-hook': 'average-star-rating'}):
            for spans in i_tags.findAll('span', attrs={'class': 'a-icon-alt'}):
                product_json['star-rating'] = spans.text.strip()
                break
        # This block of code will help extract the number of customer reviews of the product
        for spans in soup.findAll('span', attrs={'id': 'acrCustomerReviewText'
                                  }):
            if spans.text:
                review_count = spans.text.strip()
                product_json['customer-reviews-count'] = review_count
                break
        # This block of code will help extract top specifications and details of the product
        product_json['details'] = []
        for ul_tags in soup.findAll('ul',
                                    attrs={'class': 'a-unordered-list a-vertical a-spacing-none'
                                    }):
            for li_tags in ul_tags.findAll('li'):
                for spans in li_tags.findAll('span',
                        attrs={'class': 'a-list-item'}, text=True,
                        recursive=False):
                    product_json['details'].append(spans.text.strip())

        # This block of code will help extract the short reviews of the product

        product_json['short-reviews'] = []
        reviewdetails = []

        for divs in soup.findAll('div', attrs={'class': 'a-section review aok-relative'}):
            productjsn = {}
            productjsn['brand'] =[]
            productjsn['brand'].append(product_json['name'])
            productjsn['price'] =[]
            productjsn['price'].append(product_json['price'])
            productjsn['img-url'] =[]
            productjsn['img-url'].append(product_json['img-url'])
            productjsn['star-rating'] =[]
            productjsn['star-rating'].append(product_json['star-rating'])
            productjsn['customer-reviews-count'] =[]
            productjsn['customer-reviews-count'] = product_json['customer-reviews-count']
            productjsn['details'] =[]
            productjsn['details'] = product_json['details']
            productjsn['short-reviews'] = []
            for a_tags in divs.findAll('a',
                                       attrs={'data-hook': 'review-title'
                                       }):
                short_review = a_tags.text.strip()
                productjsn['short-reviews'].append(short_review)
            # This block of code will help extract the long reviews of the product
            productjsn['long-reviews'] = []
            for divs01 in divs.findAll('div', attrs={'data-hook': 'review-collapsed'
                                     }):
                long_review = divs01.text.strip()
                productjsn['long-reviews'].append(long_review)

            productjsn['person_name'] = []
            for spans in divs.findAll('span', attrs={'class': 'a-profile-name'
                                                   }):
                person_name = spans.text.strip()
                productjsn['person_name'].append(person_name)
                reviewdetails.append(productjsn)
        # Saving the scraped html file
        with open('output_file.html', 'wb') as file:
            file.write(html)
        storeAmazonData = {}
        storeAmazonData['website'] = "www.Amazon.com"
        storeAmazonData['brand'] = product_json['name'];
        storeAmazonData['htmlContent'] = html

        # Saving the scraped data in json format
        with open('product.json', 'w') as outfile:
            json.dump(reviewdetails, outfile, indent=4)
        print ('----------Extraction of data is complete. Check json file.----------')

        m.insertIntoMongodb(storeAmazonData)
        result = m.insertIntoMongodb(reviewdetails)



        #print("mongo db status insert - "+result)

