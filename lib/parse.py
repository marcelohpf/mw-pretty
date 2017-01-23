from hashlib import sha256
from mw_error import NoName
from pathlib import Path
from urllib.request import urlopen

import json
import os
import re

MW_PATH = "/tmp/mw-pretty/"

class GenerateData:
    """Fetch the data from matricula web for a giver course
       and save it in a file to generate the beautiful view"""

    BASE_URL = 'https://matriculaweb.unb.br/graduacao/curriculo.aspx?cod='
    DATA_PATH = "/tmp/mw-pretty/data/"
    def __init__(self,course_code):
        assert(re.search(r'\D+',str(course_code)) is None)
        self.code = str(course_code)
        self.url_course = self.BASE_URL+self.code

    def output_data(self):
        """Write the content matched from matricula web to a file
           with name 'code_of_course.json'"""
        course = Course(self.url_course)
        data_course = json.dumps(course, 
                    default=lambda x: x.__dict__,
                    ensure_ascii=False,
                    sort_keys=True)

        if not os.path.exists(MW_PATH):
            os.mkdir(MW_PATH)
        if not os.path.exists(self.DATA_PATH):
            os.mkdir(self.DATA_PATH)
        data_dir = self.DATA_PATH + "%s.json" % self.code
        with open(data_dir,'w') as file_output:
            file_output.write(data_course)

class PageProcess:
    PATTERN_CLEAN = {'pattern': '\n|\t|\r',
                    'repl': '',
                    }
    WITHOUT_SPACE = {'pattern': '> +<',
                     'repl': '><',
                     }
    CACHE_DIR = "/tmp/mw-pretty/cache/"

    # TODO: make a cache with web pages and just verify the last date 
    # of change
    def get_page(self,url):
        """Use url open to return a http response if it is successful"""
        http_response = urlopen(url)
        print('Try get page: '+url)
        if http_response.status != 200:
            raise BaseException("Can't connect to %s" % url)
        return http_response

        
    def get_content_page(self,url):
        """Given a url, return the content of the page in a string
           python format"""
        string_content = ""
        if not self.has_cache(url):
            print("Obtain page from web")
            page = self.get_page(url)
            string_content = self.load_page_url(page)
            self.save_cache(url,string_content)
        else:
            print("Obtain page from cache")
            string_content = self.load_page_cache(url)
        
        return string_content
        
    def load_page_url(self,page):
        """Load a content and remove the characters \\n \\t \\r and remove 
           spaces between tags </>  <> from a http response object with status 
           code 200."""
        assert(page.status == 200)
        content = page.read()
        content_decoded = content.decode('utf-8')
    
        # Remove spaces and enters and tabulations
        content_clean = re.sub(string=content_decoded, **self.PATTERN_CLEAN)
        string_content = re.sub(string=content_clean, **self.WITHOUT_SPACE)

        return string_content

    def has_cache(self,url):
        """Only check if has a page in cache dir(/tmp/mw-pretty/)"""
        self.create_cache_dir()
        path = self.hash_url_path(url)
        cache_file = Path(path)
        print("Check cache in %s"%cache_file)
        return cache_file.is_file()

    def hash_url_path(self,url):
        """Return the hexa value using sha256 to a url"""
        file_path = str.encode(url)
        hash_function = sha256(file_path)
        path = self.CACHE_DIR+hash_function.hexdigest()
        return path

    def create_cache_dir(self):
        """Create the temporary dir to cache web pages"""
        if not os.path.exists(MW_PATH):
            os.mkdir(MW_PATH)
        if not os.path.exists(self.CACHE_DIR):
            os.mkdir(self.CACHE_DIR)
        
    def load_page_cache(self,url):
        """Load the content already processed from a cached file in tmp dir"""
        cache_file = self.hash_url_path(url)
        string_content = ""
        with open(cache_file,'r') as cache:
            string_content = cache.read()
        return string_content

    def save_cache(self,url,string_content):
        """Save a processed web page in cache"""
        cache_file = self.hash_url_path(url)
        with open(cache_file,'w') as cache:
            cache.write(string_content)


class Course(PageProcess):
    """Contains all information about the course, use get_discipline
       to obtain the data"""

    PATTER_CODES = r'[^#>](\d{6})'
    name = ''
    def __init__(self,url):
        self.disciplines = {}
        self.url = url
        self.mount_disciplines()
        self.determine_levels()

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
        # TODO: identify disciplines inexistents
        codes = self.extract_codes()
        for code in codes:
            discipline = Discipline(code)
            discipline_requirements = discipline.get_requirements()
            self.disciplines[code] = discipline
            self.disciplines.update(discipline_requirements)
                
        return self.disciplines

    def determine_levels(self):
        for discipline in self.disciplines.values():
            discipline.determine_level(self.disciplines)

    def print_pre_requirements(self):
        for discipline in self.disciplines.values():
            discipline.print_pre(self.disciplines,1)

    def __str__(self):
        strs = ""
        for code in self.disciplines:
            strs+= str(self.disciplines[code])
            strs+="\n"
        return strs


class Discipline(PageProcess):
    """Store the all informations about the discipline, obtain their 
    pre-requisites, name of discipline"""

    BASE_URL = 'https://matriculaweb.unb.br/graduacao/disciplina.aspx?cod='

    def __init__(self,code):
        self.code = code
        self.url_discipline = self.BASE_URL+self.code
        self.level = 0
        page = self.get_content_page(self.url_discipline)
        self.get_name(page)
        self.get_codes_requirement(page)

    def get_name(self,page):
        """Find the full name off discipline, the name is after
        'Denominação', in same tr, but a different td in html content
        """
        match_name = re.search('Denominação:</b></td><td>([\w| |\d|-]+)</td>',page)
        if match_name is not None and len( match_name.groups()) == 1:
            self.name = match_name.groups()[0]
        else:
            raise NoName('Name not found for discipline %s' % self.code)
        return self.name

    def get_codes_requirement(self,page):
        """The list with pre-requisits of discipline
        """
        # TODO: The disciplinas has conditions E and OU
        regex = '\w{2,4}-(\d{6})'
        self.pre_requirement = re.findall(regex,page)
        if len(self.pre_requirement) == 0:
            print("don't have pre-requirement")
        return self.pre_requirement
    
    def get_requirements(self):
        """Obtain recursively the all pre requirements for the discipline"""
        pre_disciplines = {}
        excluded_codes = []
        for code in self.pre_requirement:
            try:
                pre_disciplines[code] = Discipline(code)
                pre_discipline = pre_disciplines[code].get_requirements()
                pre_disciplines.update(pre_discipline)
            except NoName as e:
                print(e)
                excluded_codes.append(code)
        for excluded_code in excluded_codes:
            self.pre_requirement.remove(excluded_code)
        return pre_disciplines
                

    def determine_level(self,disciplines):
        """Execute a dfs to obtain the bigger level of discipline"""
        if self.level == 0:
            level_max=0
            for code_requisit in self.pre_requirement:
                next_discipline = disciplines[code_requisit]
                level = next_discipline.determine_level(disciplines)
                level_max = max(level_max, level)
            self.level = level_max+1

        return self.level

    def print_pre(self,disciplines,level):
        print("%s-%s "%(' '*level,self.name))
        for code in self.pre_requirement:
            
            disciplines[code].print_pre(disciplines,level+1)

    def __str__(self):
        return "%s (%d) <%s>" % (self.name,self.level,self.url_discipline)


