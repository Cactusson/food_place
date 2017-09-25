levels = [
    {
        'info_dict': {
          'title': 'LEVEL 1',
          'text': (
            "Here's some text that explains how to play and stuff.",
            "Good luck, you fucker.",
            ),
          'buttons': ('START',)
        },
        'tables': (('none', 'none'),
                   ('none', 'none'),),
        'time': '00:45',
        'customers': ((2000, ('red',)),
                      (5000, ('red', 'red')),
                      (10000, ('red', 'blue')),
                      (2000, ('blue',)),
                      (10000, ('blue', 'red'))),
        'goal': 1000,
    },
    {
        'info_dict': {
          'title': 'LEVEL 2',
          'text': (
            "You can expect a fucking UFO to arrive in your shitty cafe.",
            ),
          'pic': 'UFO',
          'buttons': ('START',)
        },
        'tables': (('none', 'none'),
                   ('none', 'blue'),
                   ('none', 'none', 'red', 'blue'),),
        'time': '01:00',
        'customers': ((2000, ('red',)),
                      (3000, ('blue', 'blue')),
                      (6000, ('red', 'blue', 'red', 'blue')),
                      (4000, ('blue',)),
                      (1000, ('blue', 'blue')),
                      (8000, ('red', 'red', 'red')),
                      (4000, ('blue', 'red')),
                      (8000, ('blue', 'blue'))),
        'ufo': (40000,),
        'goal': 2000,
    },
    {
        'info_dict': {
          'title': 'LEVEL 3',
          'text': (
            "You're doing pretty good there.",
            ),
          'buttons': ('START',)
        },
        'tables': (('none', 'red'),
                   ('none', 'none'),
                   ('none', 'red', 'red', 'none'),
                   ('red', 'red', 'blue', 'none')),
        'time': '01:15',
        'customers': ((2000, ('green', 'green')),
                      (4000, ('green', 'blue')),
                      (8000, ('red', 'red', 'red', 'green')),
                      (1000, ('red',)),
                      (3000, ('green', 'blue')),
                      (6000, ('blue', 'red', 'red')),
                      (5000, ('blue', 'blue')),
                      (9000, ('blue', 'blue', 'green')),
                      (3000, ('red', 'blue', 'green')),
                      (5000, ('red', 'red')),
                      (2000, ('blue',))),
        'ufo': (30000, 60000),
        'goal': 3000,
    },
    {
        'info_dict': {
          'title': 'LEVEL 4',
          'text': (
            "If a robber comes to your place, just shoot him.",
            ),
          'buttons': ('START',)
        },
        'tables': (('green', 'none'),
                   ('red', 'none'),
                   ('none', 'green', 'green', 'red'),
                   ('none', 'red', 'blue', 'blue')),
        'time': '01:30',
        'customers': ((1000, ('red', 'green')),
                      (3000, ('blue',)),
                      (3000, ('green', 'blue', 'blue', 'green')),
                      (5000, ('red', 'red')),
                      (7000, ('green', 'blue', 'green', 'red')),
                      (2000, ('blue', 'red', 'green')),
                      (3000, ('red', 'red')),
                      (6000, ('blue', 'red', 'blue')),
                      (9000, ('red', 'blue', 'green')),
                      (1000, ('red', 'blue')),
                      (1000, ('blue', 'green')),
                      (3000, ('green',)),
                      (3000, ('blue', 'red', 'red'))),
        'ufo': (40000, 80000),
        'robber': (10000,),
        'goal': 4000,
    },
    {
        'info_dict': {
          'title': 'LEVEL 5',
          'text': (
            "The final round. Good luck!",
            ),
          'buttons': ('START',)
        },
        'tables': (('none', 'none'),
                   ('none', 'none'),
                   ('none', 'none', 'none', 'none'),
                   ('none', 'none', 'none', 'none')),
        'time': '01:45',
        'customers': ((1000, ('blue', 'blue', 'blue', 'blue')),
                      (2000, ('blue', 'red', 'green')),
                      (3000, ('green',)),
                      (4000, ('red', 'blue')),
                      (5000, ('green', 'blue', 'green', 'red')),
                      (5000, ('green', 'red', 'red')),
                      (2000, ('blue',)),
                      (2000, ('blue', 'red', 'blue')),
                      (8000, ('green', 'green', 'green')),
                      (1000, ('red', 'blue')),
                      (2000, ('blue', 'blue')),
                      (3000, ('red', 'red')),
                      (6000, ('blue', 'red', 'blue')),
                      (6000, ('green', 'blue')),
                      (1000, ('green', 'red', 'blue'))),
        'ufo': (25000, 50000, 75000),
        'robber': (40000, 70000),
        'goal': 5000,
    }
]

infinite = {
    'info_dict': {
          'title': 'INFINITE MODE',
          'text': (
            "This is the infinite mode, motherfucker.",
            "There are no time restrictions and shit.",
            "Try to get as many score points as possible."
            ),
          'buttons': ('START',)
        },
    'tables': (('none', 'red'),
               ('none', 'none'),
               ('none', 'red', 'red', 'none'),
               ('red', 'red', 'blue', 'none')),
}
