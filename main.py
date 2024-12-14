from bs4 import BeautifulSoup
from urllib.request import urlopen
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
    with open("queue.txt", 'w') as file:
        while queue.len > 0:
            file.write(f"{queue.head.value}\n")
            queue.dequeue()
    return
def save_page(page: Webpage):
    with open("graph.txt", 'a') as file:
        file.write(f"{page.url}")
        for link in page.adj:
            file.write(f" {link}")
        file.write('\n')
    return
def load_queue(queue: QforBFS):
    with open("queue.txt", 'a+') as file:
        file.seek(0)
        for line in file:
            queue.enqueue(line.strip())
    return
def load_graph() -> dict:
    outp = {}
    with open("graph.txt", 'r') as file:
        for line in file:
            line = line.split()
            outp[line[0]] = line[1:]
    return outp


def mass_enqueue(visited, queue, adj):
    for i in adj:
        if i in visited: continue
        queue.enqueue(i)
    return
    
def main():
    queue = QforBFS()
    load_queue(queue)
    if not queue.head:
        queue.enqueue("pirkl")
    pages = Graph()
    visited = load_graph()

    while queue.len > 0 and pages.nodes <= 1:
        url =  queue.head.value
        page = urlopen("https://en.wikipedia.org/wiki/" + url)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        contents = soup.find("div", class_="mw-content-ltr mw-parser-output")
        

        # NEED: Add check for if url is a valid wiki page

        pages.add_vertex(url)

        for link in contents.find_all('a', href=re.compile(r"(/wiki/.*)")):
            new_url = link["href"].replace("/wiki/", "", 1)
            if new_url.find(':') != -1: continue
            if new_url in pages.g_dict[url].adj: continue
            pages.add_edge(url, new_url)
        queue.dequeue()
        save_page(pages.g_dict[url])
        mass_enqueue(pages.g_dict, queue, pages.g_dict[url].adj)
        print(url + '\n')
        
        print(pages.g_dict[url].adj)
        
        time.sleep(7 + (len(pages.g_dict[url].adj) % 10))

    save_queue(queue)
    


if __name__ == "__main__":
    main()

# This is just for testing
temp = {
    "Google.com": ["Youtube.com", "Reddit.com", "Facebook.com"],
    "Youtube.com": ["Google.com", "Youtube.kids"],
    "Reddit.com": ["Google.com", "Reddit.com/r/apples"],
    "Facebook.com": ["Google.com", "Facebook.com/marketplace"],
    "Youtube.kids": ["Youtube.com"],
    "Reddit.com/r/apples": ["Reddit.com"],
    "Facebook.com/marketplace": ["Facebook.com"]
}

#graph = Graph(i_dict=temp)

#graph.print_adj()
#print()
#graph.BFS("Google.com")