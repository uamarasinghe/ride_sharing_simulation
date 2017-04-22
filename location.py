class Location:
    """A location on a grid made of non-negative integers.

    === Attributes ===
    @param int row: non-negative int
    @param int column: non-negative int
    """

    def __init__(self, row, column):
        """Initialize a location.

        @param Location self: this Location
        @param int row: non-negative int
        @param int column: non-negative int
        @rtype: None
        """
        self.row, self.column = row, column

    def __str__(self):
        """Return a string representation.

        @param Location self: this Location
        @rtype: str

        >>> l = Location(2, 3)
        >>> print(l)
        (2, 3)
        >>> l2 = Location(1, 2)
        >>> print(l2)
        (1, 2)
        """
        return '({},{})'.format(self.row, self.column)

    def __eq__(self, other):
        """Return True if self equals other, and false otherwise.

        @param Location self: this Location
        @param Location | object other: object being compared to self
        @rtype: bool

        >>> l = Location(2, 3)
        >>> l2 = Location(1, 2)
        >>> l3 = Location(2, 3)
        >>> l == l3
        True
        >>> l2 == l
        False
        """
        return type(self) == type(other) and self.row == other.row and self.column == other.column


def manhattan_distance(origin, destination):
    """Return the Manhattan distance between the origin and the destination.

    @param Location origin: the initial location
    @param Location destination: the final location
    @rtype: int

    >>> l = Location(1, 1)
    >>> l2 = Location(6, 6)
    >>> manhattan_distance(l, l2)
    10
    >>> l3 = Location(3, 5)
    >>> manhattan_distance(l, l3)
    6
    """
    return abs(int(origin.row) - int(destination.row)) + abs(int(origin.column) - int(destination.column))


def deserialize_location(location_str):
    """Deserialize a location.

    Precondition: location_str will be of format x,y ; where x and y are ints

    @param location_str: str
        A location in the format 'row,col'
    @rtype: Location

    >>> str1 = '3,2'
    >>> l1 = deserialize_location(str1)
    >>> print(l1)
    (3, 2)
    >>> str2 = '6,2'
    >>> l2 = deserialize_location(str2)
    >>> print(l2)
    (6, 2)
    """
    return Location(location_str[0], location_str[2])
