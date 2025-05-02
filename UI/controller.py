import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCreaGrafo(self,e):
        # metodo che verrà chiamato dal view quando l'utente premerà il bottone "Crea Grafo"
        self._model.buildGraph()
        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text("Grafo correttamente creato!"))
        self._view.lst_result.controls.append(ft.Text(f"Il grafo contiene {self._model.getNumNodi()} nodi."))
        self._view.lst_result.controls.append(ft.Text(f"Il grafo contiene {self._model.getNumArchi()} archi."))
        self._view._btnCalcola.disabled = False # dopo aver creato il grafo riabilito il tasto
        self._view.update_page()

    def handleCercaRaggiungibili(self,e):
        # metodo che verrà chiamato dal view quando l'utente premerà il bottone "Cerca Raggiungibili"
            # devo poter chiamare questo metodo SOLO se il grafo è stato creato (solo se il grafo è pieno),
            # quindi modifico il view impostandolo come disabled e lo riabilito solo dopo aver creato il grafo
        # verifico che l'utente abbia selezionato correttamente una fermata di partenza
        if self._fermataPartenza is None: # non ho selezionato nulla dal dropdown
            self._view.lst_result.controls.clear()
            self._view.lst_result.controls.append(ft.Text("Attenzione! Stazione di partenza non selezionata!", color="red"))
            self._view.update_page()
            return
        # altrimenti o selezionato una stazione di partenza dal drop down e allora:
        nodes = self._model.getBFSNodesFromEdges(self._fermataPartenza) # individuo i nodi raggiungibili dalla stazione di partenza selezionata
        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text(f"Di seguito le stazioni raggiungibili a partire da {self._fermataPartenza}:", color="green"))
        for n in nodes: # ciclo sui nodi e li aggiungo uno a uno
            self._view.lst_result.controls.append(ft.Text(n))
        self._view.update_page()

    def loadFermate(self, dd: ft.Dropdown()):
        # metodo per riempire il dropdown
        fermate = self._model.fermate

        if dd.label == "Stazione di Partenza":
            for f in fermate:
                dd.options.append(ft.dropdown.Option(text=f.nome,
                                                     data=f,
                                                     on_click=self.read_DD_Partenza))
        elif dd.label == "Stazione di Arrivo":
            for f in fermate:
                dd.options.append(ft.dropdown.Option(text=f.nome,
                                                     data=f,
                                                     on_click=self.read_DD_Arrivo))

    def read_DD_Partenza(self,e):
        # metodo peer leggere l'oggetto selezionato, altrimenti leggeremmo la stringa
        print("read_DD_Partenza called ")
        if e.control.data is None:
            self._fermataPartenza = None
        else:
            self._fermataPartenza = e.control.data

    def read_DD_Arrivo(self,e):
        # metodo peer leggere l'oggetto selezionato, altrimenti leggeremmo la stringa
        print("read_DD_Arrivo called ")
        if e.control.data is None:
            self._fermataArrivo = None
        else:
            self._fermataArrivo = e.control.data
