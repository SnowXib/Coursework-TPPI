from textual.containers import Container, Vertical
from textual.widgets import Button, Static, Input, DataTable
from textual.screen import Screen
from art import text2art
from textual import on

class CalcScreen(Screen):
    CSS_PATH = ['../styles/calc_screen.tcss']

    def __init__(self, calc):
        super().__init__()
        self.calc = calc

    def compose(self):

        label  = text2art("AutoTPPI", font='slant')
        
        yield Container(
            Container(
                Static(renderable=label, id='static_label'),
                id='container_head',
            ),
            Container(
                DataTable(id='datatable'),
                id='container_calc'
            ),
            Button('Экспорт', id='button_export'),
            Static(id='static_error'),
            id='container_main',
        )

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        static_error = self.query_one('#static_error', Static)

        table.add_columns("Key", "Value")

        for key, value in dict(self.calc).items():
            if key == 'error':
                if value != {}:
                    static_error.update(str(value))
                    self.add_class('error')
                    continue
            table.add_row(str(key), str(value))