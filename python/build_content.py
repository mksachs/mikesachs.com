import sys
import argparse

import bs4
from bs4 import BeautifulSoup

sys.path.append('./')

def latex_escape(text, abbrev=False):
    if len(text) != 0:
        if abbrev:
            tmp_text = '.~'.join(text.split('. '))
            if tmp_text[-1] == '~':
                text = tmp_text[0:-2]
            else:
                text = tmp_text
        return '\\$'.join('\\%'.join(
            '\\&'.join(
                '\\#'.join(
                    '\\_'.join(
                        text.split('_')
                    ).split('#')
                ).split('&')
            ).split('%')
        ).split('$'))
    else:
        return ''

class Resume:
    doc_title_str = """\\makeheading{Michael Sachs}
        {http://www.mikesachs.com}
        {www.mikesachs.com}
        {mike@mikesachs.com}
        {646-262-8530}



"""

    def __init__(self, base_html_doc_loc: str, doc_header_template_loc: str, **kwargs):
        self.no_title_sections = ['summary']
        try:
            self.skip_sections = kwargs['skip_sections']
        except KeyError:
            self.skip_sections = []

        html_f = open(base_html_doc_loc)
        soup = BeautifulSoup(html_f.read(), 'html.parser')
        self.sections_tags = soup('div', class_='section')

        doc_header_template_f = open(doc_header_template_loc)
        self.doc_header_template = doc_header_template_f.read()
        self.sections = []

        html_f.close()
        doc_header_template_f.close()

    def generate(self):
        if len(self.sections) != 0:
            self.sections = []
        for section in self.sections_tags:
            rs = ResumeSection(section)
            if rs.section_id not in self.skip_sections:
                if rs.section_id in self.no_title_sections:
                    rs.skip_title = True
                rs.generate()
                self.sections.append(rs)

    def latex(self) -> str:
        if len(self.sections) == 0:
            self.generate()

        latex_str_list = [self.doc_header_template, '\\begin{document}', self.doc_title_str]
        for section in self.sections:
            latex_str_list.append(section.latex())
        latex_str_list.append('\\end{document}\n')
        latex_str_list.append('%%%%%%%%%%%%%%%%%%%%%%%%% End CV Document %%%%%%%%%%%%%%%%%%%%%%%%%%%%')

        return ''.join(latex_str_list)

class ResumeSection:
    def __init__(self, section_tag: bs4.element.Tag, **kwargs):
        try:
            self.skip_title = kwargs['skip_title']
        except KeyError:
            self.skip_title = False
        self.section_tag = section_tag
        self.section_title = self.section_tag.find('h1').get_text(strip=True)
        self.section_id = self.section_tag['id']
        self.subsections = []

    def generate(self):
        if len(self.subsections) != 0:
            self.subsections = []

        subsections_tags = self.section_tag(class_= 'subsection');

        for subsection in subsections_tags:
            try:
                subsection_type = next(x for x in subsection['class'] if x != 'subsection')
            except StopIteration:
                subsection_type = None
            if subsection_type == 'job':
                self.subsections.append(ResumeJob(subsection))
            elif subsection_type == 'school':
                self.subsections.append(ResumeSchool(subsection))
            elif subsection_type == 'publication':
                self.subsections.append(ResumePublication(subsection))
            elif subsection_type == 'conference':
                self.subsections.append(ResumeConference(subsection))
            elif subsection_type == 'news-outlet':
                self.subsections.append(ResumePress(subsection))
            elif subsection_type == 'space':
                self.subsections.append(ResumeSpace(subsection))
            elif subsection_type is None:
                if self.section_id == 'summary':
                    self.subsections.append(ResumeSummary(subsection))
                elif self.section_id == 'technologies':
                    self.subsections.append(ResumeTechnology(subsection))
                elif self.section_id =='awards':
                    self.subsections.append(ResumeAwards(subsection))

    def latex(self) -> str:
        if len(self.subsections) == 0:
            self.generate()
        subsections_str = ''
        for subsection in self.subsections:
            subsections_str += subsection.latex()
        latex_str = '% Section\n'
        end_bibsection = ''
        if not self.skip_title:
            latex_str += f'\\section{{{self.section_title}}}\n\n'
            if self.section_id == 'publications':
                latex_str += '\n\\begin{bibsection}\n'
                end_bibsection = '\\end{bibsection}\n\\vspace{1.5\\baselineskip}\n\n'

        latex_str += f'{subsections_str}{end_bibsection}\\vspace{{\\baselineskip}}\n'

        return latex_str

class ResumeSpace:

    def __init__(self, space_tag: bs4.element.Tag):
        self.space_height = float(space_tag['class'][-1])

    def latex(self) -> str:
        return f"""\\vspace{{{self.space_height:.1f}\\baselineskip}}

"""

