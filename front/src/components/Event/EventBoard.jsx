import { useEffect, useState } from "react";
import EmptyState from "@/components/Error/EmptyState";
import { EventCard, EventCardLoading } from "@/components/Event/EventCard";
import { EventAPI } from "@/utils/api";
//import EventFilters from "@components/Event/EventFilters";


const isEmpty = (arr) => arr?.length === 0;

function filterEvent(event, filters) {
    //possible filters to apply to event list
    const {pavillon, cafe, dateRangeStart, dateRangeEnd} = filters;

    if (event.id == cafe.id) {
        return false;
    }

    return true
}

function renderError(error) {
    return <div className="mt-20 mb-36"><EmptyState type="error" error={error} /></div>;
}

function renderEmpty() {
    // temporary use of CafeCardLoading
    return (
        <div className="grid grid-cols-1 gap-4 py-8 animate-pulse duration-100">
            {Array.from({ length: 10 }).map((_, i) => (
                <EventCardLoading key={i} />
            ))}
        </div>
    )
}

function renderEvents(events, filters, setFilters) {
    const filteredData = events; //.filter((event) => filterEvent(event, filters))

    return (
        <div className="relative bottom-4 xl:bottom-2">
            {/*<EventFilters filters={filters} setFilters={setFilters} events={events} />*/}

            {/* isEmpty(filteredData) && (

                <div className="mt-20 mb-36">
                    <EmptyState name="evenement" />
                </div>
            )*/}

            <div className="grid grid-cols-1 gap-4 py-8 animate-pulse duration-100">
                {filteredData.map((event) => (
                    <EventCard key={event.id} event={event} />
                ))}
            </div>
        </div>
    );
}


const EventBoard = ({ setStoredEvents, storedEvents }) => {
    const [filters, setFilters] = useState({
        //filters
    });

    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

    // Fetching event
    useEffect(() => {
        EventAPI.getAll(setIsLoading)
            .then((data) => {
                setStoredEvents(data);
            })
            .catch((error) => {
                setError(error)
            })
    }, []);

    if (error) {
        console.trace(error);
        return renderError(error);
    }

    if (isLoading && isEmpty(storedEvents)) {
        return renderEmpty();
    }

    return renderEvents(storedEvents, filters, setFilters);
};

export default EventBoard;
