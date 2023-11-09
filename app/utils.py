
def calculate_statistic(results, statistic_type):
    if not statistic_type:
        return None

    values = [measurement.value for measurement in results]

    if statistic_type == 'min':
        return min(values)
    elif statistic_type == 'max':
        return max(values)
    elif statistic_type == 'avg':
        return sum(values) / len(values)  if values else 0
    elif statistic_type == 'sum':
        return sum(values)
    else:
        return None