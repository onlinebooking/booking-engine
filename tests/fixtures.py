from datetime import datetime, time, timedelta, date


wrong_period = (datetime(year=2016, month=2, day=2, hour=9),)



period = (
    datetime(year=2016, month=2, day=2, hour=9),
    datetime(year=2016, month=2, day=4, hour=12)
)

service_recipe = [
    {
        'type': 'sedia',
        'delta_periods': [
            (timedelta(0), timedelta(minutes=30)),
            (timedelta(minutes=30), timedelta(hours=2))
        ]
    }
]

resources = [
    {
        'type': 'sedia',
        'occupations': [],
        'availability': {
        }
    },
    {
        'type': 'sedia'
    }
]

availability = {
    'special_closing_days': [
        date(year=2016, month=9, day=22),
    ],
    'special_working_hours': {
        date(2016,4,2) : [
            (time(hour=9), time(hour=9, minute=30)),
        ]
    },
    'fixed_closing_days': [
        date(year=4, month=2, day=29),
        date(year=4, month=2, day=3)
    ],
    'week_working_hours': {
        # Martedi
        1: [
            (time(hour=0), time(hour=1)),
            (time(hour=9), time(hour=12)),
            (time(hour=14), time(hour=18)),
            (time(hour=23), time(hour=0))
        ],
        2: [
            (time(hour=0), time(hour=2)),
            (time(hour=9), time(hour=12)),
            (time(hour=14), time(hour=16))
        ],
    }
}

