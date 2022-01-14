import time
import pandas as pd
import numpy as np

CITY_DATA = {
    "chicago": "chicago.csv",
    "new york city": "new_york_city.csv",
    "washington": "washington.csv",
}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let's explore some US bikeshare data!")

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_list = ["chicago", "new_york_city", "washington"]
    while True:
        city = input("Please enter a city you want to analyse?\n").lower().strip()
        if city not in city_list:
            print("Bad input; try again")
        else:
            break
    months = ["january", "february", "march", "april", "may", "june", "all"]

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input("Please enter a month to filter by:\n").lower().strip()
        if month not in months:
            print("Bad input; try again")
        else:
            break
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    week_days = [
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
        "all",
    ]
    while True:
        day = input("Please enter the day of the week to filter by:\n").lower().strip()
        if day not in week_days:
            print("Bad input; try again")
        else:
            break

    print("-" * 40)
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
    df["Start Time"] = pd.to_datetime(df["Start Time"])

    # extract month and day of week from Start Time to create new columns
    df["month"] = df["Start Time"].dt.month
    df["day_of_week"] = df["Start Time"].dt.weekday_name

    # filter by month if applicable
    if month != "all":
        # use the index of the months list to get the corresponding int
        months = ["january", "february", "march", "april", "may", "june"]
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df["month"] == month]

    # filter by day of week if applicable
    if day != "all":
        # filter by day of week to create the new dataframe
        df = df[df["day_of_week"] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel.
    Args:
        (DataFrame) df - Pandas DataFrame containing city data filtered by month and day
    """

    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()

    df["Start Time"] = pd.to_datetime(df["Start Time"])

    df["month"] = df["Start Time"].dt.month
    df["day_of_week"] = df["Start Time"].dt.weekday_name
    df["hour"] = df["Start Time"].dt.hour

    # TO DO: display the most common month
    months = ["january", "february", "march", "april", "may", "june"]
    most_common_month = df["month"].mode()[0]
    print("The most common month is :", months[most_common_month - 1])

    # TO DO: display the most common day of week
    most_common_day_of_week = df["day_of_week"].mode()[0]
    print("The most common day of week is :", most_common_day_of_week)

    # TO DO: display the most common start hour
    most_common_start_hour = df["hour"].mode()[0]
    print("The most common start hour is :", most_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip.
    Args:
        (DataFrame) df - Pandas DataFrame containing city data filtered by month and day
    """

    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_common_start_station = df["Start Station"].mode()[0]
    print("The most commonly used start station :", most_common_start_station)

    # TO DO: display most commonly used end station
    most_common_end_station = df["End Station"].mode()[0]
    print("The most commonly used end station :", most_common_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    most_common_start_and_end_stations = (
        df.groupby(["Start Station", "End Station"]).size().nlargest(1)
    )
    print("\nThe most frequent combination of start statiion and end station trip: ")
    print(most_common_start_and_end_stations)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration in seconds.
    Args:
        (DataFrame) df - Pandas DataFrame containing city data filtered by month and day
    """

    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df["Trip Duration"].sum()
    print(
        "The total travel time from the given fitered data is: "
        + str(total_travel_time)
    )

    # TO DO: display mean travel time
    mean_travel_time = df["Trip Duration"].mean()
    print(
        "The mean travel time from the given fitered data is: " + str(mean_travel_time)
    )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def user_stats(df):
    """Displays statistics on bikeshare users.
    Args:
        (DataFrame) df - Pandas DataFrame containing city data filtered by month and day
    """

    print("\nCalculating User Stats...\n")
    start_time = time.time()

    # TO DO: Display counts of user types
    try:
        user_types = df["User Type"].value_counts()
        print(user_types, "\n")
    except KeyError:
        print("User Types: No data available for this month.")

    # TO DO: Display counts of gender
    try:
        gender_types = df["Gender"].value_counts()
        print(gender_types, "\n")
    except KeyError:
        print("Gender Types: No data available for this month.")

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        earliest_year = int(df["Birth Year"].min())
        print("Earliest year of birth: ", earliest_year)
    except KeyError:
        print("Earliest year of birth: No data available for this month.")

    try:
        most_recent_year = int(df["Birth Year"].max())
        print("Most recent year of birth: ", most_recent_year)
    except KeyError:
        print("Most recent year of birth: No data available for this month.")

    try:
        most_common_year = int(df["Birth Year"].mode()[0])
        print("Most common year of birth: ", most_common_year)
    except KeyError:
        print("Most common year of birth: No data available for this month.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def view_data(df):
    """Displays additional 5 rows of data based on user request"""

    view_data = input(
        "Would you like to view 5 rows of individual trip data? Enter yes or no? \n"
    )
    start_loc = 0
    end_loc = 5
    while view_data.lower() != "no":
        print(df[start_loc:end_loc])
        start_loc = start_loc + 5
        end_loc = end_loc + 5
        view_data = input("Do you wish to continue?: ").lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        view_data(df)

        restart = input("\nWould you like to restart? Enter yes or no.\n")
        if restart.lower() != "yes":
            break


if __name__ == "__main__":
    main()
