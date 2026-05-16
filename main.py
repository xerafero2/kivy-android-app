from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.modalview import ModalView
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.utils import platform

# Warna UI Modern / Elegan
BG_COLOR = '#121212'
PANEL_COLOR = '#1E1E1E'
ACCENT_COLOR = '#BB86FC'
TEXT_COLOR = '#FFFFFF'

Window.clearcolor = get_color_from_hex(BG_COLOR)

# Profil Perangkat Nyata (Real Devices)
DEVICE_PROFILES = {
    "Poco C75 (Android 14)": "Mozilla/5.0 (Linux; Android 14; 22101316G Build/UKQ1.230917.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/120.0.6099.193 Mobile Safari/537.36",
    "Samsung A32 4G (Android 13)": "Mozilla/5.0 (Linux; Android 13; SM-A325F Build/TP1A.220624.014; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/119.0.6045.163 Mobile Safari/537.36",
    "Desktop Windows 11": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

class SettingsPanel(ModalView):
    def __init__(self, apply_callback, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.85, 0.6)
        self.background_color = get_color_from_hex(PANEL_COLOR)
        self.apply_callback = apply_callback
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        layout.add_widget(Label(
            text="Pengaturan Sesi & Fingerprint", 
            font_size=20, 
            color=get_color_from_hex(TEXT_COLOR),
            size_hint_y=None, height=40
        ))
        
        # Pilihan Perangkat
        layout.add_widget(Label(text="Pilih Profil Perangkat:", color=get_color_from_hex(TEXT_COLOR), size_hint_y=None, height=30))
        self.device_spinner = Spinner(
            text="Poco C75 (Android 14)",
            values=list(DEVICE_PROFILES.keys()),
            background_normal='',
            background_color=get_color_from_hex('#333333'),
            color=get_color_from_hex(TEXT_COLOR),
            size_hint_y=None, height=50
        )
        layout.add_widget(self.device_spinner)
        
        # Input Custom URL
        layout.add_widget(Label(text="URL Target:", color=get_color_from_hex(TEXT_COLOR), size_hint_y=None, height=30))
        self.url_input = TextInput(
            text="https://whoer.net", # Situs untuk cek fingerprint
            multiline=False,
            background_color=get_color_from_hex('#2D2D2D'),
            foreground_color=get_color_from_hex(TEXT_COLOR),
            size_hint_y=None, height=50
        )
        layout.add_widget(self.url_input)
        
        # Tombol Simpan
        save_btn = Button(
            text="Terapkan & Buka Sesi",
            background_normal='',
            background_color=get_color_from_hex(ACCENT_COLOR),
            color=get_color_from_hex('#000000'),
            size_hint_y=None, height=50
        )
        save_btn.bind(on_press=self.save_and_close)
        layout.add_widget(save_btn)
        
        self.add_widget(layout)
        
    def save_and_close(self, instance):
        selected_device = self.device_spinner.text
        user_agent = DEVICE_PROFILES[selected_device]
        url = self.url_input.text
        self.apply_callback(url, user_agent)
        self.dismiss()

class MultiSessionBrowserApp(App):
    def build(self):
        self.main_layout = BoxLayout(orientation='vertical')
        
        # Header UI
        header = BoxLayout(size_hint_y=None, height=60, padding=10, spacing=10)
        
        settings_btn = Button(
            text="[ Pengaturan Profil ]", 
            background_normal='', 
            background_color=get_color_from_hex('#333333'),
            color=get_color_from_hex(TEXT_COLOR)
        )
        settings_btn.bind(on_press=self.open_settings)
        
        close_session_btn = Button(
            text="[ Hapus Sesi ]", 
            background_normal='', 
            background_color=get_color_from_hex('#CF6679'), # Merah elegan
            color=get_color_from_hex('#000000')
        )
        close_session_btn.bind(on_press=self.clear_session)
        
        header.add_widget(settings_btn)
        header.add_widget(close_session_btn)
        self.main_layout.add_widget(header)
        
        # Area Konten WebView
        self.webview_container = BoxLayout()
        self.placeholder_label = Label(text="Buka Pengaturan Profil untuk memulai sesi baru.", color=get_color_from_hex(TEXT_COLOR))
        self.webview_container.add_widget(self.placeholder_label)
        
        self.main_layout.add_widget(self.webview_container)
        
        return self.main_layout

    def open_settings(self, instance):
        panel = SettingsPanel(apply_callback=self.launch_webview)
        panel.open()

    def launch_webview(self, url, user_agent):
        self.webview_container.clear_widgets()
        
        if platform == 'android':
            from jnius import autoclass
            from android.runnable import run_on_ui_thread
            
            WebView = autoclass('android.webkit.WebView')
            WebViewClient = autoclass('android.webkit.WebViewClient')
            CookieManager = autoclass('android.webkit.CookieManager')
            activity = autoclass('org.kivy.android.PythonActivity').mActivity
            
            @run_on_ui_thread
            def create_webview():
                webview = WebView(activity)
                webview.setWebViewClient(WebViewClient())
                
                # Konfigurasi Fingerprint (User-Agent)
                settings = webview.getSettings()
                settings.setJavaScriptEnabled(True)
                settings.setDomStorageEnabled(True)
                settings.setUserAgentString(user_agent)
                
                # Isolasi Sesi (Manajemen Cookie Independen)
                cookie_manager = CookieManager.getInstance()
                cookie_manager.setAcceptCookie(True)
                cookie_manager.setAcceptThirdPartyCookies(webview, True)
                
                webview.loadUrl(url)
                activity.setContentView(webview)
            
            create_webview()
        else:
            # Fallback untuk pengujian di Desktop/Termux tanpa GUI native Android
            lbl = Label(text=f"Mode Simulasi Desktop.\n\nTarget URL: {url}\nUser-Agent: {user_agent}", color=get_color_from_hex(TEXT_COLOR))
            self.webview_container.add_widget(lbl)

    def clear_session(self, instance):
        if platform == 'android':
            from jnius import autoclass
            from android.runnable import run_on_ui_thread
            CookieManager = autoclass('android.webkit.CookieManager')
            WebStorage = autoclass('android.webkit.WebStorage')
            
            @run_on_ui_thread
            def clear_data():
                CookieManager.getInstance().removeAllCookies(None)
                CookieManager.getInstance().flush()
                WebStorage.getInstance().deleteAllData()
                
            clear_data()
            self.webview_container.clear_widgets()
            self.webview_container.add_widget(Label(text="Sesi dan Cookie telah dibersihkan.", color=get_color_from_hex('#34C759')))
        else:
            self.webview_container.clear_widgets()
            self.webview_container.add_widget(Label(text="Sesi dibersihkan (Simulasi).", color=get_color_from_hex('#34C759')))

if __name__ == '__main__':
    MultiSessionBrowserApp().run()
