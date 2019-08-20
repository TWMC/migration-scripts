import os
import re
from datetime import datetime
from shutil import copyfile, copy

from bs4 import BeautifulSoup

html_walks_root_path = '/Users/lfoppiano/development/twmc/classic/previous_walks'
html_doc_path = html_walks_root_path + '/walks_2000.html'

output = "output"

years_to_process = ['2003', '2004', '2005']
# years_to_process = ['2006']

# kirby_hike_page_structure = {
#     "Title": "",
#     "Status": "Completed",
#     "Place": "",
#     "Location": "",
#     "Prefecture": "",
#     "Tags": "",
#     "Date": "",
#     "Enddate": "",
#     "Days": "",
#     "Organiser": "",
#     "Coorganiser": "",
#     "Difficulty": "",
#     "Description": "",
#     "Report": ""
# }

class KirbiGalleryData:
    gallery = 1
    caption = ''
    path = ''

    def to_string(self):
        output = []

        output.append("Caption: " + str(self.caption))
        output.append("\n\n")
        output.append("----")
        output.append("\n\n")

        output.append("Gallery: " + str(self.gallery))
        output.append("\n\n")
        output.append("----")
        output.append("\n\n")

        return ''.join(output)


class KirbiPageData():
    def __init__(self):
        self.images = []

    title = ''
    status = 'Completed'
    place = ''
    location = ''
    prefecture = ''
    tags = ''
    start_date = ''
    end_date = ''
    days = ''
    organiser = ''
    coorganiser = ''
    difficulty = ''
    description = ''
    report = ''
    # list of tuple (image, caption)
    images = []

    def to_string(self):
        output = []

        output.append("Title: " + str(self.title))
        output.append("\n\n")
        output.append("----")
        output.append("\n\n")

        output.append("Status: " + str(self.status))
        output.append("\n\n")
        output.append("----")
        output.append("\n\n")

        output.append("Place: " + str(self.place))
        output.append("\n\n")
        output.append("----")
        output.append("\n\n")

        output.append("Location: " + str(self.location))
        output.append("\n\n")
        output.append("----")
        output.append("\n\n")

        output.append("Prefecture: " + str(self.prefecture))
        output.append("\n\n")
        output.append("----")
        output.append("\n\n")

        output.append("Tags: " + str(self.tags))
        output.append("\n\n")
        output.append("----")
        output.append("\n\n")

        output.append("Date: " + str(self.start_date.strftime("%Y-%m-%d")))
        output.append("\n\n")
        output.append("----")
        output.append("\n\n")

        output.append("Enddate: " + str(self.end_date.strftime("%Y-%m-%d")))
        output.append("\n\n")
        output.append("----")
        output.append("\n\n")

        output.append("Days: " + str(self.days))
        output.append("\n\n")
        output.append("----")
        output.append("\n\n")

        output.append("Organiser: " + str(self.organiser))
        output.append("\n\n")
        output.append("----")
        output.append("\n\n")

        output.append("Coorganiser: " + str(self.coorganiser))
        output.append("\n\n")
        output.append("----")
        output.append("\n\n")

        output.append("Difficulty: " + str(self.difficulty))
        output.append("\n\n")
        output.append("----")
        output.append("\n\n")

        output.append("Description: " + str(self.description))
        output.append("\n\n")
        output.append("----")
        output.append("\n\n")

        output.append("Report: " + str(self.report))
        output.append("\n\n")
        output.append("----")
        output.append("\n\n")

        return ''.join(output)


def parse_walk_page(input_file):
    html_doc = open(input_file)

    soup = BeautifulSoup(html_doc, 'html.parser')

    body = soup.find("body")
    output = {}

    for child in body.children:
        if child.name == 'h2' or child.name == 'hr' or child.name == 'h3' or child.name == 'font':
            if 'header' not in output:
                output['header'] = []
            output['header'].append(child.text.strip())

        elif child.name == 'p':
            if 'description' not in output:
                output['description'] = []
            output['description'].append(child.text.strip())

    if 'images' not in output:
        output['images'] = []

    images = soup.find_all('img')
    for image in images:
        find_all = image.find_parent().find_all("font")
        # caption = '\n'.join([x for x in find_all])
        caption = [x.text.rstrip().replace('\n', '') for x in find_all]

        output['images'].append((os.path.dirname(input_file) + '/' + image['src'], ''.join(caption)))

    return output


def parse_index_walk_page(input_file):
    html_doc = open(input_file)

    soup = BeautifulSoup(html_doc, 'html.parser')

    body = soup.find("body")
    output = []

    for child in body.children:

        if child.name == 'h2' or child.name == 'hr' or child.name == 'h3' or child.name == 'font':
            month_year = child.text
            # if month_year not in output:
            #     output[month_year] = []

        elif child.name == 'P' or child.name == 'p':
            for child_2 in child.children:
                if child_2.name == 'table':
                    output.extend(parseTable(month_year, child_2))

        elif child.name == 'table':
            output.extend(parseTable(month_year, child))

        else:
            # print(child)
            pass

    return output


def parseTable(month_year, table):
    rows = table.find_all('tr')
    rows_out = []
    for row in rows:
        cols = row.find_all('td')
        cols_out = []
        if month_year is not None:
            cols_out.append(month_year)
        for ele in cols:
            report_link = ele.find_all('a')
            for link in report_link:
                print(link['href'])
                cols_out.append(parse_walk_page(html_walks_root_path + '/' + link['href']))

            cols_out.append(ele.text.strip())
        rows_out.append(cols_out)
    return rows_out


