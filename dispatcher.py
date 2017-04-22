from driver import Driver
from location import Location
from rider import Rider, WAITING, CANCELLED, SATISFIED

# green checkmark cannot happen cause request_driver != request_driver


class Dispatcher:
    """A dispatcher fulfills requests from riders and drivers for a
    ride-sharing service.

    When a rider requests a driver, the dispatcher assigns a driver to the
    rider. If no driver is available, the rider is placed on a waiting
    list for the next available driver. A rider that has not yet been
    picked up by a driver may cancel their request.

    When a driver requests a rider, the dispatcher assigns a rider from
    the waiting list to the driver. If there is no rider on the waiting list
    the dispatcher does nothing. Once a driver requests a rider, the driver
    is registered with the dispatcher, and will be used to fulfill future
    rider requests.
    """

    def __init__(self):
        """Initialize a Dispatcher.

        @param Dispatcher self:
        @rtype: None
        """

        self.rider = {WAITING: [], CANCELLED: [], SATISFIED: []}
        self.driver = {'idle': [], 'total': []}

    def __str__(self):
        """Return a string representation.

        @param Dispatcher self: this dispatcher
        @rtype: str

        >>> disp = Dispatcher()
        >>> print(disp)
        rider's statuses:
         - waiting riders: []
         - cancelled requests: []
         - satisfied riders: []
         driver's statuses:
         -idle drivers: []
         -total drivers: []
        """
        return ("rider's statuses:\n - waiting riders: {}\n - cancelled requests: {}\n - satisfied riders: {}\n \
driver's statuses:\n -idle drivers: {}\n -total drivers: {}".format(self.rider[WAITING],
                                                                    self.rider[CANCELLED],
                                                                    self.rider[SATISFIED],
                                                                    self.driver['idle'],
                                                                    self.driver['total']))

    def request_driver(self, rider):
        """Return a driver for the rider, or None if no driver is available.

        Add the rider to the waiting list if there is no available driver.

        @param Dispatcher self: this dispatcher
        @param Rider rider: the rider
        @rtype: Driver | None

        >>> dis = Dispatcher()
        >>> d1 = Driver('Sam', Location(1,1), 2)
        >>> r1 = Rider('xyz', Location(1,1), Location(6,6), 4)
        >>> dis.request_driver(r1)

        >>> dis.driver['idle'].append(d1)
        >>> dis.request_driver(r1)
        ID: Sam, Location: (1,1), Speed: 2
        """
        # add rider to WAITING
        self.rider[WAITING].append(rider)

        # Find the driver with the shortest arrival time and assign to rider
        while self.driver['idle']:
            # eta is a list of the expected arrival times for each idle driver
            eta = [driver.get_travel_time(rider.origin) for driver in self.driver['idle']]
            min_eta = min(eta)
            # find the corresponding driver for the min_eta
            for driver in self.driver['idle']:
                if driver.get_travel_time(rider.origin) == min_eta:
                    return driver

    def request_rider(self, driver):
        """Return a rider for the driver, or None if no rider is available.

        If this is a new driver, register the driver for future rider requests.

        @param Dispatcher self: this dispatcher
        @param Driver driver: the driver
        @rtype: Rider | None

        >>> dis = Dispatcher()
        >>> d1 = Driver('Sam', Location(1,1), 2)
        >>> r1 = Rider('xyz', Location(1,1), Location(6,6), 4)
        >>> dis.request_rider(d1)

        >>> dis.rider[WAITING].append(r1)
        >>> dis.request_rider(d1)
        ID: xyz, Origin: (1,1), Destination: (6,6), Status: waiting, Patience: 4
        """

        # if driver is new, add driver to total list of drivers
        if driver not in self.driver['total']:
            self.driver['total'].append(driver)
            # if driver is currently idle, add to list of idle drivers
            if driver.is_idle:
                self.driver['idle'].append(driver)

        # if there are riders waiting for a driver to be assigned to them, the return the longest waiting rider
        if self.rider[WAITING] != []:
            return self.rider[WAITING][0]
        else:
            return None

    def cancel_ride(self, rider):
        """Cancel the ride for rider.

        @param Dispatcher self: this dispatcher
        @param Rider rider: the rider
        @rtype: None
        """
        # If the rider is currently waiting, remove from waiting list and append to cancelled list
        if rider in self.rider[WAITING]:
            index_ = self.rider[WAITING].index(rider)
            self.rider[WAITING].pop(index_)
            self.rider[CANCELLED].append(rider)

    def end_successful_ride(self, rider):
        """End successful ride for the rider.

        @param Dispatcher self: this dispatcher
        @param Rider rider: the rider
        @rtype: None
        """
        # if rider is currently waiting, remove from waiting list and add to satisfied list.
        if rider in self.rider[WAITING]:
            index_ = self.rider[WAITING].index(rider)
            self.rider[WAITING].pop(index_)
            self.rider[SATISFIED].append(rider)