class ResumePress:

    def __init__(self, news_outlet_tag: bs4.element.Tag):
        self.name = news_outlet_tag.find(class_='name').get_text(strip=True)
        self.articles = []
        for article in news_outlet_tag(class_='article'):
            self.articles.append(article)

    def latex(self) -> str:
        articles_str_list = []
        for art in self.articles:
            try:
                href = art.find('a').attrs['href']
            except AttributeError:
                href = ''
            if href == '':
                for child in art.children:
                    if child.name != 'br':
                        articles_str_list.append(f'{child.strip()}')
            else:
                title = art.get_text(strip=True)
                articles_str_list.append(f'\\href{{{href}}}{{{title}}}')

        newline_str = '\\\\ \n'
        latex_str = f"""% Subsection
\\subsection{{{self.name}}}{{}}

{newline_str.join(articles_str_list)}
\\vspace{{1.5\\baselineskip}}

"""
        return latex_str

class ResumeAwards:

    def __init__(self, awards_tag: bs4.element.Tag):
        self.awards_list = []
        for li in awards_tag('li'):
            self.awards_list.append(latex_escape(li.get_text(strip=True)))

    def latex(self) -> str:
        awards_list_str = ''
        for li in self.awards_list:
            awards_list_str += f'\\item[\\listbullet] {li}\n'
        latex_str = f"""% Subsection
\\begin{{loneinnerlist}}
{awards_list_str}\\end{{loneinnerlist}}
\\vspace{{1.5\\baselineskip}}

"""
        return latex_str

class ResumePublication:

    def __init__(self, pub_tag: bs4.element.Tag):
        self.pub_tag = pub_tag

    def author_line(self, text) -> str:
        if len(text.split('*M. K. Sachs')) == 1:
            return latex_escape(' \\bf{M. K. Sachs}'.join(text.split('M. K. Sachs')), abbrev=True).strip()
        else:
            return latex_escape(' \\bf{*M. K. Sachs}'.join(text.split('*M. K. Sachs')), abbrev=True).strip()

    def latex(self) -> str:
        latex_str_lst = []
        for child in self.pub_tag.children:
            if type(child) is bs4.element.Tag:
                if child.name == 'span':
                    if child['class'][0] == 'title':
                        title_str = latex_escape(child.get_text(strip=True))
                        try:
                            href_str = latex_escape(child.contents[0]['href'])
                            latex_str_lst.append(f'\\item \\bf{{\\href{{{href_str}}}{{{title_str}}}}}')
                        except TypeError:
                            latex_str_lst.append(f'\\item \\bf{{{title_str}}}')
                    elif child['class'][0] == 'author':
                        author_str = self.author_line(child.get_text(strip=True))
                        latex_str_lst.append(f'{author_str}')
                    elif child['class'][0] == 'date':
                        date_str = latex_escape(child.get_text(strip=True), abbrev=True)
                        latex_str_lst.append(f'({date_str}) ')
                    else:
                        other_str = latex_escape(child.get_text(strip=True), abbrev=True)
                        latex_str_lst.append(f'{other_str} ')
                elif child.name == 'br':
                    latex_str_lst.append('\\\\ \n')
            elif type(child) is bs4.element.NavigableString:
                try:
                    char = child.encode('ascii', 'xmlcharrefreplace').strip().split()[0]
                except IndexError:
                    char = None
                if char == '&#160;':
                    latex_str_lst.append(' ')
        latex_str = ''.join(latex_str_lst)
        if latex_str[-5:-1].strip() == '\\\\':
            return latex_str[0:-5] + '\n\n'
        else:
            return latex_str + '\n\n'

class ResumeConference:

    def __init__(self, conference_tag: bs4.element.Tag):
        self.name = conference_tag.find(class_='name').get_text(strip=True)
        try:
            self.href = conference_tag.find(class_='name').find('a').attrs['href']
        except AttributeError:
            self.href = ''
        self.submissions = []
        for submission in conference_tag(class_='submission'):
            self.submissions.append(ResumePublication(submission))

    def latex(self) -> str:
        submissions_str_list = []
        for sub in self.submissions:
            submissions_str_list.append(sub.latex())
        latex_str = f"""% Subsection
\\subsection{{{self.name}}}{{{self.href}}}

\\begin{{bibsection}}
{''.join(submissions_str_list)}\\end{{bibsection}}
\\vspace{{1.5\\baselineskip}}

"""
        return latex_str

class ResumeSchool:

    def __init__(self, job_tag: bs4.element.Tag):
        self.org = job_tag.find(class_='org').get_text(strip=True)
        self.degree_date = job_tag.find(class_='degree_date').get_text(strip=True)
        # self.description_list = job_tag.find(class_='description').get_text(strip=True)
        self.description_list = []
        ul = job_tag.find('ul', class_='description')
        if ul is not None:
            for li in ul('li'):
                self.description_list.append(latex_escape(li.get_text(strip=True)))

    def latex(self) -> str:
        description_list_str = ''
        for li in self.description_list:
            description_list_str += '\\item[\\listbullet] {li}\n'.format(li=li)
        latex_str = f"""% Subsection
\\subsection{{{self.org}}}{{}}

\\subsubsectiontitle{{{self.degree_date}}}\\\\

\\begin{{outerlist}}
{description_list_str}\\end{{outerlist}}
\\vspace{{1.5\\baselineskip}}

"""
        return latex_str

