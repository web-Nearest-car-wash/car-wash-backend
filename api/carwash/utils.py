from decimal import Decimal


def cut_zeros(data):
    """Удаляет в сериализованных данныx координат лишние нули в конце"""
    data['latitude'] = '{:.10f}'.format(
            Decimal(data['latitude'])
        ).rstrip('0')
    data['longitude'] = '{:.10f}'.format(
            Decimal(data['longitude'])
        ).rstrip('0')
    return data
