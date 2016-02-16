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
    datetime(year=2016, month=2, day=2, hour=9),
    datetime(year=2016, month=2, day=4, hour=12)
)

service_recipe = [
    {
        'type': 'sedia',
        'delta_periods': [
            (timedelta(0), timedelta(minutes=30)),
            (timedelta(minutes=40), timedelta(hours=1))
        ]
    }
]


#example ...
service_occupations = [
    (
        { 'type' : 'sedia', "id" : 12 }, 
        (
            datetime(year=2016, month=2, day=2, hour=9), 
            datetime(year=2016, month=2, day=4, hour=12)
        )
    ),

]


resources = [
    {
        'type': 'sedia',
        'occupations': [],
        'id' : 1
    },
    {
        'type': 'sedia',
        'occupations': [],
        'id' : 2
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
            (time(hour=23), time(hour=0))
        ],
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
            ({'type':'sedia', 'id':1}, (datetime(2016, 2, 2, 9, 0), datetime(2016, 2, 2, 9, 30))),
            ({'type':'sedia', 'id':1}, (datetime(2016, 2, 2, 9, 40), datetime(2016, 2, 2, 10, 0)))
        ]

    ),


    #((datetime(2016, 2, 2, 9, 30), datetime(2016, 2, 2, 10, 30)),
    #((datetime(2016, 2, 2, 10, 0), datetime(2016, 2, 2, 11, 0)),
    #((datetime(2016, 2, 2, 10, 30), datetime(2016, 2, 2, 11, 30)),
    #((datetime(2016, 2, 2, 11, 0), datetime(2016, 2, 2, 12, 0)),
    #((datetime(2016, 2, 2, 23, 0), datetime(2016, 2, 3, 0, 0)),

]
