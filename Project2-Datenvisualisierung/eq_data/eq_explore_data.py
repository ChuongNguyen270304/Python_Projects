from pathlib import Path
import json
# Liest die Daten als String und konvertiert sie in ein Python-Objekt   
path = Path('eq_data/eq_data_1_day_m1.geojson')
contents = path.read_text(encoding="utf-8")
all_eq_data = json.loads(contents)

# Eine besser lesbare Version der Datendatei erzeugen.
path = Path('eq_data/readable_eq_data.geojson')
readable_contents = json.dumps(all_eq_data, indent=4)
path.write_text(readable_contents)