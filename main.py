from tkinter import filedialog
from PIL import Image, ImageTk
import pandas as pd
import tkinter as tk
import matplotlib.pyplot as plt

data = None
org_sig_img = None
new_sig_img = None
filter = "low"
sample_rate = 1000

channels = []
window = None

def import_csv():
    global data, channels, channel_var, channel_menu

    file = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file:
        data = pd.read_csv(file)
        # channels = list(range(data.shape[1]))
        # print(channels)
        # channel_var.set(channels[0] if channels else 0)
        #
        # channel_menu.destroy()
        # channel_menu_new = tk.OptionMenu(choice_frame, channel_var, *range(data.shape[1]))
        # channel_menu_new.grid(row=1, column=2, padx=10, pady=5)
        # channel_menu = channel_menu_new

        label_plik.config(text=f"Wybrano: {file}")


def plot_signal(signal, title):
    plt.figure(figsize=(8, 4))
    plt.plot(signal)
    # plt.title(title)
    plt.xlabel("Próbki")
    plt.ylabel("Amplituda")
    plt.grid()
    filename = title.replace(" ", "_").lower() + ".png"
    plt.savefig(filename)

def original_signal():
    global data, org_sig_img

    plot_signal(data, "orginal signal")
    obraz = Image.open("orginal_signal.png")
    width, height = obraz.size
    obraz = obraz.resize((width // 2, height // 2))
    org_sig_img = ImageTk.PhotoImage(obraz)
    label_obraz.config(image=org_sig_img)
    label_obraz_text.config(text="Oryginalny sygnał:")

    obraz2 = Image.open("images.jpeg").resize((width // 2, height // 2))
    new_sig_img = ImageTk.PhotoImage(obraz2)
    label_obraz2.config(image=new_sig_img)
    label_obraz2.image = new_sig_img
    label_obraz2_text.config(text="Przefiltrowany sygnał:")


root = tk.Tk()
root.title("Filtrowanie sygnału .csv")

main_frame = tk.Frame(root)
main_frame.pack(pady=20)
file_frame = tk.Frame(main_frame)
file_frame.pack(pady=10)
choice_frame = tk.Frame(main_frame)
choice_frame.pack(pady=10)
ok_frame = tk.Frame(main_frame)
ok_frame.pack(pady=10)
photos_frame = tk.Frame(main_frame)
photos_frame.pack()


okno_szer = 900
okno_wys = 600
ekran_szer = root.winfo_screenwidth()
ekran_wys = root.winfo_screenheight()
poz_x = (ekran_szer // 2) - (okno_szer // 2)
poz_y = (ekran_wys // 2) - (okno_wys // 2)
root.geometry(f"{okno_szer}x{okno_wys}+{poz_x}+{poz_y}")


tk.Button(file_frame, text="Wczytaj plik CSV", command=import_csv).grid(row=0, column=0, padx=0, pady=0)
label_plik = tk.Label(file_frame, text="Nie wybrano pliku")
label_plik.grid(row=1, column=0)

sample_rate_var = tk.StringVar(value="1000")
filter_type = tk.StringVar(value="low")
tk.Label(choice_frame, text="Wybierz częstotliwość:").grid(row=0, column=0, padx=10, pady=5)
tk.Entry(choice_frame, textvariable=sample_rate_var).grid(row=1, column=0, padx=10, pady=5)
tk.Label(choice_frame, text="Wybierz rodzaj filtrowania:").grid(row=0, column=1, padx=10, pady=5)
tk.OptionMenu(choice_frame, filter_type, "low", "high", "band").grid(row=1, column=1, padx=10, pady=5)


# channel_var = tk.IntVar()
# channel_var.set(0)
# channel_menu = tk.OptionMenu(choice_frame, channel_var, ())
# channel_menu.grid(row=1, column=2, padx=10, pady=5)
# tk.Label(choice_frame, text="Wybierz kanał:").grid(row=0, column=2, padx=10, pady=5)

tk.Button(ok_frame, text="Wygeneruj sygnał", command=original_signal).grid(row=0, column=0, padx=10, pady=5)

label_obraz_text = tk.Label(photos_frame)
label_obraz_text.grid(row=0, column=0, padx=10, pady=5)

label_obraz = tk.Label(photos_frame)
label_obraz.grid(row=1, column=0, padx=10, pady=5)

label_obraz2_text = tk.Label(photos_frame)
label_obraz2_text.grid(row=0, column=1, padx=10, pady=5)

label_obraz2 = tk.Label(photos_frame)
label_obraz2.grid(row=1, column=1, padx=10, pady=5)

# tk.Button(buttons_frame, text="Przycisk 1").grid(row=0, column=0, padx=5)
# tk.Button(buttons_frame, text="Przycisk 2").grid(row=0, column=1, padx=5)
# tk.Button(buttons_frame, text="Przycisk 3").grid(row=0, column=2, padx=5)

root.mainloop()
