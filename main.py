from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
from QforBFS import QforBFS

# NEED TO ADD PROPER QUEUE IMPLEMENTATION

class Webpage:
    def __init__(self, url, adj=None):
        self.url = url
        self.adj = [] if not adj else adj

class Graph:
    def __init__(self, i_dict=None):
        self.g_dict = {}

        if i_dict:
            for url in i_dict:
                self.g_dict[url] = Webpage(url, adj=i_dict[url])

    def add_vertex(self, url):
        if url not in self.g_dict:
            self.g_dict[url] = Webpage(url)
        return self
    
    def add_edge(self, url1, url2):
        if url1 not in self.g_dict: return self
        self.g_dict[url1].adj.append(url2)
        return self
    
    def del_vertex(self, url):
        if url not in self.g_dict: return self
        self.g_dict.pop(url)
        for i in self.g_dict:
            for j in range(len(self.g_dict[i].adj)):
                if self.g_dict[i].adj[j] == url:
                    self.g_dict[i].adj.pop(j)
                    break
            
        return self

    def del_edge(self, url1, url2):
        if url1 not in self.g_dict: return self
        self.g_dict[url1].adj.remove(url2)
        return self
    
    def BFS(self, start):
        """
        Go to the start url and grab all links

        Google.com: [Youtube, Reddit, Facebook]
        """
        queue = []
        visited = []

        visited.append(start)
        queue += self.g_dict[start].adj

        for i in queue:
            if i in visited: continue
            visited.append(i)
            queue += self.g_dict[i].adj

        print(visited)

    def print_adj(self):
        for vert in self.g_dict.values():
            print(f"{vert.url}: {vert.adj}")
        print()
        return self
    
def main():
    url = "https://en.wikipedia.org/wiki/Pirkl"
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    contents = soup.find("div", class_="mw-content-ltr mw-parser-output")

    queue = QforBFS()
    pages = Graph()
    pages.add_vertex(url)
    for link in contents.find_all('a', href=re.compile(r"/wiki/.*")):
        new_url = link["href"].replace("/wiki/", "", 1)
        if new_url in pages.g_dict[url].adj:
            continue
        pages.add_edge(url, new_url)
    pages.print_adj()
    


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