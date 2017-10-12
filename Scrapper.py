'''
--------------------------
    Python Web Scraper
--------------------------
1. Scrapes product name and product prices from newegg.com
2. Saves scraped data in a csv file of user entered name
3. Plots graph of prices on user request

Mini project in SDL
by  Dhruv Panchal
    TECOB279

'''

# Import Libraries

# For GUI creation
from Tkinter import *
# For windowed messages
import tkMessageBox
# for using spreadsheet
import csv
# for accessing html tags in websites
from bs4 import BeautifulSoup
# for acessing web using URL
import urllib
# for cleaning up text of unwanted symbols
import re
# for ploting graphs
import matplotlib.pyplot as plt

count = 0
x = []
y = []

# Creates window
root = Tk()
root.title("Python Web Scrapper")
root.geometry("250x200+200+200")

# Main function


def scrape():

    print(str(productName.get()))
    # URL that is queried
    base_url = "http://www.newegg.com/Product/ProductList.aspx?Submit=ENE&Description=" + \
        str(productName.get()) + "&Page="

    # Function to search for product name and price

    def getData(product):
        try:
            global count
            count += 1
            name = product.find("a", class_="item-title")
            name1 = re.sub('<.*?>', '', str(name))
            price = product.find("li", class_="price-current")
            # Dollar prices
            dprice = price.find("strong").string
            # Cent prices
            cprice = price.find("sup").string

            final = [name1, "$", str(dprice), str(cprice), count]

            # Data stored in CSV

            with open(str(saveName.get()), 'a') as f:
                writer = csv.writer(f)
                writer.writerow(final)

        except:
            tkMessageBox.showerror("Error", "Something went wrong. Try again")
            print("Somthing went wrong.But do not worry I handelled it.")

    for i in range(int(page.get())):
        searchUrl = base_url + str(i)
        print("Sending request for page " + str(i))
        html = urllib.urlopen(searchUrl).read()
        soup = BeautifulSoup(html, "lxml")
        products = soup.find_all("div", class_="item-container")

        for product in products:
            getData(product)

    print("Job done")
    tkMessageBox.showinfo("Status", "Job Done")

# Function to show graph


def showgraph():
    with open(str(saveName.get()), 'r') as csvfile:
        plots = csv.reader(csvfile)
        for row in plots:
            x.append(int(row[4]))
            y.append(int(row[2]))

        plt.plot(x, y, label=str(productName.get()))
        plt.xlabel('Products')
        plt.ylabel('Price in Dollars')
        plt.title('Product Prices Graph')
        plt.legend()
        plt.show()

# UI elements


# Labels
nameLabel = Label(root, text="Product Name")
pagesLabel = Label(root, text="Pages")
saveLabel = Label(root, text="Save file name")

# Buttons
scrapeButton = Button(root, text="Scrape!!!", command=scrape)
quitButton = Button(root, text="Quit", command=root.quit)
graphButon = Button(root, text="Show graph", command=showgraph)

# Input boxes
productName = StringVar()
nameEntry = Entry(root, textvariable=productName)
page = StringVar()
pageEntry = Entry(root, textvariable=page)
saveName = StringVar()
saveEntry = Entry(root, textvariable=saveName)

# UI element alignment
nameLabel.grid(row=1)
pagesLabel.grid(row=2)
saveLabel.grid(row=3)

scrapeButton.grid(row=4, column=0)
graphButon.grid(row=4, column=1)
quitButton.grid(row=5, column=0)

nameEntry.grid(row=1, column=1)
pageEntry.grid(row=2, column=1)
saveEntry.grid(row=3, column=1)

# End of UI
root.mainloop()
