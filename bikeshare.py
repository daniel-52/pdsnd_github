import time
import datetime
import pprint
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington).
    while True:
        city = input('Please enter the city you want to analyze: [C]hicago, [N]ew York City, or [W]ashington?\n')
        if city.lower() in ['c', 'chicago', '[c]hicago']:
            city = 'chicago'
        elif city.lower() in ['n', 'ny', 'nyc', 'new york', 'new york city', '[n]ew york city']:
            city = 'new york city'
        elif city.lower() in ['w', 'washington', '[w]ashington']:
            city = 'washington'
        else:
            print('\nInvalid input, please choose one of the listed cities.')
            continue
        print(city.title() + ' selected.\n')
        break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Do you want to filter the data for one month?\n' +
                      'Enter one of the months "January" to "June" for filtering the data, or "all" to use all data.\n')
        if month.lower() in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
            month = month.lower()
            print(month.title() + ' selected.\n')
            break
        else:
            print('\nInvalid input, please choose one of the months (enter full name) or "all".')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Do you want to filter the data for one weekday?\n' +
                    'Enter e.g. "Monday" for filtering the data, or "all" to use all data.\n')
        if day.lower() in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
            day = day.lower()
            print(day.title() + ' selected.\n')
            break
        else:
            print('\nInvalid input, please choose one of the weekdays (enter full name) or "all".')

    print('-'*40)
    return city, month, day


def get_filters_debugging():
    """Skips user input for faster debugging of later parts of the code"""
    return 'chicago', 'all', 'all'


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
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month, if the data is not filtered by month
    if month == 'all':
        # get the most common month
        common_month = df['month'].mode()[0]
        # get the trip count for the most common month
        common_month_count = df['month'].value_counts().max()
        # print statistic
        print('Most common month: {}, count: {}, for weekday: {}'
              .format(common_month, common_month_count, day.title()))

    # display the most common day of week, if the data is not filtered by day
    if day == 'all':
        # get the most common week-day
        common_day = df['day_of_week'].mode()[0]
        # get the trip count for the most common week-day
        common_day_count = df['day_of_week'].value_counts().max()
        # print statistic
        print('Most common day of week: {}, count: {}, for month: {}'
              .format(common_day, common_day_count, month.title()))

    # display the most common start hour
    # Create a new column with the hour
    df['hour'] = df['Start Time'].dt.hour
    # get the most common hour
    common_hour = df['hour'].mode()[0]
    # get the trip count for the most common hour
    common_hour_count = df['hour'].value_counts().max()
    # print statistic
    print('Most common start hour: {}, count: {}, for month: {} and weekday: {}'
          .format(common_hour, common_hour_count, month.title(), day.title()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df, month, day):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    # get the most common start station
    common_start_station = df['Start Station'].mode()[0]
    # get the trip count for the most common start station
    common_start_station_count = df['Start Station'].value_counts().max()
    # print statistic
    print('Most common start station: {}, count: {}, for month: {} and weekday: {}'
          .format(common_start_station, common_start_station_count, month.title(), day.title()))

    # display most commonly used end station
    # get the most common end station
    common_end_station = df['End Station'].mode()[0]
    # get the trip count for the most common end station
    common_end_station_count = df['End Station'].value_counts().max()
    # print statistic
    print('Most common end station: {}, count: {}, for month: {} and weekday: {}'
          .format(common_end_station, common_end_station_count, month.title(), day.title()))

    # display most frequent combination of start station and end station trip
    # Create new column with the trip start and end station combined
    df['Start End Station'] = df['Start Station'] + ' to ' + df['End Station']
    # get the most common trip
    common_start_end_station = df['Start End Station'].mode()[0]
    # get the trip count for the most common trip
    common_start_end_station_count = df['Start End Station'].value_counts().max()
    # print statistic
    print('Most common trip: {}, count: {}, for month: {} and weekday: {}'
          .format(common_start_end_station, common_start_end_station_count, month.title(), day.title()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df, month, day):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_travel_time_formatted = datetime.timedelta(seconds=int(total_travel_time))
    print('Total travel time: {} seconds or {}, for month: {} and weekday: {}'
          .format(total_travel_time, total_travel_time_formatted, month.title(), day.title()))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mean_travel_time_formatted = datetime.timedelta(seconds=int(mean_travel_time))
    print('Mean travel time: {:.0f} seconds or {}, for month: {} and weekday: {}'
          .format(mean_travel_time, mean_travel_time_formatted, month.title(), day.title()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, month, day):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    def dict_to_string(dict_1, dict_2):
        """Returns a string with the information of two value_counts dictionaries"""
        dict_string = ''
        for key in dict_1:
            dict_string += '\n{}: {} or {:.1%}, '.format(key, dict_1[key], dict_2[key])
        return dict_string

    # Display counts of user types
    user_type_counts = dict(df['User Type'].value_counts())
    user_type_counts_normalized = dict(df['User Type'].value_counts(normalize=True))
    user_type_string = dict_to_string(user_type_counts, user_type_counts_normalized)
    print('User counts: ' + user_type_string + '\nfor month: {} and weekday: {}'
          .format(month.title(), day.title()))

    # Display counts of gender
    if 'Gender' in df:
        gender_counts = dict(df['Gender'].value_counts())
        gender_counts_normalized = dict(df['Gender'].value_counts(normalize=True))
        gender_string = dict_to_string(gender_counts, gender_counts_normalized)
        print('\nUser genders: ' + gender_string + '\nfor month: {} and weekday: {}'
              .format(month.title(), day.title()))
    else:
        print('\nNo gender data of users.')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_birth_year = int(df['Birth Year'].min())
        recent_birth_year = int(df['Birth Year'].max())
        common_birth_year = int(df['Birth Year'].mode()[0])
        print('\nUser year of birth: Earliest: {}, most recent: {}, most common: {}, for month: {} and weekday: {}'
              .format(earliest_birth_year, recent_birth_year, common_birth_year, month.title(), day.title()))
    else:
        print('\nNo year of birth data of users.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def get_5_rows(df):
    """Returns 5 trips at a time."""
    if 'Start End Station' in df:
        df = df.drop(columns=['Start End Station'])
    for i in range(0, len(df), 5):
        yield [df.iloc[i], df.iloc[i+1], df.iloc[i+2], df.iloc[i+3], df.iloc[i+4]]


def main():
    while True:
        print('\n')
        # Get user input and filter dataframe with it
        city, month, day = get_filters()
        df = load_data(city, month, day)

        # Calculate statistics
        time_stats(df, month, day)
        station_stats(df, month, day)
        trip_duration_stats(df, month, day)
        user_stats(df, month, day)

        # Show sample data
        show_data = input('\nWould you like to see the data of 5 trips? Enter yes or no.\n')
        for rows in get_5_rows(df):
            if show_data.lower() in ['y', 'yes']:
                for row in rows:
                    print(row)
                    print()
            else:
                break
            show_data = input('\nWould you like to see 5 more trips? Enter yes or no.\n')

        # Restart or end program
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() not in ['y', 'yes']:
            break


if __name__ == "__main__":
	main()
