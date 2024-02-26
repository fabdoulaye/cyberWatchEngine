import scrapy
from ..items import TheHackerNewsWatchEngineItem
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs


class TheHackerNewsWatchEngineSpider(scrapy.Spider):
    name = 'thehackernewsWatchEngine'
    dayDate = datetime.now().strftime('%Y-%m-%d') + 'T23:59:59%2B05:30&max-results=20'
    start_urls = [
        'https://thehackernews.com/search?updated-max=' + dayDate + '&max-results=9&start=9&by-date=true'
    ]

    def parse(self, response, **kwargs):

        items = TheHackerNewsWatchEngineItem()

        all_div_posts = response.css('div.body-post')

        for div_posts in all_div_posts:

            title = div_posts.css(".home-title::text").extract()
            link = div_posts.css('a.story-link::attr(href)').get()
            date = div_posts.css(".h-datetime::text").extract()
            htag = div_posts.css(".h-tags::text").extract()
            label = div_posts.css(".item-label::text").extract()
            descr = div_posts.css(".home-desc::text").extract()
            alterimgtext = div_posts.css('img.home-img-src::attr(alt)').extract()
            imgpath = div_posts.css('img.home-img-src::attr(data-src)').extract()
            # Utiliser urlparse pour extraire les composants de l'URL
            parsed_url = urlparse(link)
            # Extraire le nom de domaine
            domain_name = parsed_url.netloc

            items['title'] = title
            items['link'] = link
            items['date'] = date
            items['tags'] = htag
            # items['tag2'] = htag[0].split("/")[1].strip()
            items['label'] = label
            items['description'] = descr
            items['imagepath'] = imgpath
            items['alterimagetext'] = alterimgtext
            items['domainname'] = domain_name

            yield items

        # To get all href on a page :
        # next_page = # To get all href on a page :
        # next_page = response.css("div.blog-pager a").xpath("@href")[0].extract()
        next_page = response.css("#Blog1_blog-pager-older-link").css('a.blog-pager-older-link-mobile::attr(href)').extract_first()
        print("next_page = ", next_page)

        # Extraire les paramètres de l'URL
        parsed_url = urlparse(next_page)
        query_params = parse_qs(parsed_url.query)

        # Extraire la valeur de 'updated-max' (date) du dictionnaire des paramètres
        date_string = query_params.get('updated-max', [''])[0]

        # Analyser la date
        if date_string:
            # Convertir la chaîne de date en objet datetime
            date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S%z')

            # Obtenir la date actuelle
            current_date = datetime.now(date_object.tzinfo)

            # Calculer la date il y a un an
            one_year_ago = current_date - timedelta(days=365)

            # Comparer les dates
            if date_object > one_year_ago:
                # print("La date est postérieure à il y a un an.")
                yield response.follow(next_page, callback=self.parse)
