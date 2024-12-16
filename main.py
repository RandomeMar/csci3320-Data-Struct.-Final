from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError
import re
from QforBFS import QforBFS
import time


class Webpage:
    def __init__(self, url, adj=None):
        self.url = url
        self.adj = [] if not adj else adj

class Graph:
    def __init__(self, i_dict=None):
        self.g_dict = {}
        self.nodes = 0
        self.edges = 0

        if i_dict:
            for url in i_dict:
                self.g_dict[url] = Webpage(url, adj=i_dict[url])
                self.nodes += 1

    def add_vertex(self, url):
        if url not in self.g_dict:
            self.g_dict[url] = Webpage(url)
            self.nodes += 1
        return self
    
    def add_edge(self, url1, url2):
        if url1 not in self.g_dict: return self
        self.g_dict[url1].adj.append(url2)
        self.edges += 1
        return self
    
    def del_vertex(self, url):
        if url not in self.g_dict: return self
        self.g_dict.pop(url)
        self.nodes -= 1
        for i in self.g_dict:
            for j in range(len(self.g_dict[i].adj)):
                if self.g_dict[i].adj[j] == url:
                    self.g_dict[i].adj.pop(j)
                    self.edges -= 1
                    break 
        return self

    def del_edge(self, url1, url2):
        if url1 not in self.g_dict: return self
        self.g_dict[url1].adj.remove(url2)
        self.edges -= 1
        return self
    
    def print_adj(self):
        for vert in self.g_dict.values():
            print(f"{vert.url}:\n{vert.adj}")
        print()
        return self
    

def save_queue(queue: QforBFS):
    # Saves queue to queue.txt
    with open("queue.txt", 'w', encoding="utf-8") as file:
        while queue.len > 0:
            file.write(f"{queue.head.value}\n")
            queue.dequeue()
    return

def save_page(page: Webpage):
    # Saves single article page to graph.txt
    with open("graph.txt", 'a', encoding="utf-8") as file:
        file.write(f"{page.url}")
        for link in page.adj:
            file.write(f" {link}")
        file.write('\n')
    return

def load_queue(queue: QforBFS):
    # Loads queue from queue.txt
    with open("queue.txt", 'a+') as file:
        file.seek(0)
        for line in file:
            queue.enqueue(line.strip())
    return

def load_visited() -> dict:
    # Returns a dictionary with the names of already visited articles
    outp = {}
    with open("graph.txt", 'a+') as file:
        file.seek(0)
        for line in file:
            page = re.search(r"(\S+) \S+", line).group(1)
            print(f"Loaded {page}")
            outp[page] = None
    return outp

def load_graph(graph):
    # Loads graph of articles from graph.txt. Also returns the article with the most links and the article with the least links
    most_links = [0, '']
    least_links = [1000000000, '']
    with open("graph.txt", 'a+') as file:
        file.seek(0)
        for line in file:
            line = line.split()
            graph[line[0]] = [0] + line[1:]
            if most_links[0] < len(graph[line[0]]) - 1:
                most_links = [len(graph[line[0]]) - 1, line[0]]
            if least_links[0] > len(graph[line[0]]) - 1:
                least_links = [len(graph[line[0]]) - 1, line[0]]
    return most_links, least_links

def mass_enqueue(visited, queue, adj):
    # Enqueues an articles adjacency list
    for i in adj:
        if i in visited: continue
        queue.enqueue(i)
    return


def scrape():
    queue = QforBFS()
    load_queue(queue)
    if not queue.head:
        print("There is no saved queue.")
        print("When entering an article keep in mind capitilization may matter.")
        while True:
            selection = input("Please enter a wikipedia article you would like to scrape: ")
            selection = selection.replace(' ', '_')
            try:
                urlopen("https://en.wikipedia.org/wiki/" + selection)
            except HTTPError:
                print("No wikipedia article with that name exists.")
                continue
            break
        queue.enqueue(selection)
    pages = Graph()
    visited = load_visited()
    limit = 0
    while limit <= 0:
        try:
            limit = int(input("Please enter how many articles you would like to scrape: "))
            if limit <= 0: raise ValueError
        except ValueError:
            print("That is an invalid number.")

    while queue.len > 0 and pages.nodes < limit:
        url =  queue.head.value
        page = urlopen("https://en.wikipedia.org/wiki/" + url)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        contents = soup.find("div", class_="mw-content-ltr mw-parser-output")
        pages.add_vertex(url)

        for link in contents.find_all('a', href=re.compile(r"(/wiki/.*)")): # The regex pattern ensures only links to internal wikipedia pages are looked at
            new_url = link["href"].replace("/wiki/", "", 1)
            if new_url.find(':') != -1: continue # Ensures only articles are looked at
            if new_url in pages.g_dict[url].adj or new_url in visited: continue
            pages.add_edge(url, new_url)
        queue.dequeue()
        save_page(pages.g_dict[url])
        mass_enqueue(pages.g_dict, queue, pages.g_dict[url].adj)
        print(f"Scraped https://en.wikipedia.org/wiki/{url}")
        time.sleep(6 + (len(pages.g_dict[url].adj) % 7)) # Added variance to make sure bot is not easily detected
    save_queue(queue)

def analyze():
    most_linked_to = [0, '']
    most_links = []
    least_links = []
    graph = {}
    most_links, least_links = load_graph(graph)

    for i in graph.keys():
        for j in graph[i][1:]:
            if j in graph:
                graph[j][0] += 1
                if most_linked_to[0] < graph[j][0]:
                    most_linked_to = [graph[j][0], j]

    if not graph:
        print("There is no saved graph.txt file. Try scraping before analyzing.")
        return

    print("\nPrint list of articles [1]\nLook at article links [2]\nLook at article html [3]\nQuit [q]\n")
    selection = None
    while selection != 'q':
        selection = input("Please make a valid selection: ")
        if selection == '1':
            print()
            for i in graph.keys():
                print(i)
            print("\nThis is the list of articles that have been scraped so far.\n")
            print(f"Article {most_linked_to[1]} was the most linked to article with {most_linked_to[0]} articles linking to it.")
            print(f"Article {most_links[1]} was the article with the most links. It links to {most_links[0]} articles.")
            print(f"Article {least_links[1]} was the article with the least links. It links to {least_links[0]} articles.\n")
            print("Print list of articles [1]\nLook at article links [2]\nLook at article html [3]\nQuit [q]\n")
        elif selection == '2':
            while True:
                choice = input("Please type the name of the article you would like to see: ")
                if choice not in graph:
                    continue
                print()
                for i in graph[choice][1:]:
                    print(i)
                print(f"\n{choice} has {len(graph[choice]) - 1} links.\n{graph[choice][0]} articles link to this article.\n")
                break
            print("Print list of articles [1]\nLook at article links [2]\nLook at article html [3]\nQuit [q]\n")
        elif selection == '3':
            while True:
                choice = input("Please type the name of the article you would like to see: ")
                if choice not in graph:
                    continue
                page = urlopen("https://en.wikipedia.org/wiki/" + choice)
                html = page.read().decode("utf-8")
                soup = BeautifulSoup(html, "html.parser")
                print(soup.prettify()) # Keeps html indentation
                break
            print("\nPrint list of articles [1]\nLook at article links [2]\nLook at article html [3]\nQuit [q]\n")

def main():
    print("Wiki Scraper\n\nScraper [1]\nAnalyze [2]\n")
    selection = None
    while not selection:
        try:
            selection = int(input("Please make a valid selection: "))
        except ValueError:
            continue
        if selection == 1:
            return scrape()
        elif selection == 2:
            return analyze()
        selection = None

if __name__ == "__main__":
    main()