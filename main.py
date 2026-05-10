from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.core.window import Window

# Set ukuran window untuk testing di PC (opsional)
Window.size = (350, 600)

Builder.load_string('''
<CalcButton@Button>:
    font_size: '25sp'
    background_color: (0, 0, 0, 0)
    canvas.before:
        Color:
            rgba: (0.15, 0.15, 0.15, 1) if self.state == 'normal' else (0.3, 0.3, 0.3, 1)
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [20,]

<OrangeButton@Button>:
    font_size: '25sp'
    background_color: (0, 0, 0, 0)
    canvas.before:
        Color:
            rgba: (1, 0.6, 0, 1) if self.state == 'normal' else (1, 0.7, 0.2, 1)
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [20,]

<CalculatorLayout>:
    orientation: 'vertical'
    padding: 20
    spacing: 15
    canvas.before:
        Color:
            rgba: (0.05, 0.05, 0.05, 1)
        Rectangle:
            pos: self.pos
            size: self.size

    TextInput:
        id: display
        text: '0'
        font_size: '50sp'
        multiline: False
        halign: 'right'
        readonly: True
        background_color: (0, 0, 0, 0)
        foreground_color: (1, 1, 1, 1)
        size_hint_y: 0.3

    GridLayout:
        cols: 4
        spacing: 12
        
        # Baris 1
        CalcButton:
            text: 'C'
            on_press: display.text = ""
        CalcButton:
            text: 'DEL'
            on_press: display.text = display.text[:-1]
        CalcButton:
            text: '%'
            on_press: display.text += self.text
        OrangeButton:
            text: '/'
            on_press: display.text += self.text

        # Baris 2
        CalcButton:
            text: '7'
            on_press: display.text += self.text
        CalcButton:
            text: '8'
            on_press: display.text += self.text
        CalcButton:
            text: '9'
            on_press: display.text += self.text
        OrangeButton:
            text: '*'
            on_press: display.text += self.text

        # Baris 3
        CalcButton:
            text: '4'
            on_press: display.text += self.text
        CalcButton:
            text: '5'
            on_press: display.text += self.text
        CalcButton:
            text: '6'
            on_press: display.text += self.text
        OrangeButton:
            text: '-'
            on_press: display.text += self.text

        # Baris 4
        CalcButton:
            text: '1'
            on_press: display.text += self.text
        CalcButton:
            text: '2'
            on_press: display.text += self.text
        CalcButton:
            text: '3'
            on_press: display.text += self.text
        OrangeButton:
            text: '+'
            on_press: display.text += self.text

        # Baris 5
        CalcButton:
            text: '0'
            size_hint_x: 2
            on_press: display.text += self.text
        CalcButton:
            text: '.'
            on_press: display.text += self.text
        OrangeButton:
            text: '='
            on_press: root.calculate(display.text)
''')

class CalculatorLayout(BoxLayout):
    def calculate(self, expression):
        try:
            self.ids.display.text = str(eval(expression))
        except Exception:
            self.ids.display.text = "Error"

class CalculatorApp(App):
    def build(self):
        return CalculatorLayout()

if __name__ == '__main__':
    CalculatorApp().run()
