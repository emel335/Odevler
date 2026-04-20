import winreg
import sys
import tkinter as tk
from tkinter import messagebox

def check_and_set_install_flag():
    # Registry yolu (Gizli mühür)
    registry_path = r"Software\KastamonuUni_Emel_Odev"
    value_name = "IsInstalled"

    try:
        # Anahtarı açmaya çalış (Daha önce kurulmuş mu?)
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_path, 0, winreg.KEY_READ)
        value, _ = winreg.QueryValueEx(key, value_name)
        winreg.CloseKey(key)

        # Eğer değer 1 ise daha önce kurulmuştur
        if value == 1:
            root = tk.Tk()
            root.withdraw() # Boş pencereyi gizle
            messagebox.showerror("Kurulum Hatası", "HATA: Bu yazılım bu sisteme zaten bir kez kurulmuştur. Tekrar kurulamaz!")
            sys.exit() # Programı kapat

    except FileNotFoundError:
        # Anahtar bulunamadıysa ilk kez kuruluyor demektir. Mührü basalım!
        try:
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, registry_path)
            winreg.SetValueEx(key, value_name, 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)
            
          
            root = tk.Tk()
            root.withdraw()
            messagebox.showinfo("Kurulum", "Sistem kaydı oluşturuldu. İlk kurulum başarılı.")
        except Exception as e:
            print(f"Kayıt defteri hatası: {e}")

