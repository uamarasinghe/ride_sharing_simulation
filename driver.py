from location import Location, manhattan_distance
from rider import Rider


class Driver:
    """A driver for a ride-sharing service.

    === Attributes ===
    @param str identifier: str
        A unique identifier for the driver.
    @param Location location:
        The current location of the driver.
    @param bool is_idle:
        A property that is True if the driver is idle and False otherwise.
    """

    def __init__(self, identifier, location, speed):
        """Initialize a Driver.

        @param Driver self: this driver
        @param str identifier: A unique identifier for the driver.
        @param Location location: The current location of the driver.
        @param int speed: driver's speed
        @rtype: None

        """
        self.identifier, self.location, self.speed = identifier, location, speed
        self.destination = None
        self.is_idle = True

    def __str__(self):
        """Return a string representation.

        @param Driver self: this driver
        @rtype: str

        >>> d1 = Driver('Sam', Location(2,2), 3)
        >>> print(d1)
        ID: Sam, Location: (2,2), Speed: 3
        >>> d2 = Driver('Lila', Location(2,3), 4)
        >>> print(d2)
        ID: Lila, Location: (2,3), Speed: 4
        """
        return "ID: {}, Location: {}, Speed: {}".format(self.identifier, self.location, self.speed)

    def __eq__(self, other):
        """Return True if self equals other, and false otherwise.

        @param Driver self: this driver
        @param Driver|object other: object being compared to driver self
        @rtype: bool

        >>> d1 = Driver('Sam', Location(2,2), 3)
        >>> d2 = Driver('Lila', Location(2,3), 4)
        >>> d3 = Driver('Lila', Location(2,3), 4)
        >>> d1 == d2
        False
        >>> d2 == d3
        True
        """
        return (type(self) == type(other) and
                self.identifier == other.identifier and
                self.location == other.location and
                self.speed == other.speed and
                self.is_idle == other.is_idle and
                self.destination == other.destination)

    def __repr__(self):
        """
        Returns a string representation when self is called.

        @param Driver self: this Driver self
        @rtype: str

        >>> d1 = Driver('Sam', Location(2,2), 3)
        >>> d1
        ID: Sam, Location: (2,2), Speed: 3
        >>> d2 = Driver('Lila', Location(2,3), 4)
        >>> d2
        ID: Lila, Location: (2,3), Speed: 4
        """
        return str(self)

    def get_travel_time(self, destination):
        """Return the time it will take to arrive at the destination,
        rounded to the nearest integer.

        @param Driver self: this driver
        @param Location destination: driver's destination
        @rtype: int

        >>> d1 = Driver('Sam', Location(1,1), 2)
        >>> d1.get_travel_time(Location(6,6))
        5
        >>> d2 = Driver('Sam', Location(1,1), 2)
        >>> d2.get_travel_time(Location(4,4))
        3
        """
        if destination is not None and self.location is not None and self.speed != 0:
            return round(manhattan_distance(self.location, destination)/self.speed)
        else:
            return 0

    def start_drive(self, location):
        """
        Start driving to the location and return the time the drive will take.

        @param Driver self: this driver
        @param Location location: location driver will start driving to
        @rtype: int

        >>> d1 = Driver('Sam', Location(1,1), 2)
        >>> d1.start_drive(Location(6,6))
        5
        >>> d2 = Driver('Sam', Location(1,1), 2)
        >>> d2.start_drive(Location(4,4))
        3
        """
        self.is_idle = False
        time = self.get_travel_time(location)
        self.destination = location
        return time

    def end_drive(self):
        """End the drive and arrive at the destination.

        Precondition: self.destination is not None.

        @param Driver self: this driver
        @rtype: None
        """
        self.is_idle, self.location = False, self.destination

    def start_ride(self, rider):
        """
        Start a ride and return the time the ride will take.

        @param Driver self: this driver
        @param Rider rider: rider
        @rtype: int

        >>> d1 = Driver('Sam', Location(1,1), 2)
        >>> r1 = Rider('xyz', Location(1,1), Location(6,6), 4)
        >>> d1.start_ride(r1)
        5
        >>> d1 = Driver('Sam', Location(1,1), 3)
        >>> r2 = Rider('xyz', Location(1,1), Location(6,6), 4)
        >>> d1.start_ride(r1)
        3
        """
        self.is_idle = False
        self.destination = rider.destination
        return self.get_travel_time(rider.destination)

    def end_ride(self):
        """End the current ride, and arrive at the rider's destination.

        Precondition: The driver has a rider.
        Precondition: self.destination is not None.

        @param Driver self: this driver
        @rtype: None
        """
        self.is_idle, self.location, self.destination = True, self.destination, None
