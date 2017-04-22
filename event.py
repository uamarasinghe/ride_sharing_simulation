"""Simulation Events

This file should contain all of the classes necessary to model the different
kinds of events in the simulation.
"""
from rider import Rider, WAITING, CANCELLED, SATISFIED
from dispatcher import Dispatcher
from driver import Driver
from location import Location, deserialize_location
from monitor import Monitor, RIDER, DRIVER, REQUEST, CANCEL, PICKUP, DROPOFF


class Event:
    """An event.

    Events have an ordering that is based on the event timestamp: Events with
    older timestamps are less than those with newer timestamps.

    This class is abstract; subclasses must implement do().

    You may, if you wish, change the API of this class to add
    extra public methods or attributes. Make sure that anything
    you add makes sense for ALL events, and not just a particular
    event type.

    Document any such changes carefully!

    === Attributes ===
    @type timestamp: int
        A timestamp for this event.
    """

    def __init__(self, timestamp):
        """Initialize an Event with a given timestamp.

        @type self: Event
        @type timestamp: int
            A timestamp for this event.
            Precondition: must be a non-negative integer.
        @rtype: None

        >>> Event(7).timestamp
        7
        """
        self.timestamp = timestamp

    # The following six 'magic methods' are overridden to allow for easy
    # comparison of Event instances. All comparisons simply perform the
    # same comparison on the 'timestamp' attribute of the two events.
    def __eq__(self, other):
        """Return True iff this Event is equal to <other>.

        Two events are equal iff they have the same timestamp.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first == second
        False
        >>> second.timestamp = first.timestamp
        >>> first == second
        True
        """
        return self.timestamp == other.timestamp

    def __ne__(self, other):
        """Return True iff this Event is not equal to <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first != second
        True
        >>> second.timestamp = first.timestamp
        >>> first != second
        False
        """
        return not self == other

    def __lt__(self, other):
        """Return True iff this Event is less than <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first < second
        True
        >>> second < first
        False
        """
        return self.timestamp < other.timestamp

    def __le__(self, other):
        """Return True iff this Event is less than or equal to <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first <= first
        True
        >>> first <= second
        True
        >>> second <= first
        False
        """
        return self.timestamp <= other.timestamp

    def __gt__(self, other):
        """Return True iff this Event is greater than <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first > second
        False
        >>> second > first
        True
        """
        return not self <= other

    def __ge__(self, other):
        """Return True iff this Event is greater than or equal to <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first >= first
        True
        >>> first >= second
        False
        >>> second >= first
        True
        """
        return not self < other

    def __str__(self):
        """Return a string representation of this event.

        @type self: Event
        @rtype: str
        """
        raise NotImplementedError("Implemented in a subclass")

    def do(self, dispatcher, monitor):
        """Do this Event.

        Update the state of the simulation, using the dispatcher, and any
        attributes according to the meaning of the event.

        Notify the monitor of any activities that have occurred during the
        event.

        Return a list of new events spawned by this event (making sure the
        timestamps are correct).

        Note: the "business logic" of what actually happens should not be
        handled in any Event classes.

        @type self: Event
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]
        """
        raise NotImplementedError("Implemented in a subclass")


class RiderRequest(Event):
    """A rider requests a driver.

    === Attributes ===
    @type rider: Rider
        The rider.
    """
    def __init__(self, timestamp, rider):
        """Initialize a RiderRequest event.

        @type self: RiderRequest
        @type rider: Rider
        @rtype: None
        """
        super().__init__(timestamp)
        self.rider = rider

    def do(self, dispatcher, monitor):
        """Assign the rider to a driver or add the rider to a waiting list.
        If the rider is assigned to a driver, the driver starts driving to
        the rider.

        Return a Cancellation event. If the rider is assigned to a driver,
        also return a Pickup event.

        @type self: RiderRequest
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]
        """
        monitor.notify(self.timestamp, RIDER, REQUEST,
                       self.rider.identifier, self.rider.origin)

        events = []
        # assigns driver if there are drivers, else putting rider onto
        # waiting list
        driver = dispatcher.request_driver(self.rider)
        # if there is a driver
        if driver is not None:
            # find how long it'll take to get to driver
            travel_time = driver.start_drive(self.rider.origin)
            # adds to event list, the pick up time, rider name and driver name
            events.append(Pickup(self.timestamp + travel_time, self.rider,
                                 driver))
            # add to event list, the time the rider will cancel and rider's name
        events.append(Cancellation(self.timestamp + self.rider.patience,
                                   self.rider))

        return events

    def __str__(self):
        """Return a string representation of this event.

        @type self: RiderRequest
        @rtype: str

        >>> rider = Rider('xyz', Location(1, 2), Location(3, 3), 3)
        >>> r1 = RiderRequest(3, rider)
        >>> print(r1)
        3 -- ID: xyz, Origin: (1,2), Destination: (3,3), Status: waiting, Patience: 3: Request a driver
        >>> rider_z = Rider('eggshells', Location(0, 2), Location(3, 2), 1)
        >>> r2 = RiderRequest(0, rider)
        >>> print(r2)
        0 -- ID: xyz, Origin: (1,2), Destination: (3,3), Status: waiting, Patience: 3: Request a driver
        """
        return "{} -- {}: Request a driver".format(self.timestamp, self.rider)


