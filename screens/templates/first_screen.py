from textual.containers import Container, Vertical
from textual.widgets import Button, Static, Input
from textual.screen import Screen
from art import text2art
from textual import on

from screens.templates.calc_screen import CalcScreen
from calc import MathCalc

class FirstScreen(Screen):

    CSS_PATH = ['../styles/first_screen.tcss']

    def compose(self):
        label  = text2art("AutoTPPI", font='slant')

        yield Container(
            Container(
                Static(renderable=label, id='static_label'),
                id='container_head',
            ),
            Container(
                Static(renderable='Ошибка формы', id='static_error'),
                Container(
                    Input(placeholder='Ft в Кн', tooltip='Значение в кН, действующее на приводной барабан транспортера.', id='input_ft'),
                    Input(placeholder='V в м/c', tooltip='Скорость движения ленты в м/с.', id='input_v'),
                    Input(placeholder='D в мм', tooltip='Диаметр приводного барабана транспортера в м.', id='input_d'),
                    Input(placeholder='Передачи в необходимом формате', tooltip='Формат: [{"count": 3, "coef_gear": 0.99}]', id='input_types_gear'),
                    id='container_input'
                    ),
                id='container_body'
            ),
                Container(
                    Button('Начать работу', id='button_start'),
                    Button('Demo', id='demo_button'),
                    id='container_buttons'
                ),
            id='container_main',
        )

    @on(Button.Pressed, '#button_start')
    def on_button_start_pressed(self) -> None:
        input_ft = self.query_one('#input_ft', Input)
        input_v = self.query_one('#input_v', Input)
        input_d = self.query_one('#input_d', Input)
        input_types_gear = self.query_one('#input_types_gear', Input)

        self.add_class('error')

        if input_ft.value and input_v.value and input_d.value:
            calc = MathCalc(Ft=input_ft, V=input_v, D=input_d, types_gear=input_types_gear)
            self.app.push_screen(CalcScreen(calc=calc))
        else:
            self.add_class('error')
    
    @on(Button.Pressed, '#demo_button')
    def on_button_demo_pressed(self) -> None:
        calc = MathCalc()
        self.app.push_screen(CalcScreen(calc=calc))
