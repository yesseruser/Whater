import weather

city = input("Zadej název města: ")
w = weather.get_current_weather(city)
weather.print_weather_info(w)