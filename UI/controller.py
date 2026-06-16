import datetime

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCreaGrafo(self, e):
        # pulisco l'area risultati

        self._view.txt_result.controls.clear()

        # leggo i valori dai dropdown
        categorianome = self._view._ddcategory.value
        datai= self._view._dp1.value
        dataf= self._view._dp2.value


        # controllo che l'utente abbia selezionato entrambi
        if categorianome is None:
            self._view.txt_result.controls.append(
                ft.Text("Errore: selezionare la categoria.")
            )
            self._view.update_page()
            return
        if datai is None or dataf is None:
            self._view.txt_result.controls.append(
                ft.Text("Errore: selezionare le date.")

            )
        self._view.txt_result.controls.append(
            ft.Text(f"Date selezionate correttamente.")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"star date: {datai}"))
        self._view.txt_result.controls.append(
            ft.Text(f"end date: {dataf}"))


        categoriaid = self._model.getCategoriaIdByName(categorianome)

        # costruisco il grafo
        self._model.buildGraph(categoriaid, datai, dataf)

        # dati base grafo
        n_nodi, n_archi = self._model.getGraphDetails()

        self._view.txt_result.controls.append(
            ft.Text(f"Grafo creato correttamente.")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"Numero vertici: {n_nodi}"))
        self._view.txt_result.controls.append(
            ft.Text(f"Numero archi: {n_archi}"))



        self.fillDDProdotti()
        self._view.update_page()


    def handleBestProdotti(self, e):
        listanodipp = self._model.getNodiPiuProfittevoli()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text("di seguito i nodi maggiormente profittevoli:")
        )
        for nodi in listanodipp:
            self._view.txt_result.controls.append(
                ft.Text(f"Nodi profittevoli: {nodi[0].product_name}- con: {nodi[1]} punti")
            )
        self._view.update_page()

    def handleCercaCammino(self, e):
        if self._view._txtInLun.value=="":
            self._view.txt_result.controls.append(ft.Text("Attenzione inserire un numero "))
            self._view.update_page()
            return

        try:
            lun=int(self._view._txtInLun.value)
        except ValueError:
            self._view.txt_result.controls.append(ft.Text("Inserire un numero"))
            self._view.update_page()
            return
        path, score = self._model.getBestPath(lun, self._prodStartValue, self._prodEndValue)
        if len(path)==0:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Nessun cammino trovato"))
            self._view.update_page()
            return

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"ecco l'elenco del cammino migliore")
        )
        for p in path:
            self._view.txt_result.controls.append(
                ft.Text(p)
            )
        self._view.txt_result.controls.append(
            ft.Text(f"score:{score}"))
        self._view.update_page()

    def fillDDProdotti(self):
        allProdotti= self._model.getnodi()
        nodesDDOptionStart=list(map(
            lambda x:ft.dropdown.Option(data=x, key=x.product_name, on_click=self._choiceProdStart),
            allProdotti))
        nodesDDOptionEnd = list(map(
            lambda x: ft.dropdown.Option(data=x, key=x.product_name, on_click=self._choiceProdEnd),
            allProdotti))
        self._view._ddProdStart.options=nodesDDOptionStart
        self._view._ddProdEnd.options = nodesDDOptionEnd

        self._view.update_page()

    def _choiceProdStart(self,e):
            self._prodStartValue=e.control.data

    def _choiceProdEnd(self,e):
            self._prodEndValue=e.control.data







    def setDates(self):
        first, last = self._model.getDateRange()

        self._view._dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view._dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp2.current_date = datetime.date(last.year, last.month, last.day)