class DriverRequest(Event):
    """A driver requests a rider.

    === Attributes ===
    @type driver: Driver
        The driver.
    """

    def __init__(self, timestamp, driver):
        """Initialize a DriverRequest event.

        @type self: DriverRequest
        @type driver: Driver
        @rtype: None
        """
        super().__init__(timestamp)
        self.driver = driver

    def do(self, dispatcher, monitor):
        """Register the driver, if this is the first request, and
        assign a rider to the driver, if one is available.

        If a rider is available, return a Pickup event.

        @type self: DriverRequest
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]

        Writing multiple examples for the DriverRequest class is not feasible because it would require the
        initialization of a monitor and a dispatcher. However it is not sufficient to just initialize these objects
        without relevant driver and rider data and since it is a simulation, we would not get a good understanding
        how the DriverRequest interacts with and spawns other relevant Events. Furthermore, these examples add
        very little value for testing the functionality of this method because the method itself is dependant on
        helper methods that will have already been tested.
        """
        # Notify the monitor about the request.
        monitor.notify(self.timestamp, DRIVER, REQUEST,
                       self.driver.identifier, self.driver.location)
        events = []
        # Request a rider from the dispatcher.
        rider = dispatcher.request_rider(self.driver)
        # If there is one available, the driver starts driving towards the rider
        if rider is not None:
            # time taken to drive to pick up location
            travel_time = self.driver.start_drive(rider.origin)
            # the method returns a Pickup event for when the driver
            events.append(Pickup(self.timestamp + travel_time, rider,
                                 self.driver))
        return events

    def __str__(self):
        """Return a string representation of this event.

        @type self: DriverRequest
        @rtype: str

        >>> d1 = Driver('Sam', Location(1,1), 2)
        >>> dr = DriverRequest(3, d1)
        >>> print(dr)
        3 -- ID: Sam, Location: (1,1), Speed: 2: Request a rider
        >>> d2 = Driver('boo', Location(1,1), 2)
        >>> dz = DriverRequest(0, d2)
        >>> print(dz)
        0 -- ID: boo, Location: (1,1), Speed: 2: Request a rider
        """
        return "{} -- {}: Request a rider".format(self.timestamp, self.driver)


class Cancellation(Event):
    """ Cancel a rider's request.

    === Attributes ===
    @param Rider rider: waiting rider requesting a ride
    """

    def __init__(self, timestamp, rider):
        """
        Initialize a cancellation event.

        @param Cancellation self: this Cancellation event
        @param Rider rider: waiting rider requesting a ride
        @rtype: None
        """
        super().__init__(timestamp)
        self.rider = rider

    def __str__(self):
        """Return a string representation of this cancellation event.

        @type self: Cancellation
        @rtype: str

        >>> rider = Rider('xyz', Location(1, 2), Location(3, 3), 3)
        >>> r1 = Cancellation(8, rider)
        >>> print(r1)
        8 -- ID: xyz, Origin: (1,2), Destination: (3,3), Status: waiting, Patience: 3: Cancellation by rider
        >>> rider_z = Rider('eggshells', Location(0, 2), Location(3, 2), 1)
        >>> r2 = Cancellation(0, rider)
        >>> print(r2)
        0 -- ID: xyz, Origin: (1,2), Destination: (3,3), Status: waiting, Patience: 3: Cancellation by rider
        """
        return "{} -- {}: Cancellation by rider".format(self.timestamp,
                                                        self.rider)

    def do(self, dispatcher, monitor):
        """If a rider's pickup time is greater than the rider's patience then
        change the status of rider from waiting to cancelled.

        Don't schedule any future events.

        @type self: Cancellation
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]

        Writing multiple examples for the Cancellation class is not feasible because it would require the
        initialization of a monitor and a dispatcher. However it is not sufficient to just initialize these objects
        without relevant driver and rider data and since it is a simulation, we would not get a good understanding
        how the Cancellation class interacts with and spawns other relevant Events. Furthermore, these examples add
        very little value for testing the functionality of this method because the method itself is dependant on
        helper methods that will have already been tested.
        """

        # Notify the monotor about the request
        monitor.notify(self.timestamp, RIDER, CANCEL, self.rider.identifier, self.rider.origin)

        events = []
        # Check whether rider is satisfied.
        if self.rider not in dispatcher.rider[SATISFIED]:
            # If not satisfied, change status to cancelled and cancel ride.
            self.rider.status = CANCELLED
            dispatcher.cancel_ride(self.rider)
        return events