class ResumeTechnology:

    def __init__(self, job_tag: bs4.element.Tag):
        self.subtitle = job_tag.find('h2').get_text(strip=True)
        self.description = job_tag.find('p').get_text(strip=True)

    def latex(self) -> str:
        latex_str = f"""% Subsection
\\subsection{{{self.subtitle}}}{{}}

{self.description}
\\vspace{{1.5\\baselineskip}}

"""
        return latex_str

class ResumeJob:

    def __init__(self, job_tag: bs4.element.Tag):
        self.org = job_tag.find(class_='org').get_text(strip=True)
        self.roles = [ResumeRole(x) for x in job_tag.find_all(class_='role')]

    def latex(self) -> str:
        latex_str = f"""% Subsection
\\subsection{{{self.org}}}{{}}

"""
        for role in self.roles:
            latex_str += f"{role.latex()}"

        latex_str += '\\vspace{{0.5\\baselineskip}}\n\n'

        return latex_str

class ResumeRole:

    def __init__(self, role_tag: bs4.element.Tag):
        self.title =  role_tag.find(class_='title').get_text(strip=True)
        self.dates = role_tag.find(class_='dates').get_text(strip=True)
        try:
            self._description_text = role_tag.find('p', class_='description').get_text(strip=True)
        except AttributeError:
            self._description_text = ''
        self._description_list = []
        ul = role_tag.find('ul', class_='description')
        if ul is not None:
            for li in ul('li'):
                self._description_list.append(li.get_text(strip=True))

    @property
    def description_text(self):
        return latex_escape(self._description_text)

    @property
    def description_list(self):
        return [latex_escape(x) for x in self._description_list]

    def latex(self) -> str:

        description_list_str = ''
        for li in self.description_list:
            description_list_str += f'\\item[\\listbullet] {li}\n'
        latex_str = f"""\\subsubsectiontitle{{{self.title}}}\\\\
\\subsubsectionsubtitle{{{self.dates}}}\\\\
"""
        if self.description_text != '':
            latex_str +=f"""
{self.description_text}
"""

        latex_str += f"""
\\vspace{{\\baselineskip}}

\\begin{{outerlist}}
{description_list_str}\\end{{outerlist}}\\\\

\\vspace{{1.5\\baselineskip}}

"""
        return latex_str

class ResumeSummary:
    def __init__(self, summary_tag: bs4.element.Tag):
        self.highlight_title = summary_tag.find('b').get_text(strip=True)
        try:
            self._summary_text = summary_tag.find('p').get_text(strip=True)
        except AttributeError:
            self._summary_text = ''
        self._highlight_list = []
        ul = summary_tag.find('ul')
        if ul is not None:
            for li in ul('li'):
                self._highlight_list.append(li.get_text(strip=True))

    @property
    def summary_text(self):
        return latex_escape(self._summary_text)

    @property
    def highlight_list(self):
        return [latex_escape(x) for x in self._highlight_list]

    def latex(self) -> str:

        highlight_list_str = ''
        for li in self.highlight_list:
            highlight_list_str += f'\\item[\\listbullet] {li}\n'
        latex_str = f"""{self.summary_text}\\\\

\\bf{{{self.highlight_title}}}\\\\

\\begin{{outerlist}}
{highlight_list_str}\\end{{outerlist}}\\\\

\\vspace{{1.5\\baselineskip}}


"""
        return latex_str

def main(argv=None):
    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '-w', '--web',
        help='Create the web version of the pdf resume. If no args are supplied this is the default action.',
        action='store_true'
    )
    group.add_argument('-p', '--print', dest='print_ver', help='Create the print version of the pdf resume.',
                    action='store_true')
    parser.add_argument('-m', '--min', dest='min', help='Create a mini version of the resume.',
                       action='store_true')
    args = parser.parse_args()

    # html_f = open('../index.html')

    # skip_sections = ['examples']
    #
    # if args.print_ver:
    #     xetex_template_f = open('../tex/templates/template_print.xetex')
    #     skip_sections.append('conferences')
    # else:
    #     xetex_template_f = open('../tex/templates/template_web.xetex')
    #
    # if args.min:
    #     skip_sections.append('publications')
    #     skip_sections.append('awards_and_recognition')
    #     skip_sections.append('teaching_experience')
    #     skip_sections.append('press')
    #     skip_sections.append('conferences')
    #
    # skip_sections = list(set(skip_sections))

    resume = Resume('../index.html', '../tex/templates/doc_header_template.ltx', skip_sections = ['awards', 'conferences', 'press', 'publications'])

    out_f = open('../tex/pdf.ltx','w')

    out_f.write(resume.latex())
    out_f.close()

if __name__ == "__main__":
    sys.exit(main())
