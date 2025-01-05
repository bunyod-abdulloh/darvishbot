def extracter(all_medias, delimiter):
    empty_list = []
    for e in range(0, len(all_medias), delimiter):
        empty_list.append(all_medias[e:e + delimiter])
    return empty_list


warning_text = ("Илтимос, саволга жавоб берганингиздан сўнг тугмани қайта қайта босманг! Саволга жавоб берилгач бот "
                "автоматик равишда кейинги саволга ўтади. Тугмани қайта қайта босилиши натижаларни нотўғри "
                "ҳисобланишига олиб келиши мумкин!")
