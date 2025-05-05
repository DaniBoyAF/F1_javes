import struct

def parse_session_packet(data):
    weather = struct.unpack_from('B', data, 52)[0]
    track_temp = struct.unpack_from('b', data, 53)[0]
    air_temp = struct.unpack_from('b', data, 54)[0]

    weather_map = {
        0: "Céu limpo", 1: "Poucas nuvens", 2: "Nublado",
        3: "Chuva leve", 4: "Chuva forte"
    }

    return {
        "clima": weather_map.get(weather, "Desconhecido"),
        "temperatura_pista": track_temp,
        "temperatura_ar": air_temp
    }

def parse_car_status_packet(data):
    carros = []
    for i in range(22):
        offset = 60 + (i * 60)
        tyre_wear = struct.unpack_from('4B', data, offset + 40)
        tyre_temp = struct.unpack_from('4B', data, offset + 48)
        actual_temp = struct.unpack_from('4B', data, offset + 52)

        carros.append({
            "id": i,
            "desgaste_pneus": list(tyre_wear),
            "temperatura_pneus": list(tyre_temp),
            "temperatura_pneus_real": list(actual_temp)
        })
    return carros
