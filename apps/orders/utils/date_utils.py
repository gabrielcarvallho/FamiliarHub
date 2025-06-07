from datetime import timedelta


class DateUtils:
    @staticmethod
    def get_next_business_day(date):
        while date.weekday() >= 5:
            date += timedelta(days=1)
        return date