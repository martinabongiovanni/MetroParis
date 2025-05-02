from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._fermate = DAO.getAllFermate() # leggo tutte le fermate dal DAO
        self._grafo = nx.DiGraph() # il grafo solitamente lo definisco privato perché non vorrei che qualcuno lo modificasse
        self._idMapFermate = {} # chiave = id_fermata, valore = fermata, così riesco ad accedere a una fermata conoscendone solo l'id
        for f in self._fermate: # ciclo su tutte le fermate per popolare la mappa di fermate
            self._idMapFermate[f.id_fermata] = f

    def getBFSNodesFromTree(self, source):
        '''
        Cerco l'albero di visita che mi viene fuori da Breadth First Search.
        Parametro source = nodo sorgente, selezionato dall'utente dal drop down
        '''
        tree = nx.bfs_tree(self._grafo, source)
        archi = list(tree.edges())
        nodi = list(tree.nodes())
        return nodi[1:] # perché escludo il nodo da cui parto

    def getDFSNodesFromTree(self, source):
        tree = nx.dfs_tree(self._grafo, source)
        nodi = list(tree.nodes())
        return nodi[1:] # perché escludo il nodo da cui parto

    def getBFSNodesFromEdges(self, source):
        archi = nx.bfs_edges(self._grafo, source)
        # questi archi sono tuple => ciclando su tale iterable di archi otterrò delle coppie di nodi
        res = [] # lista vuota in cui inserisco tutti i nodi che posso raagiungere a partire da un certo nodo source
        for u,v in archi: # u è il nodo da cui parte l'arco, quindi devo considerare solo il secondo per prendere i nodi di arrivo dei vari archi
            res.append(v)
        return res

    def getDFSNodesFromEdges(self, source):
        '''
        voglio recuperare la lista di nodi di un depth first iterando sugli archi e quindi chiamo dfs edges e ciclo sugli archi
        '''
        archi = nx.dfs_edges(self._grafo, source)
        res = []
        for u, v in archi:
            res.append(v)
        return res

    def buildGraphPesato(self):
        # Svuoto il grafo che avevo popolato precedentemente
        self._grafo.clear()
        # Aggiungo i nodi come fatto per il grafo precedente
        self._grafo.add_nodes_from(self._fermate)
        # Aggiungo gli archi con un nuovo metodo
        self.addEdgesPesati2()

    def addEdgesPesati(self):
        self._grafo.clear_edges()
        # è molto simile ad addEdges3
        self.allEdges = DAO.getAllEdges()  # prendo tutti gli archi dal DAO
        for edge in self.allEdges: # per ogni arco trovato
        # il peso sarà il numero di linee che connettono due certe fermate,
        # quindi inserisco un contatore che si aggiornerà ogni qual volta trovo un arco che collega due fermate
            u = self._idMapFermate[edge.id_stazP]
            v = self._idMapFermate[edge.id_stazA]
            if self._grafo.has_edge(u, v): # se il grafo ha già un arco che collega i nodi u e v
                # allora modifico semplicemente il peso di tale arco
                self._grafo[u][v]['weight'] += 1
            else: # altrimenti devo creare il grafo, devo inserire un arco fra quei due nodi
                self._grafo.add_edge(u, v, weight=1)
    # potrei scrivere meno codice qui modificando direttamente la query inserendo una group by (id_stazP, id_stazA)

    def addEdgesPesati2(self):
        self._grafo.clear_edges()
        allEdgesPesati = DAO.getAllEdgesPesati()
        for edge in allEdgesPesati:
            self._grafo.add_edge(self._idMapFermate[edge[0]], self._idMapFermate[edge[1]], weight=edge[2])

    def getArchiPesoMaggiore(self):
        '''
        Considero tutti gli archi e restituisco quelli con peso maggiore di 1
        '''
        edges = self._grafo.edges(data=True) # passo come parametro data=True perché mi serve prendere anche i pesi degli archi
        res = []
        for edge in edges:
            if self._grafo.get_edge_data(edge[0], edge[1])["weight"] > 1:
                res.append(f"{edge[0]} - {edge[1]} => weight: {self._grafo.get_edge_data(edge[0], edge[1])['weight']}")
        return res

    def buildGraph(self):
        # Aggiungo al grafo i nodi che nell' init ho salvato nella variabile self._fermate
        self._grafo.add_nodes_from(self._fermate)
        # Aggiungo al grafo gli archi
        self.addEdges3()

    def addEdges1(self):
        '''
        Aggiungo gli archi con doppio ciclo sui nodi testando se per ogni coppia esiste una connessione.
        Questo metodo è lentissimo!
        '''
        for u in self._fermate:
            for v in self._fermate:
                # se i nodi sono diversi e
                # se esiste una connessione tra i due nodi (oggetti di tipo fermata)
                if u != v and DAO.hasConnessione(u,v):
                    self._grafo.add_edge(u, v)
                    print(f"Aggiungo arco fra {u} e {v}")

    def addEdges2(self):
        '''
        Ciclo solo una volta e faccio una query per trovare tutti i vicini del nodo che passo come parametro.
        Molto più veloce di addEdges1!
        '''
        for u in self._fermate:
            for connessione in DAO.getVicini(u): # per ogni connessione trovata dal DAO
                v = self._idMapFermate[connessione.id_fermata] # recupero la fermata dalla mappa, conoscendo il suo id che passo come paramtreo
                self._grafo.add_edge(u, v) # aggiungo l'arco al grafo

    def addEdges3(self):
        '''
        Faccio una query unica che prende tutti gli archi e poi ciclo in questo metodo qui.
        '''
        self.allEdges = DAO.getAllEdges()  # prendo tutti gli archi dal DAO
        for edge in self.allEdges: # ciclo su tutti gli archi trovati e li aggiungo al grafo
                                   # (ottengo più archi che collegano due stessi fermate se più linee percorrono quel tratto)
            u = self._idMapFermate[edge.id_stazP]
            v = self._idMapFermate[edge.id_stazA]
            self._grafo.add_edge(u, v)

    # definisco due nodi per conoscere il numero di nodi e di archi del grafo,
    # per rispettare il principio di non dare accesso diretto al grafo dal controller
    def getNumNodi(self):
        # return self._grafo.number_of_nodes() # alternativa che mi restituisce direttamente il numero di nodi del grafo
        return len (self._grafo.nodes) # mi restituisce la lista di nodi, per sapere il numero considero la lunghezza di tale lista

    def getNumArchi(self):
        # return self._grafo.number_of_edges() # alternativa che mi restituisce direttamente il numero di archi del grafo
        return len (self._grafo.edges) # mi restituisce la lista di archi, per sapere il numero considero la lunghezza di tale lista

    @property
    def fermate(self):
        return self._fermate