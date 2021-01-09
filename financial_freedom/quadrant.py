"""
TODO:
- Add each source of income per quadrant
- Stocks: substract prev month capital gain
    - Oct 25th, total: $121,580.67, gain: +$69,642.79
- Add a expected lifetime for each source (1y for employee)
- Add other people's rates
"""
SELF_EMPLOYEE_RATE = (9000 / 160)
BUSINESS_OWNER_AVAILABLE_DAILY_HOURS = 1

QUADRANTS = {
    "employee": {},
    "self-employee": {
        "rings": {
            "income": (110000 / 12),
            "start_date": "08/01/20",
            "life_expectancy": "1 year"
        }
    },
    "business_owner": {},
    "investor": {
        "stocks": {
            'drive_wealth': 'tech companies'
        },
        "real_estate": {
            'don_mateo': {},
            'ameghino': {}
        },
        "businesses": {

        }
    },
}
