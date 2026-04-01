import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Polygon as MplPolygon
import numpy as np
from csp import backtrack

# load geojson file for plot
print("Loading GeoJSON from file...")

with open("telangana_docs/telangana_district.geojson", "r", encoding="utf-8") as f:
    geojson = json.load(f)

features = geojson["features"]
print(f"Loaded {len(features)} districts.")

#detect district name key
NAME_FIELD = None
for key in ["DISTRICT", "district", "NAME_2", "name", "District", "dtname", "DT_NAME", "D_N"]:
    if key in features[0]["properties"]:
        NAME_FIELD = key
        break

if NAME_FIELD is None:
    raise ValueError("Could not find district name field.")

print(f"Using name field: '{NAME_FIELD}'")

NEIGHBORS = {
    "Adilabad": ["Kumuram Bheem Asifabad", "Nirmal"],
    "Kumuram Bheem Asifabad": ["Adilabad", "Mancherial", "Nirmal"],
    "Mancherial": ["Kumuram Bheem Asifabad", "Jagitial", "Peddapalli", "Nirmal"],
    "Nirmal": ["Adilabad", "Kumuram Bheem Asifabad", "Mancherial", "Nizamabad", "Kamareddy", "Jagitial"],
    "Nizamabad": ["Nirmal", "Kamareddy", "Medak", "Sangareddy", "Jagitial"],
    "Kamareddy": ["Nirmal", "Nizamabad", "Medak", "Sangareddy", "Siddipet", "Rajanna Sircilla"],
    "Jagitial": ["Mancherial", "Peddapalli", "Karimnagar", "Rajanna Sircilla", "Nizamabad", "Nirmal"],
    "Peddapalli": ["Mancherial", "Jagitial", "Karimnagar", "Jayashankar Bhupalpally"],
    "Jayashankar Bhupalpally": ["Peddapalli", "Karimnagar", "Siddipet", "Warangal", "Mulugu"],
    "Mulugu": ["Jayashankar Bhupalpally", "Warangal", "Bhadradri Kothagudem"],
    "Bhadradri Kothagudem": ["Mulugu", "Khammam", "Mahabubabad"],
    "Khammam": ["Bhadradri Kothagudem", "Mahabubabad", "Suryapet", "Nalgonda"],
    "Mahabubabad": ["Bhadradri Kothagudem", "Khammam", "Warangal", "Hanumakonda", "Jangoan", "Suryapet"],
    "Warangal": ["Jayashankar Bhupalpally", "Mulugu", "Mahabubabad", "Hanumakonda", "Jangoan", "Siddipet"],
    "Hanumakonda": ["Warangal", "Karimnagar", "Siddipet", "Jangoan", "Mahabubabad"],
    "Jangoan": ["Warangal", "Hanumakonda", "Siddipet", "Yadadri Bhuvanagiri", "Mahabubabad", "Suryapet"],
    "Rajanna Sircilla": ["Kamareddy", "Jagitial", "Karimnagar", "Siddipet"],
    "Karimnagar": ["Jagitial", "Peddapalli", "Jayashankar Bhupalpally", "Hanumakonda", "Siddipet", "Rajanna Sircilla"],
    "Medak": ["Nizamabad", "Kamareddy", "Sangareddy", "Siddipet", "Medchal Malkajgiri", "Vikarabad", "Rangareddy"],
    "Sangareddy": ["Nizamabad", "Kamareddy", "Medak", "Vikarabad", "Rangareddy", "Medchal Malkajgiri"],
    "Siddipet": ["Kamareddy", "Rajanna Sircilla", "Karimnagar", "Hanumakonda", "Jayashankar Bhupalpally","Jangoan", "Yadadri Bhuvanagiri", "Medchal Malkajgiri", "Medak", "Warangal"],
    "Yadadri Bhuvanagiri": ["Siddipet", "Jangoan", "Suryapet", "Nalgonda", "Medchal Malkajgiri","Rangareddy"],
    "Suryapet": ["Jangoan", "Mahabubabad", "Khammam", "Nalgonda", "Yadadri Bhuvanagiri"],
    "Nalgonda": ["Suryapet", "Khammam", "Yadadri Bhuvanagiri", "Rangareddy", "Medchal Malkajgiri", "Mahabubnagar"],
    "Rangareddy": ["Sangareddy", "Medchal Malkajgiri", "Hyderabad", "Vikarabad", "Mahabubnagar", "Nalgonda", "Medak","Yadadri Bhuvanagiri","Nagarkurnool"],
    "Hyderabad": ["Rangareddy", "Medchal Malkajgiri"],
    "Medchal Malkajgiri": ["Medak", "Sangareddy", "Siddipet", "Yadadri Bhuvanagiri","Nalgonda", "Rangareddy", "Hyderabad"],
    "Vikarabad": ["Sangareddy", "Rangareddy", "Mahabubnagar", "Narayanpet", "Medak"],
    "Mahabubnagar": ["Rangareddy", "Vikarabad", "Narayanpet", "Wanaparthy", "Nagarkurnool", "Nalgonda"],
    "Nagarkurnool": ["Mahabubnagar", "Wanaparthy", "Jogulamba Gadwal", "Nalgonda","Rangareddy"],
    "Wanaparthy": ["Mahabubnagar", "Nagarkurnool", "Jogulamba Gadwal", "Narayanpet"],
    "Jogulamba Gadwal": ["Wanaparthy", "Nagarkurnool", "Narayanpet"],
    "Narayanpet": ["Vikarabad", "Mahabubnagar", "Wanaparthy", "Jogulamba Gadwal"],
}

