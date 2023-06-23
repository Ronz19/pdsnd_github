import time
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
    # Define a set of city name that user can enter to view bikershare data
    citys = {"chicago", "new york city", "washington"}
    # Get user input for city (chicago, new york city, washington). 
    city =""
    while city.lower() not in citys: 
        city = input("Enter name of city that you want to analyze (chicago, new york city, washington): ") 

    # Define a set of month that user can enter to view bikershare data
    months = {"all","january","february","march","april","may","june"}
    # Get user input for month (all, january, february, ... , june)
    month =""
    while month.lower() not in months: 
        month = input("Enter month that you want to filter data (all, january, february, ... , june): ")
         
    # Define a set day of week that user can enter to view bikershare data. 
    day_of_weeks = {"all","monday","tuesday","wednesday","thursday","friday","saturday","sunday"}
    # Get user input for day of week (all, monday, tuesday, ... sunday)
    day =""
    while day.lower() not in day_of_weeks: 
        day = input("Enter day of week that you want to filter data: ") 

    print('-'*40)
    return city.lower(), month.lower(), day.lower()


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


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Popular Start Month:', popular_month)

    # Display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most Popular day of week:', popular_day)

    # Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Popular Start Station:', popular_start_station)
    
    # Display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Popular End Station:', popular_end_station)

    # Display most frequent combination of start station and end station trip
    popular_start_end_station = df[['Start Station','End Station']].mode()
    print('Most frequent combination of start station and end station trip \n')
    print(popular_start_end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time:', total_travel_time)

    # Display mean travel time
    mean_travel_time =  df['Trip Duration'].mean()
    print('Mean travel time:', mean_travel_time)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
                 
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Counts of user types\n")
    print(user_types);

    # Display counts of gender
    if 'Gender' in df: 
        genders = df['Gender'].value_counts()
        print("Counts of genders\n")
        print(genders)

    if 'Birth Year' in df: 
        # Display earliest, most recent, and most common year of birth
        earliest_year_of_birth = df['Birth Year'].min()
        print('\nEarliest year of birth: ',earliest_year_of_birth)
        
        # Display earliest, most recent, and most common year of birth
        recent_year_of_birth   = df['Birth Year'].max()
        print('\nMost recent year of birth: ',recent_year_of_birth )
    
        # Display earliest, most recent, and most common year of birth
        popular_year_of_birth  = df['Birth Year'].mode()[0]
        print('\nMost common year of birth: ',popular_year_of_birth)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df) : 
    """Displays statistics on bikeshare by user request"""
    
    index = 0
    while True:
        if index % 5 == 0: 
            view_data = input('\nDo you want to view all data of bikeshare? Enter yes or no.\n')
            if view_data.lower() == 'no' : 
                break
            elif view_data.lower() != 'yes':
                continue
                
        print(df.iloc[[index]])
        index += 1            

    print('-'*40)  
    
    
def main():
    while True:
        city, month, day = get_filters()
        try: 
            df = load_data(city, month, day)
        except FileNotFoundError:
            print (city, 'file name not exist, please import csv file and try again')
            break

        time_stats(df)  #Show popular times of travel
        station_stats(df) # Popular stations and trip
        trip_duration_stats(df) #Trip duration
        user_stats(df) #User info
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
