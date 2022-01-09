from datetime import datetime


class Date:

    def get_formatted_date(self) -> str:
        current_day = datetime.now().strftime('%d')
        current_month = datetime.now().strftime('%m')
        current_year = datetime.now().strftime('%Y')

        return f"{current_day}-{current_month}-{current_year}"
