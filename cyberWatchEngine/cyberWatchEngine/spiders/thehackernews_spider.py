import scrapy
from ..items import TheHackerNewsWatchEngineItem
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs, unquote
import re


class TheHackerNewsWatchEngineSpider(scrapy.Spider):
    name = 'thehackernewsWatchEngine'
    dayDate = datetime.now().strftime('%Y-%m-%d') + 'T23:59:59%2B05:30&max-results=20'
    url_domain = 'https://thehackernews.com/search'
    url_ext = dayDate + '&max-results=20&start=1&by-date=true'
    start_urls = [
        url_domain + '?updated-max=' + url_ext,
        url_domain + '/label/data%20breach?updated-max=' + url_ext,
        url_domain + '/label/Cyber%20Attack?updated-max=' + url_ext,
        url_domain + '/label/Vulnerability?updated-max=' + url_ext,
    ]

    def parse(self, response, **kwargs):

        # Get the actual URL of the response
        actual_url = response.url
        print("Actual URL:", actual_url)

        label_text = "home"
        items = TheHackerNewsWatchEngineItem()

        all_div_posts = response.css('div.body-post')

        for div_posts in all_div_posts:

            title = div_posts.css(".home-title::text").extract()
            link = div_posts.css('a.story-link::attr(href)').get()
            date = div_posts.css(".h-datetime::text").extract()
            htag = div_posts.css(".h-tags::text").extract()
            descr = div_posts.css(".home-desc::text").extract()
            alterimgtext = div_posts.css('img.home-img-src::attr(alt)').extract()
            imgpath = div_posts.css('img.home-img-src::attr(data-src)').extract()
            # Utiliser urlparse pour extraire les composants de l'URL
            parsed_url = urlparse(link)
            # Extraire le nom de domaine
            domain_name = parsed_url.netloc

            # Utiliser une expression régulière pour extraire le texte entre "label/" et "?"
            match = re.search(r'label/(.*?)[?&]', actual_url)
            if match:
                label_text = match.group(1)
                label_text = unquote(label_text)

            items['title'] = title
            items['link'] = link
            items['date'] = date
            items['tags'] = htag
            # items['tag2'] = htag[0].split("/")[1].strip()
            items['label'] = label_text
            items['description'] = descr
            items['imagepath'] = imgpath
            items['alterimagetext'] = alterimgtext
            items['domainname'] = domain_name

            yield items

        # To get all href on a page :
        # next_page = # To get all href on a page :
        # next_page = response.css("div.blog-pager a").xpath("@href")[0].extract()
        next_page = response.css("#Blog1_blog-pager-older-link")
        next_page = next_page.css('a.blog-pager-older-link-mobile::attr(href)').extract_first()
        print("next_page = ", next_page)

        # Extraire le label de l'URL
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
            #
            # Calculate the date 10 years ago
            ten_years_ago = current_date - timedelta(days=10 * 365)

            # Comparer les dates
            if date_object > ten_years_ago:
                # print("La date est postérieure à il y a un an.")
                yield response.follow(next_page, callback=self.parse)
