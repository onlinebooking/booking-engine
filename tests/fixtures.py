from datetime import datetime, time, timedelta, date

galactic_service_recipe = [
    {
        'type': 'lasergun',
        'delta_periods': [
            (timedelta(0), timedelta(minutes=30)),
            (timedelta(minutes=40), timedelta(hours=1)),
        ]
    },
    {
        'type': 'laserblade',
        'delta_periods': [
            (timedelta(0), timedelta(minutes=30)),
            (timedelta(minutes=40), timedelta(hours=1)),
            (timedelta(hours=1, minutes=20), timedelta(hours=1, minutes=30)),
        ]
    },
    {
        'type': 'starship',
        'delta_periods': [
            (timedelta(0), timedelta(minutes=30)),
            (timedelta(minutes=45), timedelta(minutes=50)),
        ]
    }
]

wrong_period = (datetime(year=2016, month=2, day=2, hour=9),)

period = (
    # Martedi
    datetime(year=2016, month=2, day=2, hour=9),
    # Giovedi
    datetime(year=2016, month=2, day=4, hour=12),
)

service_recipe = [
    {
        'type': 'sedia',
        'delta_periods': [
            (timedelta(0), timedelta(minutes=30)),
            (timedelta(minutes=40), timedelta(hours=1)),
        ]
    },
    {
        'type': 'hairdresser',
        'delta_periods': [
            (timedelta(minutes=30), timedelta(hours=1)),
        ]
    }
]

resources = [
    {
        'type': 'sedia',
        'occupations': [],
        'id': 1,
    },
    {
        'type': 'sedia',
        'occupations': [],
        'id': 2,
    },
    {
        'type': 'hairdresser',
        'occupations': [],
        'availability': {
            # Hollidays
            'special_closing_days': [
                date(2016, 2, 2)
            ],
        },
        'id': 3,
        'name': 'Vanessa',
        'age': 18,
    },
    {
        'type': 'hairdresser',
        'occupations': [
            (datetime(2016, 2, 2, 10, 30), datetime(2016, 2, 2, 12)),
        ],
        'id': 4,
        'name': 'Janice',
        'age': 23,
    }
]

availability = {
    'special_closing_days': [
        date(year=2016, month=9, day=22),
    ],
    'special_working_hours': {
        date(2016, 4, 2): [
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
            (time(hour=9), time(hour=11)),
            (time(hour=23), time(hour=0))
        ],
        # Mercoledi
        2: [
            (time(hour=0), time(hour=2)),
            (time(hour=9), time(hour=12)),
            (time(hour=14), time(hour=16))
        ],
    }
}

expected_ranges = [

    (
        (datetime(2016, 2, 2, 9, 0), datetime(2016, 2, 2, 10, 0)),
        [
            (
                {'type': 'sedia', 'id': 1},
                (datetime(2016, 2, 2, 9, 0), datetime(2016, 2, 2, 9, 30))
            ),
            (
                {'type': 'sedia', 'id': 1},
                (datetime(2016, 2, 2, 9, 40), datetime(2016, 2, 2, 10, 0))
            ),
            (
                {'type': 'hairdresser', 'id': 4, 'name': 'Janice', 'age': 23},
                (datetime(2016, 2, 2, 9, 30), datetime(2016, 2, 2, 10, 0))
            )
        ]
    ),
    (
        (datetime(2016, 2, 2, 9, 20), datetime(2016, 2, 2, 10, 20)),
        [
            (
                {'type': 'sedia', 'id': 1},
                (datetime(2016, 2, 2, 9, 20), datetime(2016, 2, 2, 9, 50))
            ),
            (
                {'type': 'sedia', 'id': 1},
                (datetime(2016, 2, 2, 10, 0), datetime(2016, 2, 2, 10, 20))
            ),
            (
                {'type': 'hairdresser', 'id': 4, 'name': 'Janice', 'age': 23},
                (datetime(2016, 2, 2, 9, 50), datetime(2016, 2, 2, 10, 20))
            )
        ]
    ),
    (
        (datetime(2016, 2, 2, 23, 0), datetime(2016, 2, 3, 0, 0)),
        [
            (
                {'type': 'sedia', 'id': 1},
                (datetime(2016, 2, 2, 23, 0), datetime(2016, 2, 2, 23, 30))
            ),
            (
                {'type': 'sedia', 'id': 1},
                (datetime(2016, 2, 2, 23, 40), datetime(2016, 2, 3, 0, 0))
            ),
            (
                {'type': 'hairdresser', 'id': 4, 'name': 'Janice', 'age': 23},
                (datetime(2016, 2, 2, 23, 30), datetime(2016, 2, 3, 0, 0))
            )
        ]
    ),
]
