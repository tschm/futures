import calendar

_bloomberg_futures_months = {
    1: "F",
    2: "G",
    3: "H",
    4: "J",
    5: "K",
    6: "M",
    7: "N",
    8: "Q",
    9: "U",
    10: "V",
    11: "X",
    12: "Z",
}


def code2name(code):
    numbers = {v: k for k, v in _bloomberg_futures_months.items()}
    try:
        return calendar.month_name[numbers[code]]
    except KeyError:
        raise KeyError(f"Unknown code: {code}. Has to be one of {list(numbers.keys())}")


def name2code(name):
    months = {calendar.month_name[k]: v for k, v in _bloomberg_futures_months.items()}

    try:
        return months[name]
    except KeyError:
        raise KeyError(f"Unknown month: {name}. Has to be one of {list(months.keys())}")
