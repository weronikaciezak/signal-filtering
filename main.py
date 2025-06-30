from scipy import signal
from tkinter import filedialog, messagebox
import tkinter as tk
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import firwin, lfilter

data = None
filtered_signal = None
org_sig_img = None
new_sig_img = None

def import_csv():
    global data, channel_var, channel_menu

    file = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file:
        data = pd.read_csv(file, delimiter=';', header=None)
        channels = list(range(1, len(data.columns) + 1))
        channel_var.set(channels[0] if channels else 0)

        channel_menu.destroy()
        channel_menu_new = tk.OptionMenu(choice_frame, channel_var, *channels)
        channel_menu_new.grid(row=1, column=2, padx=10, pady=5)
        channel_menu = channel_menu_new

        label_file.config(text=f"Wybrano: {file}")
        label_sample_rate.config(text=f"Liczba próbek: {data.shape[0]}, Liczba kanałów: {data.shape[1]}")

def save_csv():
    if filtered_signal is None:
        messagebox.showerror("Błąd", "Najpierw wygeneruj sygnał.")
        return

    file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file:
        try:
            filtered_signal.to_csv(file, index=False, sep=';')
            messagebox.showinfo("Sukces", "Plik został zapisany pomyślnie.")
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie można zapisać pliku: {e}")


def plot_signal(signal, time, title):
    plt.figure(figsize=(8, 4))
    plt.plot(time, signal)
    plt.xlabel('Czas [s]')
    plt.ylabel('Amplituda')
    plt.title('Oscylogram sygnału')
    plt.grid(True)
    filename = title.replace(" ", "_").lower() + ".png"
    plt.savefig(filename)
    plt.close()

def filter_signal():
    global filtered_signal

    sig = data[channel_var.get() - 1]
    filter_type = filter_kind.get()
    window_type = window_var.get()

    fs = float(sample_rate.get())
    N = sig.shape[0]
    t = np.arange(N) / fs
    numtaps = 101

    window_dict = {
        "hamming": "hamming",
        "hanning": "hann",
        "blackman": "blackman",
        "gauss": ("gaussian", 7),
        "bartlett": "bartlett",
        "prostokątne": "boxcar",
    }

    if filter_type == "filtrowanie przez średnią krocząca":
        window_values = signal.windows.get_window(window_dict[window_type], numtaps)
        fir_coeff = window_values / np.sum(window_values)

    elif filter_type == "filtrowanie SINC":
        cutoff = 0.1
        win = window_dict[window_type]
        fir_coeff = firwin(numtaps, cutoff, window=win)

    elif filter_type == "filtrowanie przez splot":
        window_values = signal.windows.get_window(window_dict[window_type], 3)
        fir_coeff = np.zeros(numtaps)
        fir_coeff[:3] = window_values / np.sum(window_values)

    else:
        raise ValueError("Nieznany typ filtru.")

    filtered_signal = lfilter(fir_coeff, 1.0, sig)
    plot_signal(filtered_signal, t,"filtered signal")


def generate_signal():
    global data, org_sig_img

    if data is None and channel_var is not None:
        messagebox.showerror("Błąd", "Najpierw wczytaj plik CSV.")
        return

    signal = data[channel_var.get() - 1]
    N = signal.shape[0]
    fs = float(sample_rate.get())

    time = [i / fs for i in range(N)]

    plot_signal(signal, time, "orginal signal")
    obraz = Image.open("orginal_signal.png")
    width, height = obraz.size
    obraz = obraz.resize((width // 2, height // 2))
    org_sig_img = ImageTk.PhotoImage(obraz)
    label_obraz.config(image=org_sig_img)
    label_obraz_text.config(text="Oryginalny sygnał:")

    filter_signal()
    obraz2 = Image.open("filtered_signal.png").resize((width // 2, height // 2))
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
label_file = tk.Label(file_frame, text="Nie wybrano pliku")
label_file.grid(row=1, column=0)
label_sample_rate = tk.Label(file_frame, text="")
label_sample_rate.grid(row=2, column=0)

sample_rate = tk.StringVar(value="1")
tk.Label(choice_frame, text="Podaj próbkowanie:").grid(row=0, column=0, padx=10, pady=5)
tk.Entry(choice_frame, textvariable=sample_rate).grid(row=1, column=0, padx=10, pady=5)

filter_kind = tk.StringVar(value="filtrowanie przez średnią krocząca")
tk.Label(choice_frame, text="Wybierz rodzaj filtrowania:").grid(row=0, column=1, padx=10, pady=5)
tk.OptionMenu(choice_frame, filter_kind, "filtrowanie przez średnią krocząca", "filtrowanie SINC", "filtrowanie przez splot").grid(row=1, column=1, padx=10, pady=5)

window_var = tk.StringVar(value="prostokątne")
tk.Label(choice_frame, text="Wybierz okno:").grid(row=0, column=3, padx=10, pady=5)
tk.OptionMenu(choice_frame, window_var, "hamming", "hanning", "blackman", "gauss", "bartlett", "prostokątne").grid(row=1, column=3, padx=10, pady=5)

channel_var = tk.IntVar()
channel_var.set(0)
channel_menu = tk.OptionMenu(choice_frame, channel_var, ())
channel_menu.grid(row=1, column=2, padx=10, pady=5)
tk.Label(choice_frame, text="Wybierz kanał:").grid(row=0, column=2, padx=10, pady=5)

tk.Button(ok_frame, text="WYGENERUJ SYGNAŁ", command=generate_signal).grid(row=0, column=0, padx=10, pady=5)

label_obraz_text = tk.Label(photos_frame)
label_obraz_text.grid(row=0, column=0, padx=10, pady=5)

label_obraz = tk.Label(photos_frame)
label_obraz.grid(row=1, column=0, padx=10, pady=5)

label_obraz2_text = tk.Label(photos_frame)
label_obraz2_text.grid(row=0, column=1, padx=10, pady=5)

label_obraz2 = tk.Label(photos_frame)
label_obraz2.grid(row=1, column=1, padx=10, pady=5)

tk.Button(ok_frame, text="Zapisz sygnał do pliku", command=save_csv).grid(row=0, column=1, padx=10, pady=5)

root.mainloop()
