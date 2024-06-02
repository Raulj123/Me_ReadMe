import os
from github import Github
from github import Auth
from dotenv import load_dotenv, dotenv_values

load_dotenv()
auth = Auth.Token(os.getenv("TOKEN"))
g = Github(auth=auth)
user = g.get_user()

name = user.name
languages = {}


temp = "temp.md"
out = "README.md"
site = "rjvhome"
msg1 = "Does anyone read these? 😔"

def render(n,topLanguages):

    with open(temp) as file:
        temp_content = file.read()

    filled_content = temp_content.replace('{name}', name)\
                                 .replace('{repos}', str(n))\
                                 .replace('{site}', site)\
                                 .replace('{top}', topLanguages)\
                                 .replace('{msg1}', msg1)
    
    with open(out, "w") as file:
        file.write(filled_content)
    


def getInfo():
    nrepos = 0
    for repo in user.get_repos():

        if repo.owner.login != user.login:
            continue

        nrepos += 1
        repo_lang = repo.get_languages()
        
        for lang, size in repo_lang.items():
            if lang in languages:
                languages[lang] += size
            else:
                languages[lang] = size

    total_lines = sum(languages.values())

    language_percentages = {lang: (size / total_lines) * 100 for lang, size in languages.items()}
    sorted_languages = sorted(language_percentages.items(), key=lambda x: x[1], reverse=True)
    topLanguages = ""

    for lang, percentage in sorted_languages[:3]:
        
        topLanguages += f" {lang} {percentage:.2f}%,"

    otherP = 0
    for lang, p in sorted_languages[3:]:
        otherP += p



    topLanguages += f" Other ({otherP:.2f}%)\n"
    
    return nrepos, topLanguages


def main():
    n,topLanguages = getInfo()
    print(n,topLanguages)
    render(n,topLanguages)

if __name__ == "__main__":
    main()