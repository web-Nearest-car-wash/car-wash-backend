import json
# metro_data - наименование, широта, долгота
# car_washes - наименование, широта, долгота, адрес, номер телефона, фотографии мойки, url
# car_wash_types - наименование
# payment_method - наименование
# workingTime - открыто с, открыто до
# social_link
# services from categoryItems
days_of_week = [6, 0, 1, 2, 3, 4, 5]
output_data = {
        "metro": [],
        "car_washes": [],
        "all_types": [],
        "all_payment_methods": []
    }
def work_with_file(file):
    with open(file) as file:
        json_data = json.load(file)
        datas = json_data["data"]["items"]
        for data in datas:
            write_one_data_to_output_data(data)



def write_one_data_to_output_data(data):
    # with open("test.json") as file:
    #     data = json.load(file) # сейчас на 1 мойку
    try:
        for metro in data.get("metro"):
            output_metro_data = {
                "name": metro.get("name"),
                "longitude": metro.get("coordinates")[0],
                "latitude": metro.get("coordinates")[1]
            }
            if output_metro_data not in output_data["metro"]:
                output_data["metro"].append(output_metro_data)
    except Exception:
        pass

    car_wash_type = []
    payment_methods = []
    for feat in data.get("features"):
        if "car_wash_type" in feat.values():
            for n in range(len(feat.get("value"))):
                type_data = {"name": feat.get("value")[n].get("name")}
                if type_data not in output_data["all_types"]:
                    output_data["all_types"].append(type_data)
                car_wash_type.append(type_data)
        elif "payment_method" in feat.values():
            for n in range(len(feat.get("value"))):
                payment_data = {"name": feat.get("value")[n].get("name")}
                if payment_data not in output_data["all_payment_methods"]:
                    output_data["all_payment_methods"].append(payment_data)
                payment_methods.append(payment_data)
    carwash_data = {}
    try:
        carwash_data["name"] = data.get("title"),
        carwash_data["longitude"] = data.get("coordinates")[0],
        carwash_data["latitude"] = data.get("coordinates")[1],
        carwash_data["car_wash_type"] = car_wash_type
        carwash_data["payment_method"] = payment_methods
        carwash_data["address"] = data.get("fullAddress")
        carwash_data["phone"] = data.get("phones")[0]["value"]
        carwash_data["site"] = data.get("urls")[0]
        carwash_data["photos"] = [{"photo_url": data.get("photos")["urlTemplate"], "avatar": True}]
        for photo in data.get("photos")["items"]:
            carwash_data["photos"].append(
                {"photo_url": photo["urlTemplate"], "avatar": False}
            )

        carwash_data["working_time"] = []
        for day in range(7):
            carwash_data["working_time"].append(
                {
                    "day_of_week": days_of_week[day],
                    "opening_time": ":".join(map(str, data.get("workingTime")[day][0]["from"].values())),
                    "closing_time": ":".join(map(str, data.get("workingTime")[day][-1]["to"].values())),
                }
            )
        carwash_data["socialLinks"] = data.get("socialLinks")
        carwash_data["services"] = []
        services = data.get("topObjects")
        if services:
            services = services["categories"][0]["categoryItems"]
            for service in services:
                carwash_data["services"].append({
                    "title": service["title"],
                    "price": service["price"]
                })
    except Exception:
        pass
    output_data["car_washes"].append(carwash_data)


def write_data_to_file():
    with open('data_output.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)

def main():
    for n in range(1, 42):
        work_with_file(f'{n}.json')
        print(f'{n}.json - done')
    write_data_to_file()

main()
