import requests, bs4, os, winshell
from pathlib import Path
from time import sleep


def main():
    # sleep(15)
    prog_path = os.getcwd()
    results = []
    URL = "https://www.vyatsu.ru/studentu-1/spravochnaya-informatsiya/raspisanie-zanyatiy-dlya-studentov.html"
    VYATSU = "https://www.vyatsu.ru"

    """Request page with multiple schedule's"""
    response = requests.get(URL)
    res = response.text

    """Parsing link with pdf file"""
    soup = bs4.BeautifulSoup(res, features="lxml")
    pdf = soup.find("div", {"class": "listPeriod", "id": "listPeriod_194912"})
    pdf_vars = pdf.find_all("a", {"target": "_blank"})
    for item in pdf_vars:
        pdf_link = item.get('href')
        results.append(pdf_link)

    """Request page with pdf file"""
    pdf_file_link = requests.get(VYATSU+results[0])

    """Formate date on filename"""
    date = results[0].split('/')[4].split('_')[3]
    date_format = f'{date[0:2]}.{date[2:4]}.{date[4:8]}'

    """Make filename and desktop path for download pdf"""
    filename = f"Расписание {date_format}.pdf"
    desktop_path = Path(os.environ["USERPROFILE"]) / "Desktop"
    pdf_file = f"{str(desktop_path)}\\{filename}"

    """Save schedule on desktop"""
    with open(pdf_file, 'wb') as output_file:
        output_file.write(pdf_file_link.content)

    """Delete old schedule's on desktop if exist"""
    os.chdir(desktop_path)
    file = sorted([[str(os.path.getctime(f)), f] for f in os.listdir(desktop_path) if f.startswith('Расписание')])
    file.pop(-1)
    if len(file) >= 1:
        for i in file:
            os.remove(i[1])

    # """Make autorun, if no need - delete link on this path, and write to the developer"""
    # autorun_path = Path(os.environ["USERPROFILE"]) / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
    # if prog_path != autorun_path:
    #     os.chdir(prog_path)
    #     winshell.CreateShortcut(
    #         os.path.join(autorun_path, "Schedule.lnk"),
    #         os.path.join(prog_path, "Schedule.exe"),
    #     )


if __name__ == "__main__":
    main()
