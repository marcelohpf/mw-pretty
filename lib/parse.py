import re
import json
from urllib.request import urlopen

class PageProcess:
    def get_page(self,url):
        """Use url open to return a http response if it is successful"""
        http_response = urlopen(url)
        if http_response.status != 200:
            raise "Can't connect to %s" % url
        return http_response

    def get_content_page(self,url):
        """Given a url, return the content of the page in a string
           python format"""
        page = self.get_page(url)
        assert(page.status == 200)
        content = page.read()
        string_content = content.decode('utf-8')
        return string_content
        
class GenerateData:
    """Fetch the data from matricula web for a giver course
       and save it in a file to generate the beautiful view"""
    BASE_URL = 'https://matriculaweb.unb.br/graduacao/curriculo.aspx?cod='

    def __init__(self,course_code):
        assert(re.search(r'\D+',str(course_code)) is None)
        self.code = str(course_code)
        self.url_course = self.BASE_URL+self.code

    def output_data(self):
        """Write the content matched from matricula web to a file
           with name 'code_of_course.json'"""
        jsonfy_data = json.dumps(self.data_course)
        with open(self.code+'.json','w') as file_output:
            file_output.write(jsonfy_data)
    data_course={123321:[232,3231,1231]}

class Course(PageProcess):
    """Contains all information about the course, use get_discipline
       to obtain the data"""

    PATTER_CODES = r'[^#>](\d{6})'
    name = ''
    disciplines = []
    def __init__(self,url):
        self.url = url
    def extract_codes(self):
        """Obtain the codes of disciplines
           returns a list with codes separeted by position in:
           1 - obrigatory
           2 - optatives
           3.. cicle chain"""
        assert(self.url != None)
        page_course = self.get_content_page(self.url)
        # TODO: Find a efficient way to split positions
        code_disciplines = re.findall(self.PATTER_CODES,page_course)
        return code_disciplines
    def mount_disciplines(self):
        codes = self.extract_codes()

if __name__ == '__main__':
    a = GenerateData(6360)
    a.output_data()
    b = Course(a.url_course)
    print(b.extract_codes())