class Pickup(Event):
    """
    A pickup event.

    === Attributes ===
    @param Rider rider: rider waiting to be picked up
    @param Driver driver: driver picking up rider
    """

    def __init__(self, timestamp, rider, driver):
        """
        Initialize a Pickup event.

        @param Pickup self: this pickup event
        @param int timestamp: time at which driver will pick up rider
        @param Rider rider: rider waiting to be picked up
        @param Driver driver: driver picking up rider
        @rtype: None
        """
        super().__init__(timestamp)
        self.rider, self.driver = rider, driver

    def __str__(self):
        """
        Return a string representation of this Pickup Event.

        @param Pickup self: This pickup event
        @rtype: str

        >>> rider = Rider('xyz', Location(1, 2), Location(3, 3), 3)
        >>> d1 = Driver('Sam', Location(1,1), 2)
        >>> p = Pickup(4, rider, d1)
        >>> print(p)
        4 -- ID: Sam, Location: (1,1), Speed: 2 -- ID: xyz, Origin: (1,2), Destination: (3,3), Status: waiting, \
Patience: 3: Pick up time by driver of rider
        >>> rider_z = Rider('eggshells', Location(0, 2), Location(3, 2), 1)
        >>> d2 = Driver('boo', Location(1,1), 2)
        >>> p2 = Pickup(10, rider_z, d2)
        >>> print(p2)
        10 -- ID: boo, Location: (1,1), Speed: 2 -- ID: eggshells, Origin: (0,2), Destination: (3,2), Status: waiting, \
Patience: 1: Pick up time by driver of rider
        """

        return "{} -- {} -- {}: Pick up time by driver of rider".format(
            self.timestamp, self.driver, self.rider)

    def do(self, dispatcher, monitor):
        """
        Set the driver's location to the rider's location.

        If the rider is waiting, dispatcher gives them a rider and the driver's
        destination becomes the rider's destination.
        Schedule a dropoff event for the time they will arrive a the rider's
        destination. Rider becomes satisfied.

        If rider has cancelled, the driver becomes idle and schedule a new event
         for the driver requesting a rider.

        @param Pickup self: this Pickup event.
        @param Dispatcher dispatcher:
        @param Monitor monitor:
        @rtype: list[Event]

        Writing multiple examples for the Pickup class is not feasible because it would require the
        initialization of a monitor and a dispatcher. However it is not sufficient to just initialize these objects
        without relevant driver and rider data and since it is a simulation, we would not get a good understanding
        how the Pickup class interacts with and spawns other relevant Events. Furthermore, these examples add
        very little value for testing the functionality of this method because the method itself is dependant on
        helper methods that will have already been tested.

        """
        # End the drive to the pickup location.
        self.driver.end_drive()

        # Notify the monitor of about both the driver's and rider's pickup event.
        monitor.notify(self.timestamp, RIDER, PICKUP, self.rider.identifier, self.rider.destination)
        monitor.notify(self.timestamp, DRIVER, PICKUP, self.driver.identifier, self.driver.location)

        events = []
        # If rider has not cancelled
        if self.rider not in dispatcher.rider[CANCELLED]:
            # Get travel time and and start the ride
            travel_time = self.driver.start_ride(self.rider)
            # This creates a dropoff event for the rider
            events.append(Dropoff(self.timestamp + travel_time, self.rider, self.driver))
            # Rider is now satisfied as the ride is succsfully finished.
            self.rider.status = SATISFIED
            dispatcher.end_successful_ride(self.rider)

        # If rider has cancelled, driver will put in a new request
        else:
            events.append(DriverRequest(self.timestamp, self.driver))

        return events


