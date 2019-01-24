import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
monthnames = ['january', 'february', 'march', 'april', 'may', 'june']
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter

    """

    print('Hello! Let\'s explore some US bikeshare data!')
    while True:
        city = input('Would you like to see data for Chicago, New York City, or Washington?\n').lower()
        if city in CITY_DATA:
            break
        else:
            print('Enter a valid city name')
    day = 'all'
    month = 'all'

    while True:
        month_or_day = input('Would you like to filter by month, day, or not at all?\n').lower()
        if month_or_day in ('month','day','not at all', 'none', 'no'):
            break
        else:
            print('Please enter a valid answer')
    while month_or_day == 'day':
        day = input('Which day would you like to see? Sunday, Monday, ..., Saturday\n').lower()
        if day in ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'):
            break
        else:
            print('Please enter a invalid answer')
    while month_or_day == 'month':
        month = input('Which month would you like to see? (all, January, February, ... , June)\n').lower()
        day = 'all'
        if month in monthnames:
            break
        else:
            print('Please enter a valid answer')


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
# load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

# convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

# extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

# filter by month if applicable
    if month != 'all':
    # use the index of the months list to get the corresponding int
        month = monthnames.index(month) + 1


    # filter by month to create the new dataframe
        df = df[df['month'] == month]

# filter by day of week if applicable
    if day != 'all':
    # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel.
        Includes month, day of the week, and hour"""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    print('\nMost common month:\n', monthnames[int(df['month'].mode().values[0])-1])


    print('\nMost common day of the week:\n', df['day_of_week'].mode().values[0])


    print('\nMost common hour of the day:\n', df['hour'].mode().values[0])

def station_stats(df):
    """ Displays statistics on the most common stations. A new column
     is created by joining Start Station and End Station to find the most
     common route"""


    print('\nMost Frequent Start Station:\n', df['Start Station'].mode()[0] )


    print('\nMost Frequent End Station:\n', df['End Station'].mode()[0])

    df['Route'] = df['Start Station'] + ' to ' + df['End Station']

    popular_route = df['Route'].mode()[0]

    print('\nMost Popular Route:\n', popular_route)


def trip_duration_stats(df):
    """ Displays statistics on total trip duration and average trip duration.
    Breaks seconds into bigger units """

    total_travel_time = df['Trip Duration'].sum()
    if total_travel_time >= 3600:
        print('\nTotal travel time:\n', (int(total_travel_time)// 3600), 'hours',
        ((int(total_travel_time) % 3600)//60), 'min', ((int(total_travel_time) % 3600) % 60), 'sec')
    else:
        print('\nTotal travel time:\n', (int(total_travel_time)//60), 'minutes',
        (int(total_travel_time) % 60), 'seconds')

    common_travel_time = df['Trip Duration'].mean()
    print('\nAverage travel time:\n', (int(common_travel_time)// 60), 'minutes',
    (int(common_travel_time) % 60), 'seconds')

def user_stats(df):
    """Displays statistics on user characteristics. Including user type, gender,
    most common age, and the minimum and maximum age"""

    try:
        print('\nDistribution of user types:\n', df['User Type'].value_counts())

        print('\nGender distribution:\n', df['Gender'].value_counts())

        print('\nThe most common birth year:\n', int(df['Birth Year'].mode()[0]))

        print('\nThe earliest birth year:\n', int(df['Birth Year'].min()))

        print('\nThe latest birth year:\n', int(df['Birth Year'].max()))
    except KeyError:
        return

def raw_data(df):
    """Displays the first 8 columns of data if desired. The user can choose
    the number of rows shown. A nested loop is included so that the
    user receives a different prompt after the first data sample is shown.
    Data continues to be shown at the interval requested at the first prompt.

    A separate loop is created to give the user the oportunity to view trips one at a time
    as a series, which is more readable. """

    x = 0
    y = 0

    while True:
        answer = input('\n Would you like to see raw trip data? \n If yes, enter the number of trips you would like to see at once (1-100). Otherwise enter no.\n').lower()
        try:
            if answer == 'no':
                return
            if int(answer) in range(2,100) and x < df.shape[0]:
                print(df.iloc[:int(answer), :8 ])
                while True:
                    answer2 = input('\nWould you like to see more data? Enter yes or no.\n').lower()
                    if answer2== 'yes':
                        x += int(answer)
                        y = x + int(answer)
                        print(df.iloc[x:y,:8])
                    elif answer2 == 'no':
                        return
                    elif (answer2 != 'yes' and answer2 != 'no'):
                        print('\nPlease enter yes or no')
                        continue
            if answer == '1':
                print(df.iloc[0, :8 ])
                while True:
                    answer2 = input('\nWould you like to see more data? Enter yes or no.\n')
                    if answer2.lower() == 'yes' and x < df.shape[0]:
                        print(df.iloc[x,:])
                        x += 1
                    elif answer2.lower() == 'no':
                        return
                    elif (answer2.lower() != 'yes' and answer2 != 'no'):
                        print('\nPlease enter yes or no')
                        continue

        except ValueError:
            print('Please enter a valid answer')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() == 'no':
            break
        elif restart.lower() != 'yes' and restart.lower() != 'no':
            print('Please enter yes or no')
            restart = input('\nWould you like to restart? Enter yes or no.\n')



if __name__ == "__main__":
	main()