def get_walks_indexes_html_files(walks_directory, extension):
    # for subdir, dirs, files in os.walk(walks_directory):
    #     for file in files:
    #         if file.endswith('.html'):
    #             print(os.path.join(subdir, file))

    return [os.path.join(walks_directory, f) for f in os.listdir(walks_directory) if
            f.endswith(extension) and os.path.isfile(os.path.join(walks_directory, f))]


def clean(text):
    if text is None:
        return text

    return text.replace("\xc2\xa0", " ").replace(' ', ' ').replace(' ', ' ').replace('  ', ' ').replace('\n',
                                                                                                        ' ').rstrip()


def process_year(year_structure):
    yearly_pages = []
    for row in year_structure:

        kirbiPage = KirbiPageData()

        month_year = clean(row[0])
        if 'TWMC' in month_year or 'Back to the Home Page' in row:
            continue
        start_day = clean(row[1])
        end_day = clean(row[1])

        if start_day is '':
            start_day = '1'
            end_day = '1'

        numbers = re.findall('\\d+', start_day)
        # numbers = [int(s) for s in start_day.split() if s.isdigit()]

        if len(numbers) == 1:
            start_day = numbers[0]
            end_day = numbers[0]
        elif len(numbers) == 2:
            start_day = numbers[0]
            end_day = numbers[1]
        elif len(numbers) > 2:
            start_day = numbers[0]
            end_day = numbers[-1]

        raw_start_date = str(start_day) + ' ' + month_year
        raw_end_date = str(end_day) + ' ' + month_year

        start_date = datetime.strptime(clean(raw_start_date), '%d %B %Y')
        end_date = datetime.strptime(clean(raw_end_date), '%d %B %Y')

        # print(str(start_date) + ' ' + str(end_date))

        kirbiPage.start_date = start_date
        kirbiPage.end_date = end_date

        kirbiPage.days = (end_date - start_date).days + 1

        print(row)
        author_field = clean(row[3])
        if '+' in author_field:
            authors = author_field.split('+')

            kirbiPage.organiser = clean(authors[0])
            kirbiPage.coorganiser = clean(', '.join(authors[1:]))
        else:  # naive
            # authors = re.findall('\w+', row[3])
            kirbiPage.organiser = clean(row[3])
            # kirbiPage.coorganiser = ', '.join(authors[1, -1])

        title_u = clean(row[2])
        # title_u = title_u.replace(u"\u00A0", " ")
        kirbiPage.title = title_u

        title_split = kirbiPage.title.split("(")
        # kirbiPage.location = title_split[0]
        kirbiPage.place = title_split[0]

        if len(title_split) > 1:
            kirbiPage.prefecture = str.rstrip(title_split[1][0:-1])
            kirbiPage.title = str.rstrip(title_split[0])

        if len(row) > 4 and type(row[4]) != 'dict':
            if 'description' in row[4]:
                description = row[4]['description']
                kirbiPage.description = str.rstrip('\n'.join(description))

            if 'images' in row[4]:
                images = []
                for image, caption in row[4]['images']:
                    kirby_image = KirbiGalleryData()
                    kirby_image.path = image
                    kirby_image.caption = clean(caption)
                    images.append(kirby_image)

                kirbiPage.images.extend(images)

        yearly_pages.append(kirbiPage)

    return yearly_pages


def write_pages(kirby_pages, year, output):
    output_year_path = output + "/" + year
    if not os.path.exists(output_year_path):
        os.makedirs(output_year_path)

    for hike in kirby_pages:
        hike_title = hike.title.replace(' ', '-').replace('\\W', '').replace('\\t', '')
        output_year_hike_path = str.lower(output_year_path + '/' + hike_title)
        if os.path.exists(output_year_hike_path):
            output_year_hike_path = output_year_hike_path + '-2'
        os.makedirs(output_year_hike_path)

        with open(output_year_hike_path + '/' + 'hike.en.txt', 'w') as output_year_hike_file:
            output_year_hike_file.write(hike.to_string())

        for image in hike.images:
            if os.path.exists(image.path):
                copy(image.path, output_year_hike_path)
                print(image.path + " file missing. ")
            image_name = os.path.basename(image.path)

            with open(output_year_hike_path + '/' + image_name + '.en.txt', 'w') as output_image_file_caption:
                output_image_file_caption.write(image.to_string())


# files = get_walks_indexes_html_files(html_walks_root_path, ".html")
# [print(item) for item in parse_index_walk_page(html_walks_root_path + '/walks_' + '2000' + '.html')]
# [print(item) for item in parse_walk_page(html_walks_root_path + '/2000_07_Adatarasan/Adatarasan.html')]

def process(year):
    walk_structure = parse_index_walk_page(html_walks_root_path + '/walks_' + year + '.html')
    kirby_pages = process_year(walk_structure)
    write_pages(kirby_pages, year, output)


# process('2000')

for year in years_to_process:
    print(year)
    process(year)
# [print(item) for item in parse_index_walk_page(html_walks_root_path + '/walks_' + year + '.html')]

# print(parse_walk_page(html_walks_root_path + '/2000_07_Adatarasan/Adatarasan.html'))
