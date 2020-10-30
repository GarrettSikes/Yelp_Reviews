from scrapy import Spider, Request
from webscrapy.items import WebscrapyItem

class yelp_reviewsSpider(Spider):
    name = "yelp_reviews_spider"
    allowed_urls = ['https://www.yelp.com/']
    start_urls = ['https://www.yelp.com/search?find_desc=BBQ&find_loc=New%20York%2C%20NY&sortby=review_count']


    def parse(self, response):
    
    # the parse function is for navigating through the different pages of yelp resteraunts

        potential_cities = ['New York NY', 'Los Angeles CA', 'Chicago IL', 'Houston TX', 'Phoenix AZ', 'Philadelphia PA', 'San Antonio TX', 'San Diego CA', 'Dallas TX', 'San Jose CA']   
        # starting with top ten cities by population
        potential_cities_urls = []         # link for all the potential cities
        yelp_cities_urls = []               # link for all the yelp pages of potential cities
        potential_cities_split = []       # potential cities split into nested lists to use for searching cities within the url
        potential_cities_format = 'https://www.yelp.com/search?find_desc=BBQ&find_loc={}&sortby=review_count&start={}'
        # input location and review number start(multiples of 10) 

        for i in potential_cities:
            potential_cities_split.append(i.split(" "))
            #print("First for loop", '-'*80)
        for j in potential_cities_split:
            if len(j)==2:
                potential_cities_urls.append(j[0] + '%2C%20' + j[1])
                #print("First if ", '-'*80)
            if (len(j)==3):
                potential_cities_urls.append(j[0] + '%20' + j[1] + '%2C%20' + j[2])
                #print("Second if ", '-'*80)
            if (len(j)==4):
                potential_cities_urls.append(j[0] + '%20' + j[1] + '%20' + j[2] + '%2C%20' + j[3])
                
        #print(potential_cities_url, '*'*80)

        for city in potential_cities_urls:
            # print('Test here above range of 0 to 150', '$'*50)
            #num_pages = int(response.xpath('').extract_first()) 
            cities = potential_cities[city]   
            for n in range(0,21,10): # 100 most reviewed resteraunts at 10 resteraunts per page: (10*num_pages)+1 would go through all pages
                # print('Test here above cities_url append', '&'*50)
                yelp_cities_urls.append(potential_cities_format.format(city,n))
                #print(city)
                #print(yelp_cities_url)
                #print('2nd urls for loop', '-'*80)
            # print('3rd for loop', '-'*80)

        for city_url in yelp_cities_urls[:3]:
            #print(url, ':'*40)
            yield Request(url=city_url, callback = self.parse_urls)

        print('last for loop', '-'*40)


    def parse_urls(self, response):
        # this function is meant to grab each resteraunts unique yelp url 
        #base_url = 'https://www.yelp.com'

        resteraunt_urls = response.xpath('//a[@class=" link__09f24__1kwXV link-color--inherit__09f24__3PYlA link-size--inherit__09f24__2Uj95"]/@href').extract()   #------------------------
        resteraunt_urls = list(filter(lambda url: url.find("ad_business_id") == -1, resteraunt_urls))

        #resteraunt_names = response.xpath('//a[@class=" link__09f24__1kwXV link-color--inherit__09f24__3PYlA link-size--inherit__09f24__2Uj95"]/@name').extract_first()

        for link in resteraunt_urls[:3]:
            #link = response.xpath('')
            #resteraunt_urls = resteraunt_urls.append(link)
            link = 'https://www.yelp.com' + link              # ----------------------------------------
            #print(url, ':'*40)
            yield Request(url=link, callback=self.parse_info)

        print('"link" loop finished', '='*40)


    def parse_info(self, response):
        # Retrieve the objects from meta
        print('on info page', '+'*40)
        #num_pages = 10 
    
        #for row in rows[:2]:
        rest_name = response.xpath('//h1[@class="lemon--h1__373c0__2ZHSL heading--h1__373c0__dvYgw undefined heading--inline__373c0__10ozy"]/text()').extract_first()
        overall_rating = response.xpath('//div[@class="lemon--div__373c0__1mboc i-stars__373c0__1T6rz i-stars--large-4__373c0__1d6HV border-color--default__373c0__3-ifU overflow--hidden__373c0__2y4YK"]/@aria-label').extract_first()
        dollar_rating = response.xpath('//span[@class="lemon--span__373c0__3997G text__373c0__2Kxyz text-color--normal__373c0__3xep9 text-align--left__373c0__2XGa- text-bullet--after__373c0__3fS1Z text-size--large__373c0__3t60B"]/text()').extract_first()
        num_reviews = response.xpath('//div[@class="lemon--div__373c0__1mboc arrange-unit__373c0__o3tjT border-color--default__373c0__3-ifU nowrap__373c0__35McF"]/p/text()').extract_first()
        #city = response.xpath('//div[@class="lemon--div__373c0__1mboc border-color--default__373c0__3-ifU overflow--hidden__373c0__2y4YK"]/input/@value').extract_first()  
        #review_text = response.xpath('').extract()
        #reviewer_username = 

        item = WebscrapyItem()

        item['rest_name'] = rest_name
        item['overall_rating'] = overall_rating
        item['dollar_rating'] = dollar_rating
        item['num_reviews'] = num_reviews
        #item['city'] = city # use a dictionary and meta to pass this from parse

        #item['reviewer_username'] = reviewer_username
        #item['review_text'] = review_text

        yield item

# how to step into another link?
