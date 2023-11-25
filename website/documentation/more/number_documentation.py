from nicegui import ui

from ..model import UiElementDocumentation


class NumberDocumentation(UiElementDocumentation, element=ui.number):

    def main_demo(self) -> None:
        ui.number(label='Number', value=3.1415927, format='%.2f',
                  on_change=lambda e: result.set_text(f'you entered: {e.value}'))
        result = ui.label()

    def more(self) -> None:
        @self.demo('Clearable', '''
            The `clearable` prop from [Quasar](https://quasar.dev/) adds a button to the input that clears the text.    
        ''')
        def clearable():
            i = ui.number(value=42).props('clearable')
            ui.label().bind_text_from(i, 'value')

        @self.demo('Number of decimal places', '''
            You can specify the number of decimal places using the `precision` parameter.
            A negative value means decimal places before the dot.
            The rounding takes place when the input loses focus,
            when sanitization parameters like min, max or precision change,
            or when `sanitize()` is called manually.
        ''')
        def integer():
            n = ui.number(value=3.14159265359, precision=5)
            n.sanitize()