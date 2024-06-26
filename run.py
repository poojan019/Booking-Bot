from booking.booking import Booking

experimental_options = {
    "detach": True
}

extension_path = [
    r"C:\WebDrivers\AdBlocker-Ultimate.crx"
]

with Booking(r"C:\WebDrivers\chromedriver-win64", False, experimental_options=experimental_options) as bot:
    bot.land_first_page()
    bot.dismiss_sign_in_info()
    bot.change_currency(currency="U.S. Dollar")
    bot.select_place_to_go(place_to_go="New York")
    bot.select_dates(check_in_date="2024-06-17", check_out_date="2024-06-23")
    bot.select_adults(count=5)
    bot.search()
    bot.apply_filters()