class Dropoff(Event):
    """
    A dropoff event.

    === Attributes ===
    @param Rider rider: rider being dropped off
    @param Driver driver: driver dropping off rider
    """

    def __init__(self, timestamp, rider, driver):
        """
        Initialize a dropoff event.

        @param Dropoff self: this Dropoff event
        @param int timestamp: time at which rider was dropped off
        @param Rider rider: rider being dropped off
        @param Driver driver: driver dropping off rider
        @rtype: None
        """
        super().__init__(timestamp)
        self.rider, self.driver = rider, driver

    def __str__(self):
        """
        Return a string representation of Dropoff event.

        @param Dropoff self: this dropoff event
        @rtype: str

        >>> rider = Rider('xyz', Location(1, 2), Location(3, 3), 3)
        >>> d1 = Driver('Sam', Location(1,1), 2)
        >>> d = Dropoff(4, rider, d1)
        >>> print(d)
        4 -- ID: Sam, Location: (1,1), Speed: 2 -- ID: xyz, Origin: (1,2), Destination: (3,3), Status: waiting, \
Patience: 3: Dropoff time by driver of rider
        >>> rider_z = Rider('eggshells', Location(0, 2), Location(3, 2), 1)
        >>> d2 = Driver('boo', Location(1,1), 2)
        >>> p2 = Dropoff(10, rider_z, d2)
        >>> print(p2)
        10 -- ID: boo, Location: (1,1), Speed: 2 -- ID: eggshells, Origin: (0,2), Destination: (3,2), Status: waiting, \
Patience: 1: Dropoff time by driver of rider
        """

        return "{} -- {} -- {}: Dropoff time by driver of rider".format(self.timestamp, self.driver, self.rider)

    def do(self, dispatcher, monitor):
        """
        Set the driver's location to the rider's destination.

        Change status of rider to satisfied.

        Driver becomes idle and requests a new rider.

        @type self: Dropoff
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]

        Writing multiple examples for the Dropoff class is not feasible because it would require the
        initialization of a monitor and a dispatcher. However it is not sufficient to just initialize these objects
        without relevant driver and rider data and since it is a simulation, we would not get a good understanding
        how the Dropoff class interacts with and spawns other relevant Events. Furthermore, these examples add
        very little value for testing the functionality of this method because the method itself is dependant on
        helper methods that will have already been tested.
        """

        # End the ride and arrive at rider's destination.
        self.driver.end_ride()

        # Notify monitor about Dropoff event.
        monitor.notify(self.timestamp, DRIVER, DROPOFF,
                       self.driver.identifier, self.driver.location)

        # Once the ride is successful,driver will put in a new request
        events = [DriverRequest(self.timestamp, self.driver)]
        dispatcher.end_successful_ride(self.rider)
        return events


def create_event_list(filename):
    """Return a list of Events based on raw list of events in <filename>.

    Precondition: the file stored at <filename> is in the format specified
    by the assignment handout.

    @param filename: str
        The name of a file that contains the list of events.
    @rtype: list[Event]

    No examples are provided as this method deals with opening a file.
    """
    events = []

    # Read through file, strip white spaces and properly format Driver and Rider requests
    # as a list of events.

    with open(filename, "r") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            tokens = line.split(" ")
            timestamp = int(tokens[0])
            event_type = tokens[1]

            if event_type == "DriverRequest":
                identifier = tokens[2]
                location_ = deserialize_location(tokens[3])
                speed = int(tokens[4])
                driver = Driver(identifier, location_, speed)
                event_obj = DriverRequest(timestamp, driver)
                events.append(event_obj)

            elif event_type == "RiderRequest":
                ident = tokens[2]
                origin = deserialize_location(tokens[3])
                destination = deserialize_location(tokens[4])
                patience = int(tokens[5])
                rider = Rider(ident, origin, destination, patience, status=WAITING)
                event_obj = RiderRequest(timestamp, rider)
                events.append(event_obj)
    return events
