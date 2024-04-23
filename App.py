import tkinter
import requests
from bs4 import BeautifulSoup

class App(tkinter.Tk):
    def __init__(self, screenName: str | None = None, baseName: str | None = None, className: str = "Tk", useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)
        self.title("Scraper")
        self.geometry("450x600")

        # [ NEEDED VARIABLES ]
        self.linkList: list = []

        self.mainFrame = tkinter.Frame(self.master, background="#914444")
        self.mainFrame.grid(row=0, column=0, padx=20, pady=20)
        
        # Change the size of the text field
        text_width = 40  # Adjust as needed
        button_width = 20  # Adjust as needed
        self.SearchText = tkinter.Entry(self.mainFrame, width=text_width)
        self.SearchText.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)  # Fill the available space
        # button
        self.SearchButton = tkinter.Button(self.mainFrame, text="Search", width=button_width, command=self.search)
        self.SearchButton.pack(side=tkinter.RIGHT, fill=tkinter.BOTH, expand=True, padx=10)
        
    def search(self, pull: int = 5):
        res = requests.get(f"https://en.wikipedia.org/w/index.php?title=Special:Search&limit={pull}&offset=0&ns0=1&search={self.SearchText.get()}",
                        proxies={"http":"152.67.9.179:8100",
                                    "https":"152.67.9.179:8100"}, timeout=20)
        content = res.text
        
        soup = BeautifulSoup(content, 'lxml')
        tags = soup.find_all('div', class_="searchresult")
        heading = soup.find_all('div', class_="mw-search-result-heading")
        links = soup.find_all("a")

        for link in links:
            extracted_link = link.get("href")
            print(extracted_link)

        for tag in tags:
            print(tag.text)

        results_window = tkinter.Toplevel(self)
        results_window.title("Search Results")
        results_window.geometry("1000x600") 

        linkLabel = tkinter.Label(results_window, text="Links")
        linkLabel.grid(row=0, column=0, padx=10, pady=10)
        text_width = 40  # Adjust as needed
        text_height = 20  # Adjust as needed
        self.SearchOutput = tkinter.Text(results_window, width=text_width, height=text_height,
                                         wrap=tkinter.WORD)
        self.SearchOutput.grid(row=1, column=0, padx=10, pady=10) # Fill the available space

        # [ LINKS ]
        for link in links:
            extracted_link = link.get("href")
            if list(extracted_link)[0] == "h":
                self.SearchOutput.insert(tkinter.END, extracted_link + "\n")
                self.linkList.append(extracted_link)
        
        # [ CREATE A BUTTON TO SCRAPE OTHER LINKS THAT HAD BEEN FOUND ]
        button1 = tkinter.Button(results_window, text="Scrape This Links", width=20, command=self.scrapeAll)
        button1.grid(row=3, column=0, padx=10, pady=10)

    def scrapeAll(self):
        # [ SCRAPE THE OTHER LINKS THAT HAVE BEEN FOUND ]
        for i, link in enumerate(self.linkList):
            try:
                new_res = requests.get(link, proxies={
                    "http": "20.37.207.8:8080",
                    "https": "20.37.207.8:8080"
                }, timeout=20)

                new_content = new_res.text
                # [ WRITE TO HTML FILES ]
                with open(f"link{i}.html", "w") as html_file:
                    html_file.write(new_content)
                new_soup = BeautifulSoup(new_content, "lxml")
            except:
                print("error")
            finally:
                continue


if __name__ == "__main__":
    app = App()
    app.mainloop()
