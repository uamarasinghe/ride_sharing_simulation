from location import Location, manhattan_distance

RIDER = "rider"
DRIVER = "driver"
REQUEST = "request"
CANCEL = "cancel"
PICKUP = "pickup"
DROPOFF = "dropoff"

# Issue in the notify method usage of .append appears to have no discernible effect on the simulation and reports.

# Three weak warning related to accessing protected member of a class, but this is only for doctest purposes.
"""
The Monitor module contains the Monitor class, the Activity class,
and a collection of constants. Together the elements of the module
help keep a record of activities that have occurred.

Activities fall into two categories: Rider activities and Driver
activities. Each activity also has a description, which is one of
request, cancel, pickup, or dropoff.

=== Constants ===
@param RIDER: str
    A constant used for the Rider activity category.
@param DRIVER: str
    A constant used for the Driver activity category.
@param REQUEST: str
    A constant used for the request activity description.
@param CANCEL: str
    A constant used for the cancel activity description.
@param PICKUP: str
    A constant used for the pickup activity description.
@param DROPOFF: str
    A constant used for the dropoff activity description.
"""


class Activity:
    """An activity that occurs in the simulation.

    === Attributes ===
    @param int timestamp: The time at which the activity occurred.
    @param str description: A description of the activity.
    @param str identifier: An identifier for the person doing the activity.
    @param Location location: The location at which the activity occurred.
    """

    def __init__(self, timestamp, description, identifier, location):
        """Initialize an Activity.

        @param Activity self: this Activity
        @param int timestamp: The time at which the activity occurred.
        @param str description: A description of the activity.
        @param str identifier: An identifier for the person doing the activity.
        @param Location location: The location at which the activity occurred.
        @rtype: None
        """
        self.description = description
        self.time = timestamp
        self.id = identifier
        self.location = location


