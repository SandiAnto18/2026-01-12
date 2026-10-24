
import flet as ft


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def fillAllYears(self):
        # Recupero gli anni dal Model
        years = self._model.getAllYears()

        # Popolo i due menu a tendina
        for year in years:
            self._view._ddAnno1.options.append(ft.dropdown.Option(year))
            self._view._ddAnno2.options.append(ft.dropdown.Option(year))

        self._view.update_page()

    def handleCreaGrafo(self, e):
        # Leggo gli anni selezionati
        da = self._view._ddAnno1.value
        a = self._view._ddAnno2.value

        # Costruisco il grafo
        self._model.buildGraph(da, a)

        # Pulisco i risultati precedenti
        self._view.txt_result.controls.clear()

        # Mostro il numero di nodi e archi
        self._view.txt_result.controls.append(
            ft.Text("Grafo correttamente creato:")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"Numero di nodi: {self._model.getNumNodi()}")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"Numero di archi: {self._model.getNumArchi()}")
        )

        self._view.update_page()

    def handleDettagli(self, e):
        # Pulisco i risultati precedenti
        self._view.txt_result.controls.clear()

        # Recupero le componenti connesse
        cc = self._model.TotCompConnesse()

        # Stampo il numero di componenti connesse
        self._view.txt_result.controls.append(
            ft.Text(f"Numero di componenti connesse: {len(cc)}")
        )

        # Recupero la componente più grande, ordinata per grado decrescente
        largest = self._model.getLargestComp(cc)

        # Stampo la dimensione della componente più grande
        self._view.txt_result.controls.append(
            ft.Text(f"Dimensione della componente connessa più grande/maggior numero di nodi: {len(largest)} nodi")
        )

        # Stampo tutti i nodi della componente più grande
        self._view.txt_result.controls.append(
            ft.Text("Nodi della componente più grande:")
        )

        for c in largest:
            self._view.txt_result.controls.append(
                ft.Text(f"- {c}")
            )

        # Stampo i nodi con il relativo grado
        self._view.txt_result.controls.append(
            ft.Text("Nodi ordinati per grado decrescente:")
        )

        for c in largest:
            self._view.txt_result.controls.append(
                ft.Text(f"- {c} (grado: {self._model.getDegree(c)})")
            )

        # Recupero e stampo i tre archi di peso maggiore
        topEdges = self._model.getTop3Edges()

        self._view.txt_result.controls.append(
            ft.Text("TOP 3 ARCHI DI PESO MAGGIORE:")
        )

        for i, (c1, c2, data) in enumerate(topEdges, start=1):
            self._view.txt_result.controls.append(
                ft.Text(
                    f"{i}. {c1} -- {c2}: "
                    f"({data['weight']} piloti condivisi)"
                )
            )

        # Aggiorno la pagina
        self._view.update_page()

    def handleCerca(self, e):
        pass

