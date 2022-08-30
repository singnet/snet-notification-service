def datetime_to_str(timestamp):
    if not timestamp or timestamp == 'None':
        return ""
    return timestamp.strftime('%Y-%m-%d %H:%M:%S')
