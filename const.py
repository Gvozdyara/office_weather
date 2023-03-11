refresh_token = "APJWN8dOrJmWU1Wzw7Ws0l0RNbX8cRCJXnK-0av7jqIA8J_0m9dTgjFr7zONJH9JNwEY1K_vInRoCB2IoI7sgL2wxNl7gb0fNW8YxUzXXmLN610RI1SzWOnnJ8eV7-VYE77eAsXkjq3V5wa8Bk8Rpl6TkH5h06LSUKFqZw4UN3GlkXnGbOpCRL95BnsJWT6Dmo-JxxcsTmRpUdaHDouLFyFHBh6EhbmY51abbsFqwTEVKR8szlRESyg"
key = "AIzaSyCq2oNYF_aU_OhVKS6OF0uWKMlaNq8Voos"
token_path = "token.json"

warning_ranges = {
    "exwedjrg": {
        "too_low": [0, 15],
        "low": [19, 25],
        "normal": [25, 45],
        "high": [45, 65],
        "too_high": [65, 100]
    },
    "orgmjnzw": {
        "too_low": [0, 19],
        "low": [19, 21],
        "normal": [21, 24],
        "high": [24, 26],
        "too_high": [26, 100]
    },
    "rjwyzjzg": {
        "too_low": [0, 100],
        "low": [100, 200],
        "normal": [200, 650],
        "high": [650, 950],
        "too_high": [950, 100000]
    }
  }

params = {
    "exwedjrg": "Humidity",
    "orgmjnzw": "Temperature",
    "rjwyzjzg": "Carbon dioxide"}