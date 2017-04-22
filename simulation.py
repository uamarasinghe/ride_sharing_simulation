from container import PriorityQueue
from dispatcher import Dispatcher
from event import Event, create_event_list
from monitor import Monitor


class Simulation:
    """A simulation.

    This is the class which is responsible for setting up and running a
    simulation.

    The API is given to you: your main task is to implement the run
    method below according to its docstring.

    Of course, you may add whatever private attributes and methods you want.
    But because you should not change the interface, you may not add any public
    attributes or methods.

    This is the entry point into your program, and in particular is used for
    auto-testing purposes. This makes it ESSENTIAL that you do not change the
    interface in any way!
    """

    # === Private Attributes ===
    # @type _events: PriorityQueue[Event]
    #     A sequence of events arranged in priority determined by the event
    #     sorting order.
    # @type _dispatcher: Dispatcher
    #     The dispatcher associated with the simulation.

    def __init__(self):
        """Initialize a Simulation.

        @type self: Simulation
        @rtype: None
        """
        self._events = PriorityQueue()
        self._dispatcher = Dispatcher()
        self._monitor = Monitor()

    def run(self, initial_events):
        """Run the simulation on the list of events in <initial_events>.

        Return a dictionary containing statistics of the simulation,
        according to the specifications in the assignment handout.

        @type self: Simulation
        @type initial_events: list[Event]
            An initial list of events.
        @rtype: dict[str, object]
        """
        # TODO
        #  Add all initial events to the event queue.
        for event in initial_events:
            self._events.add(event)
        # Until there are no more events, remove an event
        while len(self._events.items) > 0:
            temp = self._events.remove()
            print(temp)
            if isinstance(temp, Event):
                temp2 = temp.do(self._dispatcher, self._monitor)
                if temp2 is not []:
                    for el in temp2:
                        self._events.add(el)
                else:
                    continue
            else:
                continue
        print(self._dispatcher)
        # from the event queue and do it. Add any returned
        # events to the event queue.
        return self._monitor.report()


if __name__ == "__main__":
    events = create_event_list("events_small.txt")
    sim = Simulation()
    final_stats = sim.run(events)
    print(final_stats)