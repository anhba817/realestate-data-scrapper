import scrapy, json
from datetime import datetime
from scrapy.http import FormRequest
from scrapy.selector import Selector

# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC

class ActionPropertySpider(scrapy.Spider):
    name = 'actionproperty'
    pagination_url = 'https://actionproperty.ca/wp-admin/admin-ajax.php'
    page_incr = 1

    def start_requests(self):
        urls = [
            # 'https://actionproperty.ca/properties/?wpp_search%5Bsort_order%5D=ASC&wpp_search%5Bpagination%5D=on&wpp_search%5Bper_page%5D=10&wpp_search%5Bstrict_search%5D=false&wpp_search%5Bproperty_type%5D=commercial%2Cresidential%2Capartment_residential&wpp_search%5Bcity%5D=Fort+St.+John&wpp_search%5Bavailability%5D=-1&wpp_search%5Bprice%5D%5Bmin%5D=&wpp_search%5Bprice%5D%5Bmax%5D=&wpp_search%5Bfurnished%5D=-1',
            'https://actionproperty.ca/',
        ]
        self.date = datetime.now()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response, total = 0):
        sel = Selector(response)

        if self.page_incr > 1:
            json_data = json.loads(response.body)
            sel = Selector(text=json_data.get('display', ''))

        for selector in sel.css('li.property_title'):
            href = selector.xpath('.//a/@href').get()
            building_type = selector.css('div::text').get()
            building_type = building_type.strip() if building_type else ''
            yield response.follow(href, callback=self.parse_article,
                cb_kwargs=dict(building_type=building_type), dont_filter=True)

        total_page = sel.css('span.wpp_total_page_count::text').get()
        total_page = total_page.strip() if total_page else total
        #pagination code starts here
        # if page has content
        if self.page_incr < int(total_page):
            self.page_incr +=1
            formdata = {
                "action": "wpp_property_overview_pagination",
                "wpp_ajax_query[strict_search]": "false",
                "wpp_ajax_query[show_children]": "true",
                "wpp_ajax_query[child_properties_title]": "Floor plans at location:",
                "wpp_ajax_query[fancybox_preview]": "true",
                "wpp_ajax_query[bottom_pagination_flag]": "true",
                "wpp_ajax_query[thumbnail_size]": "overview_thumbnail",
                "wpp_ajax_query[sort_by_text]": "Sort By:",
                "wpp_ajax_query[sort_by]": "post_date",
                "wpp_ajax_query[sort_order]": "DESC",
                "wpp_ajax_query[template]": "false",
                "wpp_ajax_query[ajax_call]": "true",
                "wpp_ajax_query[disable_wrapper]": "false",
                "wpp_ajax_query[sorter_type]": "buttons",
                "wpp_ajax_query[sorter]": "on",
                "wpp_ajax_query[pagination]": "on",
                "wpp_ajax_query[pagination_type]": "slider",
                "wpp_ajax_query[hide_count]": "false",
                "wpp_ajax_query[per_page]": "10",
                "wpp_ajax_query[starting_row]": "0",
                "wpp_ajax_query[query][pagi]": "0--10",
                "wpp_ajax_query[query][requested_page]": "%s" % self.page_incr,
                "wpp_ajax_query[current_page]": "1",
                "wpp_ajax_query[sortable_attrs][post_title]": "Title",
                "wpp_ajax_query[sortable_attrs][availability]": "Availability",
                "wpp_ajax_query[sortable_attrs][city]": "City",
                "wpp_ajax_query[sortable_attrs][price]": "Price",
                "wpp_ajax_query[sortable_attrs][bedrooms]": "Bedrooms",
                "wpp_ajax_query[sortable_attrs][bathrooms]": "Bathrooms",
                "wpp_ajax_query[sortable_attrs][furnished]": "Furnished",
                "wpp_ajax_query[default_query][sort_by]": "post_date",
                "wpp_ajax_query[default_query][sort_order]": "DESC",
                "wpp_ajax_query[default_query][pagi]": "0--10",
                "wpp_ajax_query[default_query][requested_page]": "%s" % self.page_incr,
                "wpp_ajax_query[index]": "1",
                "wpp_ajax_query[requested_page]": "%s" % self.page_incr
            }
            yield scrapy.FormRequest(url=self.pagination_url, formdata=formdata, callback=self.parse, cb_kwargs=dict(total=total_page), dont_filter=True)
        else:
            return

    def parse_article(self, response, building_type):
        title = response.css('h1.property-title.entry-title::text').get().strip()
        property_list = response.css('ul.overview_stats')

        value = property_list.css('li.property_location span.value::text').get()
        location = value.strip() if value else ''

        value = property_list.css('li.property_availability span.value::text').get()
        availability = value.strip() if value else ''

        value = property_list.css('li.property_city span.value::text').get()
        city = value.strip() if value else ''

        value = property_list.css('li.property_price span.value::text').get()
        price = value.strip() if value else ''

        value = property_list.css('li.property_deposit span.value::text').get()
        deposit = value.strip() if value else ''

        value = property_list.css('li.property_utilities span.value::text').get()
        utilities = value.strip() if value else ''

        value = property_list.css('li.property_bedrooms span.value::text').get()
        bedrooms = value.strip() if value else ''
        value = property_list.css('li.property_bathrooms span.value::text').get()
        bathrooms = value.strip() if value else ''
        yield {
            'source': 'ActionProperty',
            'date': self.date.strftime("%m/%d/%Y"),
            'title': title,
            'building_type': building_type,
            'availability': availability,
            'city': city,
            'rent': "$%s" % price,
            'security_deposit': "$%s" % deposit,
            'utilities': utilities,
            'bedrooms': bedrooms,
            'bathrooms': bathrooms,
            'units_in_building': '',
            'address': location,
        }
