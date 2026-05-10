from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

# Set background aplikasi menjadi warna gelap yang elegan
Window.clearcolor = get_color_from_hex('#1E1E1E')

class CalculatorApp(App):
    def build(self):
        self.operators = ["/", "*", "+", "-"]
        self.last_was_operator = None
        self.last_button = None
        
        main_layout = BoxLayout(orientation="vertical", padding=15, spacing=10)
        
        # Layar input/output
        self.solution = TextInput(
            multiline=False, 
            readonly=True, 
            halign="right", 
            font_size=60,
            background_color=get_color_from_hex('#2D2D2D'),
            foreground_color=get_color_from_hex('#FFFFFF'),
            size_hint=(1, 0.3)
        )
        main_layout.add_widget(self.solution)
        
        # Grid untuk tombol-tombol
        grid = GridLayout(cols=4, spacing=5, size_hint=(1, 0.7))
        
        buttons = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            ["C", "0", ".", "+"],
        ]
        
        for row in buttons:
            for label in row:
                # Memberikan warna beda untuk operator dan tombol 'C'
                bg_color = '#333333'
                if label in self.operators:
                    bg_color = '#FF9500' # Warna oranye ala iOS
                elif label == 'C':
                    bg_color = '#FF3B30' # Warna merah untuk Clear
                
                button = Button(
                    text=label,
                    font_size=30,
                    background_normal='',
                    background_color=get_color_from_hex(bg_color),
                    color=get_color_from_hex('#FFFFFF')
                )
                button.bind(on_press=self.on_button_press)
                grid.add_widget(button)
                
        main_layout.add_widget(grid)
        
        # Tombol Sama Dengan (=)
        equals_button = Button(
            text="=", 
            font_size=35,
            size_hint=(1, 0.15),
            background_normal='',
            background_color=get_color_from_hex('#34C759'), # Hijau
            color=get_color_from_hex('#FFFFFF')
        )
        equals_button.bind(on_press=self.on_solution)
        main_layout.add_widget(equals_button)

        return main_layout

    def on_button_press(self, instance):
        current = self.solution.text
        button_text = instance.text

        if button_text == "C":
            self.solution.text = ""
        else:
            if current and (self.last_was_operator and button_text in self.operators):
                return
            elif current == "" and button_text in self.operators:
                return
            else:
                new_text = current + button_text
                self.solution.text = new_text
        
        self.last_button = button_text
        self.last_was_operator = self.last_button in self.operators

    def on_solution(self, instance):
        text = self.solution.text
        if text:
            try:
                # Menggunakan eval untuk kalkulasi string matematika
                self.solution.text = str(eval(self.solution.text))
            except Exception:
                self.solution.text = "Error"

if __name__ == "__main__":
    CalculatorApp().run()
