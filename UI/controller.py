import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDyear(self):
        listaAvv = self._model.listaSighting
        listaAnni = []
        for a in listaAvv:
            if a.datetime.year not in listaAnni:
                listaAnni.append(a.datetime.year)
        for anno in listaAnni:
            self._view.ddyear.options.append(ft.dropdown.Option(anno))
        self._view.update_page()

    def fillDDshape(self, e):
        self._view.ddshape.options.clear()
        self._view.ddshape.value = None
        anno = self._view.ddyear.value
        listaShape = self._model.getShapeYear(anno)
        for s in listaShape:
            self._view.ddshape.options.append(ft.dropdown.Option(s))
        self._view.update_page()

    def handle_graph(self, e):
        anno = self._view.ddyear.value
        shape = self._view.ddshape.value
        self._model.creaGrafo(anno, shape)
        self._view.txt_result1.controls.clear()
        nNodes = self._model.getNumNodes()
        nEdges = self._model.getNumEdges()
        listaArchiMax = self._model.getArchiMax()
        self._view.txt_result1.controls.append(ft.Text(f"Numero di vertici: {nNodes}"))
        self._view.txt_result1.controls.append(ft.Text(f"Numero di archi: {nEdges}"))
        self._view.txt_result1.controls.append(ft.Text("I 5 archi di peso maggiore sono:"))
        for a in listaArchiMax:
            self._view.txt_result1.controls.append(ft.Text(f"{a[0].id} -> {a[1].id} | weight = {a[2]['weight']}"))
        self._view.update_page()

    def handle_path(self, e):
        path, costo = self._model.getBestPath()
        self._view.txt_result2.controls.clear()
        self._view.txt_result2.controls.append(ft.Text(f"Costo cammino massimo: {costo}"))
        for n in path:
            self._view.txt_result2.controls.append(ft.Text(f"{n}"))
        self._view.update_page()

