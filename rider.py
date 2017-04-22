from location import Location

WAITING = "waiting"
CANCELLED = "cancelled"
SATISFIED = "satisfied"

"""
The rider module contains the Rider class. It also contains
constants that represent the status of the rider.

=== Constants ===
@type WAITING: str
    A constant used for the waiting rider status.
@type CANCELLED: str
    A constant used for the cancelled rider status.
@type SATISFIED: str
    A constant used for the satisfied rider status
"""


class Rider:
    """
    A rider using the ride-sharing service.

    === Attributes ===
    @param str identifier: unique identifier for each rider
    @param Location origin: where the Rider will be picked up by Driver
    @param Location destination: where Rider will be dropped off by Driver
    @param object status: One of the constants above
    @param int patience: number of units the rider will wait to be picked up
    before they cancel
    """

    def __init__(self, identifier, origin, destination, patience, status=WAITING):
        """
        Create instance of class Rider.

        @param str identifier: unique identifier for each rider
        @param Location origin: where the Rider will be picked up by Driver
        @param Location destination: where Rider will be dropped off by Driver
        @param object status: One of the constants above
        @param int patience: number of units the rider will wait to be picked up
         before they cancel
        @rtype None
        """
        self.identifier = identifier
        self.origin = origin
        self.destination = destination
        self.status = status
        self.patience = patience

    def __eq__(self, other):
        """
        Return whether Rider self is equivalent to Rider other.

        @param Rider self: this Rider
        @param Rider | object other: Any object to compare to self
        @rtype: bool

        >>> r1 = Rider('xyz', Location(1,1), Location(6,6), 4)
        >>> r2 = Rider('xyz', Location(1,1), Location(6,6), 4)
        >>> r3 = Rider('abc', Location(1,3), Location(6,3), 4)
        >>> r1 == r2
        True
        >>> r1 == r3
        False

        """

        return(type(self) == type(other) and
               self.identifier == other.identifier and
               self.origin == other.origin and
               self.destination == other.destination and
               self.status == other.status and
               self.patience == other.patience)

    def __str__(self):
        """
        Return a string representation of instance of Rider self.

        @param Rider self:
        @rtype: str

        >>> r1 = Rider('xyz', Location(1,1), Location(6,6), 4)
        >>> print(r1)
        ID: xyz, Origin: (1,1), Destination: (6,6), Status: waiting, Patience: 4
        >>> r3 = Rider('abc', Location(1,3), Location(6,3), 4)
        >>> print(r3)
        ID: abc, Origin: (1,3), Destination: (6,3), Status: waiting, Patience: 4

        """

        return "ID: {}, Origin: {}, Destination: {}, Status: {}, Patience: {}".\
            format(self.identifier, self.origin, self.destination, self.status,
                   self.patience)

    def __repr__(self):
        """
        Returns a string representation when self is called.

        @param Rider self:
        @rtype: str

        >>> r1 = Rider('xyz', Location(1,1), Location(6,6), 4)
        >>> r1
        ID: xyz, Origin: (1,1), Destination: (6,6), Status: waiting, Patience: 4
        >>> r3 = Rider('abc', Location(1,3), Location(6,3), 4)
        >>> r3
        ID: abc, Origin: (1,3), Destination: (6,3), Status: waiting, Patience: 4
        """
        return str(self)
