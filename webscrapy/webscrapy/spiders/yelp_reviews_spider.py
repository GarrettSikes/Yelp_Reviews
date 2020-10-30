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
            for n in range(0,101,10): # 100 most reviewed resteraunts at 10 resteraunts per page: (10*num_pages)+1 would go through all pages
                # print('Test here above cities_url append', '&'*50)
                yelp_cities_urls.append((city.replace('%2C%20', ' ').replace('%20', ' '), potential_cities_format.format(city,n)))
                #print(city)
                #print(yelp_cities_url)
                #print('2nd urls for loop', '-'*80)
            # print('3rd for loop', '-'*80)

        for city, url in yelp_cities_urls:
            #print(url, ':'*40)
            meta = {'location': city}
            yield Request(url=url, callback = self.parse_urls, meta=meta)

        print('last for loop', '-'*40)


    def parse_urls(self, response):
        # this function is meant to grab each resteraunts unique yelp url 

        resteraunt_urls = response.xpath('//a[@class=" link__09f24__1kwXV link-color--inherit__09f24__3PYlA link-size--inherit__09f24__2Uj95"]/@href').extract()   #------------------------
        resteraunt_urls = list(filter(lambda url: url.find("ad_business_id") == -1, resteraunt_urls))

        #resteraunt_names = response.xpath('//a[@class=" link__09f24__1kwXV link-color--inherit__09f24__3PYlA link-size--inherit__09f24__2Uj95"]/@name').extract_first()

        for link in resteraunt_urls:
            #link = response.xpath('')
            #resteraunt_urls = resteraunt_urls.append(link)
            link = 'https://www.yelp.com' + link              # ----------------------------------------
            #print(url, ':'*40)
            yield Request(url=link, callback=self.parse_resteraunt_page, meta=response.meta)

        #print('link loop finished', '='*40)
        

    def parse_resteraunt_page(self, response):
        # Find nmumber of review pages
        num_pages = 5 #response.xpath('//div[@class="lemon--div__373c0__1mboc pagination__373c0__3z4d_ border--top__373c0__3gXLy border--bottom__373c0__3qNtD border-color--default__373c0__3-ifU"]//span/text()').extract_first()
        starting_rest_page = response.request.url
        
        #print(starting_rest_page, '&'*40)
        
        # generate urls for those pages
        review_pages_urls = []
        for z in range(0,(num_pages*20), 20):
            review_pages_urls.append(starting_rest_page + '&start={}'.format(z))
        #review_page_urls[:5]
        # yield reuqest objects for each page to parse_info

        for page in review_pages_urls:
            #print(page, '-'*40)
            yield Request(url=page, callback=self.parse_info, meta=response.meta)
            


    def parse_info(self, response):

        # Retrieve the objects from meta
        print('on info page', '+'*40)
        #num_pages = 10 

        rest_name = response.xpath('//h1[@class="lemon--h1__373c0__2ZHSL heading--h1__373c0__dvYgw undefined heading--inline__373c0__10ozy"]/text()').extract_first()
        num_reviews = response.xpath('//div[@class="lemon--div__373c0__1mboc arrange-unit__373c0__o3tjT arrange-unit-fill__373c0__3Sfw1 border-color--default__373c0__3-ifU"]//p/text()').extract_first()
        overall_rating = response.xpath('//div[@class="lemon--div__373c0__1mboc arrange-unit__373c0__o3tjT border-color--default__373c0__3-ifU"]/span/div/@aria-label').extract_first()
        dollar_rating = response.xpath('//span[@class="lemon--span__373c0__3997G text__373c0__2Kxyz text-color--normal__373c0__3xep9 text-align--left__373c0__2XGa- text-bullet--after__373c0__3fS1Z text-size--large__373c0__3t60B"]/text()').extract_first()
        location = response.meta['location']
        
        #reviewer_username = response.xpath('//div[@class="lemon--div__373c0__1mboc user-passport-info border-color--default__373c0__3-ifU"]/span/a/text()').extract() 
        #review_rating = response.xpath('//div[@class="lemon--div__373c0__1mboc arrange-unit__373c0__o3tjT arrange-unit-grid-column--8__373c0__2dUx_ border-color--default__373c0__3-ifU"]//span/div/@aria-label').extract()
        #review_text =  

        item = WebscrapyItem()

        item['rest_name'] = rest_name
        item['overall_rating'] = overall_rating
        item['dollar_rating'] = dollar_rating
        item['num_reviews'] = num_reviews
        item['location'] = location

        #item['reviewer_username'] = reviewer_username
        #item['review_rating'] = review_rating
        #item['review_text'] = review_text

        yield item

# best way to go through comments



        
