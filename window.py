# coding=utf-8
import tkinter as tk
import tkinter.font as fontlib
import weather
import urllib.request

weather_key_exists = weather.get_key() != ""
names = ["Teplota:", "Pocitová teplota:", "Atmosférický tlak:", "Rychlost větru:", "Směr větru:"]
data_names = ["temp", "feels_like", "press", "speed", "deg"]
name_labels = []
value_labels = []


def show_window():
    global weather_key_exists

    def load_weather(e):
        print()
        city = city_entry.get()
        print("Načítání počasí")
        data = weather.get_current_weather(city)

        print(data)

        weather.print_weather_info(data)
        cur_label["text"] = str(data["desc"]).capitalize()
        img_req = urllib.request.urlopen(data["icon"])
        image_label.image = tk.PhotoImage(data=img_req.read())
        image_label["image"] = image_label.image
        for i in range(5):
            name_labels[i]["text"] = names[i]
            value_labels[i]["text"] = data[data_names[i]]

    def save_key(e):
        global weather_key_exists

        weather.set_key(key_entry.get())
        weather_key_exists = True
        root.destroy()
        show_window()

    def delete_key(e):
        global weather_key_exists

        weather.delete_key()
        weather_key_exists = False
        root.destroy()
        show_window()

    root = tk.Tk()
    root.title("Whater")
    root.resizable(False, False)

    label_font = fontlib.Font(family="consolas", size=14)
    entry_font = fontlib.Font(family="consolas", size=18)

    if weather_key_exists:
        city_frame = tk.Frame(width=400, height=50)
        image_frame = tk.Frame(width=200, height=250)
        table_frame = tk.Frame(width=200, height=250)
        city_frame.pack(side=tk.TOP)
        image_frame.pack(side=tk.LEFT)
        table_frame.pack(side=tk.RIGHT)

        city_label = tk.Label(master=city_frame, font=label_font, text="Název města:")
        city_entry = tk.Entry(master=city_frame, font=entry_font)
        city_label.pack(side=tk.LEFT, padx=10)
        city_entry.pack(side=tk.RIGHT)
        city_entry.bind('<Return>', load_weather)
        city_entry.bind("<Control-k>", delete_key)

        image_label = tk.Label(master=image_frame, image=tk.PhotoImage(), width=200, height=200, bg="grey")
        image_label.pack(side=tk.TOP)
        cur_label = tk.Label(master=image_frame, font=label_font, text="Jasno")
        cur_label.pack(side=tk.BOTTOM, pady=15)

        for row in range(5):
            name = tk.Label(master=table_frame, text=names[row])
            name.grid(row=row, column=0)
            name_labels.append(name)
            value = tk.Label(master=table_frame, text="")
            value.grid(row=row, column=1, padx=20, pady=10)
            value_labels.append(value)

    else:
        key_label = tk.Label(font=label_font, text="Klíč OpenWeatherMap:")
        key_entry = tk.Entry(font=entry_font)
        key_label.pack(side=tk.LEFT, padx=10)
        key_entry.pack(side=tk.RIGHT)
        key_entry.bind('<Return>', save_key)

    tk.mainloop()


show_window()
