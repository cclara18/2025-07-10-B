import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph= nx.DiGraph()
        self._MapIdprod={}
        self._MapCat={}
        cat=DAO.getCategories()
        for c in cat:
            self._MapCat[c["category_name"]]= c["category_id"]
    def getBestPath(self, lun, start ,end):
        self._bestpath=[]
        self._bestscor=0
        parziale=[start]
        self._ricorsione(parziale, lun, end)
        return self._bestpath, self._bestscor

    def _ricorsione(self, parziale, lun, end):
        if len(parziale)== lun :
            if parziale[-1] == end and self._getscore(parziale)>self._bestscor:
                self._bestscor=self._getscore(parziale)
                self._bestpath= copy.deepcopy(parziale)
            return

        for n in self._graph.successors(parziale[-1]):
            if n not in parziale:
                parziale.append(n)
                self._ricorsione(parziale, lun, end)
                parziale.pop()

    def _getscore(self, parziale):
        score=0,
        for i in range(0, len(parziale)-1):
            score += self._graph[parziale[i]][parziale[i+1]]["weight"]
        return score



    def buildGraph(self, categoriaid, datai, dataf):
        self._graph.clear()

        nodi= DAO.getAllNodes(categoriaid)
        for n in nodi:
            self._MapIdprod[n.product_id]= n

            self._graph.add_node(n)
        archi= DAO.getAllEdges(categoriaid, datai, dataf, categoriaid, datai, dataf)

        for p in archi:
            p1=self._MapIdprod[p["p1"]]
            p2=self._MapIdprod[p["p2"]]
            q1=p1.q
            q2=p2.q
            peso= q1+q2

            if q1>q2:
                self._graph.add_edge(p2,p1, weight=peso)
            if q1<q2:
                self._graph.add_edge(p1,p2, weight= peso)
            if q1==q2:
                self._graph.add_edge(p2, p1, weight=peso)
                self._graph.add_edge(p1, p2, weight=peso)


    def getCategoriaIdByName(self, categorianome):
        return self._MapCat[categorianome]

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)


    def getDateRange(self):
        return DAO.getDateRange()

    def getNodiPiuProfittevoli(self):
        listNodesPesata = []
        for n in self._graph.nodes:
            score = 0
            for e in self._graph.in_edges(n, data=True):
                score += e[2]["weight"]
            for e in self._graph.out_edges(n, data=True):
                score -= e[2]["weight"]
            listNodesPesata.append((n, score))

        listNodesPesata.sort(key=lambda x: x[1], reverse=True)

        return listNodesPesata[0:5]

    def getnodi(self):
        return list(self._graph.nodes)