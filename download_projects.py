import sqlite3
import os
from subprocess import Popen, PIPE

from lastversion import lastversion

os.environ['GITHUB_API_TOKEN'] = ''


class Projects:
    def __init__(self, proj_name, url, language, build):
        self.proj = proj_name
        self.github_url = url
        self.github = self.github_url[19:]
        self.lang = language
        self.builder = build
        self.version = ''

    def download(self):
        cmd = f'mkdir sources && cd ../sources && python -m lastversion download {self.github} -o {self.lang}/{self.proj}.tar.gz'
        cmd += f' && cd {self.lang} && tar xzf {self.proj}.tar.gz'
        p = Popen(cmd, shell=True, stdout=PIPE, stdin=PIPE, stderr=PIPE)
        print(f'Downloaded and extracted {self.proj}')
        out, err = p.communicate()

        # if not new_version == self.version:
        #     stmt = f'UPDATE projects SET version = "{new_version}" WHERE github_url == "{self.github_url}"'
        #     print(stmt)
        #     con.execute(stmt)

    def build(self):
        self.version = lastversion.latest(repo=self.github)
        cmd = f'cd ../sources/{self.lang}/{self.proj}-{self.version}'
        cmd += f'&& atom data-flow -o ./atom-samples/{self.lang}/{self.proj}.atom --slice-outfile {self.proj}-df.json -l {self.lang} .'
        cmd += f' && atom usages -o ../atom-samples/{self.lang}/{self.proj}.atom --slice-outfile {self.proj}-usages.json -l {self.lang} .'
        # p = Popen(cmd, shell=True, stdout=PIPE, stdin=PIPE, stderr=PIPE)
        # out,err = p.communicate()
        # print(err)


con = sqlite3.connect('projects.db')
data = con.execute('SELECT * FROM projects')
result = data.fetchall()
con.close()

# tab = []
for row in result:
    proj = row[0]
    url = row[1]
    lang = row[2]
    builder = row[3]
    # github = url[19:]
    project = Projects(proj_name=proj, url=url, language=lang, build=builder)
    project.download()
    project.build()
    # tab.append(
    #         f'|[{github}]({url})|{lang}|')


# tab.sort()
# for lst in tab:
#     print(lst)
