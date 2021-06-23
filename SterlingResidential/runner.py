import gspread
from oauth2client.service_account import ServiceAccountCredentials
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# Run crawler to get data
process = CrawlerProcess(get_project_settings())
process.crawl('sterlingmgmt')
process.start()

# upload to Google Sheet
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(credentials)

spreadsheet = client.open('RealEstateData')

with open('results.csv', 'r') as file_obj:
    content = file_obj.read()
    client.import_csv(spreadsheet.id, data=content)