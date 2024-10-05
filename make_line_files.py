import csv, json

code = "SE-003-UL"

feedinfo = open(f"{code}/feed_info.txt", "r", encoding="UTF8")
feedinfo = list(csv.reader(feedinfo))

version = feedinfo[1][feedinfo[0].index("feed_version")]

def list_to_dict(headers, list):
    return_dict = dict()
    for i in range(len(list)):
        return_dict[headers[i]] = list[i]
    return return_dict

routes_dict = dict()
trips_dict = dict()
shapes_dict = dict()
stops_dict = dict()
stop_refs_dict = dict()

#special
shape_trips_dict = dict()

routes = open(f"{code}/routes.txt", "r", encoding="UTF8")
routes = csv.reader(routes)
routes = list(routes)
route_headers = list()
for route in routes:
    if route is routes[0]:
        for header in route:
            route_headers.append(header)
    else:
        routes_dict[route[0]] = list_to_dict(route_headers, route)

trips = open(f"{code}/trips.txt", "r", encoding="UTF8")
trips = csv.reader(trips)
trips = list(trips)
trip_headers = list()
prev_trip_shape = set()
for trip in trips:
    # spacial handeling of first line
    if trip is trips[0]:
        for header in trip:
            trip_headers.append(header)
    else:
        if trip[5] in prev_trip_shape:
            shape_trips_dict[trip[5]].append(list_to_dict(trip_headers, trip))
        else:
            shape_trips_dict[trip[5]] = list()
            shape_trips_dict[trip[5]].append(list_to_dict(trip_headers, trip))
            prev_trip_shape.add(trip[5])

prev_trip = set()
for i in range(190):
    # spacial handeling of first line
    trip = trips[i]
    if trip is trips[0]:
        for header in trip:
            trip_headers.append(header)
    else:
        #if trip[5] not in prev_trip:
            trips_dict[trip[0]][trip[5]] = list()
            trips_dict[trip[0]][trip[5]].append(shape_trips_dict[trip[5]])
            prev_trip.add(trip[5])
            print(prev_trip)

shapes = open(f"{code}/shapes.txt", "r", encoding="UTF8")
shapes = csv.reader(shapes)
shapes = list(shapes)
shape_headers = list()
prev_shape = None
for shape in shapes:
    if shape is shapes[0]:
        for header in shape:
            shape_headers.append(header)
    else:
        if shape[0] == prev_shape:
            shapes_dict[shape[0]].append([shape[1], shape[2]])
        else:
            shapes_dict[shape[0]] = list()
            shapes_dict[shape[0]].append([shape[1], shape[2]])
            prev_shape = shape[0]

stops = open(f"{code}/stops.txt", "r", encoding="UTF8")
stops = csv.reader(stops)
stops = list(stops)
stop_headers = list()
for stop in stops:
    if stop is stops[0]:
        for header in stop:
            stop_headers.append(header)
    else:
        stops_dict[stop[0]] = list_to_dict(stop_headers, stop)

stop_refs = open(f"{code}/stop_times.txt", "r", encoding="UTF8")
stop_refs = csv.reader(stop_refs)
stop_refs = list(stop_refs)
stop_ref_headers = list()
prev_stop_ref = None
for stop_ref in stop_refs:
    if stop_ref is stop_refs[0]:
        for header in stop_ref:
            stop_ref_headers.append(header)
    else:
        if stop_ref[0] == prev_stop_ref:
            stop_refs_dict[stop_ref[0]].append(stop_ref[3])
        else:
            stop_refs_dict[stop_ref[0]] = list()
            stop_refs_dict[stop_ref[0]].append(stop_ref[3])
            prev_stop_ref = stop_ref[0]

#export = open(f"route_{route['route_id']}.json", 'w', encoding="UTF8")
export = open(f"routes_dict.json", 'w', encoding="UTF8")
json.dump(routes_dict, export, indent=2)
export = open(f"trips_dict.json", 'w', encoding="UTF8")
json.dump(trips_dict, export, indent=2)
export = open(f"shapes_dict.json", 'w', encoding="UTF8")
json.dump(shapes_dict, export, indent=2)
export = open(f"stops_dict.json", 'w', encoding="UTF8")
json.dump(stops_dict, export, indent=2)
export = open(f"stop_refs_dict.json", 'w', encoding="UTF8")
json.dump(stop_refs_dict, export, indent=2)
export = open(f"stop_refs_dictssssssssssssssssss.json", 'w', encoding="UTF8")
json.dump(shape_trips_dict[trip[5]], export, indent=2)


print("done")
