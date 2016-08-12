import re
import json
from urllib.request import urlopen

class PageProcess:
    PATTERN_CLEAN = {'pattern': '\n|\t|\r',
                    'repl': '',
                    }
    WITHOUT_SPACE = {'pattern': '> +<',
                     'repl': '><',
                     }
    def get_page(self,url):
        """Use url open to return a http response if it is successful"""
        http_response = urlopen(url)
        print('Try get page: '+url)
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
        
        # Remove spaces and enters and tabulations
        string_clean = re.sub(string=string_content, **self.PATTERN_CLEAN)
        string_content = re.sub(string=string_clean, **self.WITHOUT_SPACE)
        
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
    disciplines = {}
    def __init__(self,url):
        self.url = url
        self.mount_disciplines()

    def extract_codes(self):
        """Obtain the codes of disciplines
           returns a list with codes separeted by position in:
           1 - obrigatory
           2 - optatives
           3.. cicle chain
           4 - from others courses"""
        assert(self.url != None)
        page_course = self.get_content_page(self.url)

        # TODO: Find a efficient way to split positions
        code_disciplines = re.findall(self.PATTER_CODES,page_course)
        return code_disciplines

    def mount_disciplines(self):
        """From the codes in the page of discipline, create the dictionary
        with disciplines, obtains inclusive the pre-requisite
        """
        codes = self.extract_codes()
        for code in codes:
            if code not in self.disciplines:
                self.disciplines[code] = Discipline(code)
                codes.extend(self.disciplines[code].pre_requisit)
        return self.disciplines

    # TODO: start a dfs with pre requisits to determine the level of discipline
    def determine_levels(self):
        return None

    def __str__(self):
        strs = ""
        for code in self.disciplines:
            strs+= str(self.disciplines[code])
            strs+=", "
        return strs

class Discipline(PageProcess):

    BASE_URL = 'https://matriculaweb.unb.br/graduacao/disciplina.aspx?cod='
    def __init__(self,code):
        self.code = code
        self.url_discipline = self.BASE_URL+self.code
        self.level = 0
        page = self.get_content_page(self.url_discipline)
        self.get_name(page)
        self.get_pre_requisit(page)

    def get_name(self,page):
        """Find the full name off discipline, the name is after
        'Denominação', in same tr, but a different td in html content
        """
        match_name = re.search('Denominação:</b></td><td>([\w| |\d]+)</td>',page)
        if match_name is not None and len( match_name.groups()) >=1:
            self.name = match_name.groups()[0]
        else:
            raise 'Name not found'
        return self.name

    def get_pre_requisit(self,page):
        """The list with pre-requisits of discipline
        """
        # TODO: The disciplinas has conditions E and OU
        regex = '\w{2,4}-(\d{6})'
        self.pre_requisit = re.findall(regex,page)
        if len(self.pre_requisit) == 0:
            print("don't have pre-requiriment")
        return self.pre_requisit
    
    # TODO: determine the level of discipline if isn't
    def determine_level(self,disciplines):
        if self.level == 0:
            self.update_level(disciplines)

    # TODO: force a calculation of the level for this discipline
    def update_level(self,disciplines):
        return None

    def __str__(self):
        return "%s (%d)" % (self.name,self.level)

if __name__ == '__main__':
    a = GenerateData(6360)
    b = Course(a.url_course)
    print(b)
