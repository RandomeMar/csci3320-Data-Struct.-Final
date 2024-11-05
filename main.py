
class Webpage:
    def __init__(self, url):
        self.url = url
        self.adj = []

class Graph:
    def __init__(self):
        self.g_dict = {}

    def add_vertex(self, url):
        if url not in self.g_dict:
            self.g_dict[url] = Webpage(url)
        return self
    
    def add_edge(self, url1, url2):
        if url1 not in self.g_dict or url2 not in self.g_dict: return self
        self.g_dict[url1].adj.append(url2)
        self.g_dict[url2].adj.append(url1)
        return self
    
    def del_vertex(self, url):
        pass

    def del_edge(self, url1, url2):
        self.g_dict[url1].adj.remove(url2)
        self.g_dict[url2].adj.remove(url1)

    def print_adj(self):
        for vert in self.g_dict.values():
            print(f"{vert.url}: {vert.adj}")
        return self

graph = Graph()

graph.add_vertex("Google.com").add_vertex("Youtube.com").add_edge("Google.com", "Youtube.com")

graph.print_adj()