class Monitor:
    """A monitor keeps a record of activities that it is notified about.
    When required, it generates a report of the activities it has recorded.
    """

    # === Private Attributes ===
    # @param _activities: dict[str, dict[str, list[Activity]]]
    #       A dictionary whose key is a category, and value is another
    #       dictionary. The key of the second dictionary is an identifier
    #       and its value is a list of Activities.

    def __init__(self):
        """Initialize a Monitor.

        @param Monitor self: this Monitor
        """
        self._activities = {
            RIDER: {},
            DRIVER: {}
        }
        """@param _activities: dict[str, dict[str, list[Activity]]]"""

    def __str__(self):
        """Return a string representation.

        @param Monitor self: this Monitor
        @rtype: str

        >>> m1 = Monitor()
        >>> print(m1)
        Monitor (0 drivers, 0 riders)
        >>> m1.notify(3, DRIVER, PICKUP, 'abc', Location(1,1))
        >>> print(m1)
        Monitor (1 drivers, 0 riders)
        """
        return "Monitor ({} drivers, {} riders)".format(
                len(self._activities[DRIVER]), len(self._activities[RIDER]))

    def notify(self, timestamp, category, description, identifier, location):
        """Notify the monitor of the activity.

        @param Monitor self: this Monitor
        @param int timestamp: The time of the activity.
        @param DRIVER | RIDER category: The category for the activity.
        @param REQUEST | CANCEL | PICKUP | DROP_OFF description: A description of the activity.
        @param str identifier: The identifier for the actor.
        @param Location location: The location of the activity.
        @rtype: None
        """
        if identifier not in self._activities[category]:
            self._activities[category][identifier] = []

        activity = Activity(timestamp, description, identifier, location)
        self._activities[category][identifier].append(activity)
        # append error may be due to CANCELLED from 'cancelled'

    def report(self):
        """Return a report of the activities that have occurred.

        @param Monitor self: this Monitor
        @rtype: dict[str, object]

        # Due to unordered dictionary type, doctest fails when test dictionaries therefore
        # expected answer declared
        >>> m1 = Monitor()
        >>> m1.notify(0, DRIVER, REQUEST, 'abc', Location(0,0))
        >>> m1.notify(3, DRIVER, PICKUP, 'abc', Location(1,1))
        >>> m1.notify(6, DRIVER, DROPOFF, 'abc', Location(5,5))
        >>> m1.notify(0, RIDER, REQUEST, 'xyz', Location(1,1))
        >>> m1.notify(3, RIDER, PICKUP, 'xyz', Location(1,1))
        >>> r1 = m1.report()
        >>> expected = {'rider_wait_time': 3.0, 'driver_total_distance': 10.0, 'driver_ride_distance': 8.0}
        >>> r1 == expected
        True
        """
        return {"rider_wait_time": self._average_wait_time(),
                "driver_total_distance": self._average_total_distance(),
                "driver_ride_distance": self._average_ride_distance()}

    def _average_wait_time(self):
        """Return the average wait time of riders that have either been picked
        up or have cancelled their ride.

        @param Monitor self: this Monitor
        @rtype: float
        >>> m1 = Monitor()
        >>> m1.notify(0, DRIVER, REQUEST, 'abc', Location(0,0))
        >>> m1.notify(3, DRIVER, PICKUP, 'abc', Location(1,1))
        >>> m1.notify(6, DRIVER, DROPOFF, 'abc', Location(5,5))
        >>> m1.notify(0, RIDER, REQUEST, 'xyz', Location(1,1))
        >>> m1.notify(3, RIDER, PICKUP, 'xyz', Location(1,1))
        >>> m1.notify(0, RIDER, REQUEST, 'ash', Location(1,1))
        >>> m1.notify(8, RIDER, CANCEL, 'ash', Location(1,1))
        >>> m1._average_wait_time()
        5.5
        """
        wait_time = 0
        count = 0
        for activities in self._activities[RIDER].values():
            # A rider that has less than two activities hasn't finished
            # waiting (they haven't cancelled or been picked up).
            if len(activities) >= 2:
                # The first activity is REQUEST, and the second is PICKUP
                # or CANCEL. The wait time is the difference between the two.
                wait_time += activities[1].time - activities[0].time
                count += 1
        if count != 0:
            return float(wait_time / count)
        else:
            raise ZeroDivisionError

    def _average_total_distance(self):
        """Return the average distance drivers have driven.

        @param Monitor self: this Monitor
        @rtype: float

        >>> m1 = Monitor()
        >>> m1.notify(0, DRIVER, REQUEST, 'abc', Location(0,0))
        >>> m1.notify(3, DRIVER, PICKUP, 'abc', Location(1,1))
        >>> m1.notify(6, DRIVER, DROPOFF, 'abc', Location(5,5))
        >>> m1.notify(0, RIDER, REQUEST, 'xyz', Location(1,1))
        >>> m1.notify(3, RIDER, PICKUP, 'xyz', Location(1,1))
        >>> m1.notify(0, RIDER, REQUEST, 'ash', Location(1,1))
        >>> m1.notify(8, RIDER, PICKUP, 'ash', Location(1,1))
        >>> m1.notify(6, DRIVER, REQUEST, 'luigi', Location(2,2))
        >>> m1.notify(8, DRIVER, PICKUP, 'luigi', Location(3,3))
        >>> m1.notify(145, DRIVER, DROPOFF, 'luigi', Location(0,0))
        >>> m1._average_total_distance()
        9.0
        """
        total_dist = 0
        count = 0
        for activities in self._activities[DRIVER].values():
                # Drivers can have several PICKUP and DROPOFF events.
                # Calculate the total distance between two events.
                if len(activities) >= 2:
                    for i in range(len(activities)-1):
                        total_dist += manhattan_distance(activities[i].location, activities[i+1].location)
                    count += 1
        if count != 0:
            return total_dist / count
        else:
            raise ZeroDivisionError

    def _average_ride_distance(self):
        """Return the average distance drivers have driven on rides.

        @param Monitor self: this Monitor
        @rtype: float

        >>> m1 = Monitor()
        >>> m1.notify(0, DRIVER, REQUEST, 'abc', Location(0,0))
        >>> m1.notify(3, DRIVER, PICKUP, 'abc', Location(1,1))
        >>> m1.notify(6, DRIVER, DROPOFF, 'abc', Location(5,5))
        >>> m1.notify(0, RIDER, REQUEST, 'xyz', Location(1,1))
        >>> m1.notify(3, RIDER, PICKUP, 'xyz', Location(1,1))
        >>> m1.notify(0, RIDER, REQUEST, 'ash', Location(1,1))
        >>> m1.notify(8, RIDER, PICKUP, 'ash', Location(1,1))
        >>> m1.notify(6, DRIVER, REQUEST, 'luigi', Location(2,2))
        >>> m1.notify(8, DRIVER, PICKUP, 'luigi', Location(3,3))
        >>> m1.notify(145, DRIVER, DROPOFF, 'luigi', Location(0,0))
        >>> m1._average_ride_distance()
        7.0
        """
        ride_dist = 0
        for activities in self._activities[DRIVER].values():
            # Drivers can have several PICKUP and DROPOFF events.
            # Calculate the total distance between two events.
            if len(activities) >= 2:
                for i in range(len(activities)-1):
                    if activities[i].description == PICKUP and activities[i+1].description == DROPOFF:
                            ride_dist += manhattan_distance(activities[i].location, activities[i+1].location)

        # using all drivers in simulation (not only the ones who have picked up riders successfully
        if len(self._activities[DRIVER]) != 0:
            return ride_dist / len(self._activities[DRIVER])
        else:
            raise ZeroDivisionError
