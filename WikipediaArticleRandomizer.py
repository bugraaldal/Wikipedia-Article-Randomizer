from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import tkinter as tk
import re


# Defining these lists to global in order to be able to access them easily
href_matches = []
id_matches = []
article_links = []
article_names = []

# Open the articles using selenium


def open_article(articles):
    PATH = "/home/buura/Desktop/operadriver_linux64/operadriver"
    driver = webdriver.Opera(executable_path=PATH)
    driver.get(articles[1])


# A pop-up window to show the articles


def pop_up_results(amount, article_names, article_links):
    top = tk.Toplevel()  # Creating a pop-up window to show the results
    top.configure(background="white")
    top.title("Article Results")
    # Showing another message if the user input is 1.For grammar reasons
    if amount == 1:
        text = "An article was randomized"
    else:
        text = f"{amount} articles were randomized."
    tk_resultsfound_label = tk.Label(
        top, text=text, bg="white", fg="black", font="none 15")
    tk_resultsfound_label.pack(side="top")
    # A label and a button for each article
    for articles in zip(article_names, article_links):
        label = tk.Label(
            top, text=articles[0], bg="white", fg="black", font="none 12")
        # If lamba isn't used it just pops up the articles
        button = tk.Button(top, text="Read it!",
                           command=lambda articles=articles: open_article(articles))
        label.pack()
        button.pack()

# Defining the function that randomizes the articles


def randomize_article(amount=5):
    # Getting the random article button from wikipedia
    for _ in range(0, amount):
        source = requests.get(
            "https://en.wikipedia.org/wiki/Special:Random").text
        soup = BeautifulSoup(source, "lxml")
        # Getting the heading that includes the name and the href that has a part of the link
        id_matches.append(soup.find(id="firstHeading"))
        href_matches.append(soup.find('a', accesskey='e').get('href'))
    for hrefs in href_matches:
        # Fetching the link using regex and prefixing it with the wikipedia article URL
        result = re.search(r"=(.*?)&", hrefs)
        article_links.append(
            f"https://en.wikipedia.org/wiki/{result.group(1)}")
    for ids in id_matches:
        # Fetching the name
        result = re.search(r'"en">(.*?)</h1>', str(ids))
        article_names.append(result.group(1))
    print(article_names, article_links)
    pop_up_results(amount, article_names, article_links)

# The main window's functions:


class GUI_ralated:
    # Defining the basics of the window
    root = tk.Tk()
    root.title("Wikipedia Article Randomizer")
    root.geometry("780x220")

    def main_window_start(self):
        root = self.root
        TITLE = tk.Label(root, text="WIKIPEDIA RANDOMIZER", bg="white",
                         fg="black", font="none 16 bold")
        TITLE.pack(side="top")
        root.configure(background="white")
        frame = tk.Frame(root, bg="white")
        frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)
    # Creeating the input box

    def searchbar(self):
        def click():  # Defining the function of "Randomize!" button
            amount = entry.get()
            # Getting how many articles are going to be shown
            if amount.isdigit():
                randomize_article(int(amount))
            # if the user just clicks without any input, it would randomize 5 articles by default
            elif amount == "":
                randomize_article(5)
            # if user inputs an invalid value, show a message in the terminal
            else:
                print("Enter a valid value")
        root = self.root
        search = tk.Label(root, text="How many articles would you like to randomize?", bg="white",
                          fg="black", font="none 12 bold")
        entry = tk.Entry(root, width=28, fg="black",
                         bg="white", font="none 15 bold")
        searchbutton = tk.Button(
            root, text="Randomize!", height=1, pady=5, font="none 12 bold", command=click)
        amount_specify = tk.Label(
            root, text="  Specify the amount here:", font="none 12 bold", bg="white", fg="black")
        search.place(x=10, y=30)
        searchbutton.place(x=635, y=110)
        entry.place(x=250, y=110)
        amount_specify.pack(side="left")

    def main_window_end(self):
        root = self.root
        root.mainloop()


GUI = GUI_ralated()
GUI.main_window_start()
GUI.searchbar()
GUI.main_window_end()