DISTRICTS = list(NEIGHBORS.keys())
COLORS = ["red", "green", "blue", "yellow"]

domain = {s: COLORS for s in DISTRICTS}
solution = backtrack(DISTRICTS, domain, NEIGHBORS, {})

if not solution:
    raise Exception("No solution found!")

print("CSP solved!")
#plotting
COLOR_HEX = {
    "red": "#E05252",
    "green": "#52A852",
    "blue": "#5278E0",
    "yellow": "#D4C230",
    None: "#cccccc",
}

fig, ax = plt.subplots(figsize=(13, 12))

for feature in features:
    district = feature["properties"][NAME_FIELD]
    color_key = solution.get(district)
    face_color = COLOR_HEX.get(color_key, "#cccccc")

    geom = feature["geometry"]
    polys = []
    if geom["type"] == "Polygon":
        polys = [geom["coordinates"][0]]
    elif geom["type"] == "MultiPolygon":
        polys = [p[0] for p in geom["coordinates"]]

    all_x, all_y = [], []
    for coords in polys:
        pts = np.array(coords)
        patch = MplPolygon(pts, closed=True)
        ax.add_patch(patch)
        patch.set_facecolor(face_color)
        patch.set_edgecolor("white")
        patch.set_linewidth(0.8)
        all_x.extend(pts[:, 0])
        all_y.extend(pts[:, 1])

    if all_x and all_y:
        cx = np.mean(all_x)
        cy = np.mean(all_y)
        ax.text(cx, cy, district, ha='center', va='center',
        fontsize=5, color='white', fontweight='bold')

ax.autoscale_view()
ax.set_aspect('equal')
ax.axis('off')
ax.set_title("Telangana CSP Map Coloring", fontsize=14)

legend_patches = [
    mpatches.Patch(color=COLOR_HEX["red"], label="Color 1"),
    mpatches.Patch(color=COLOR_HEX["green"], label="Color 2"),
    mpatches.Patch(color=COLOR_HEX["blue"], label="Color 3"),
    mpatches.Patch(color=COLOR_HEX["yellow"], label="Color 4"),
]
ax.legend(handles=legend_patches, loc="lower left")

plt.tight_layout()
plt.savefig("telangana_docs/telangana_csp_map.png")
plt.show()
