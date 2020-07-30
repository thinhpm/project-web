


def read_file():
    results = []
    fo = open("data_category-lazada.txt", "r", encoding="utf-8")

    data = fo.readlines()

    for item in data:
        arr = item.split(",")
        if len(arr) == 0:
            continue

        link = arr[-1]
        name = arr[0]
        if len(arr) > 2:
            name = arr[0]


        arr2 = link.split("?pos")
        slug = arr2[0].split("/")[-1]
        if len(slug) == 0:
            slug = arr2[0].split("/")[-2]

        if slug not in results:
            results.append(slug)
    print((results))

read_file()