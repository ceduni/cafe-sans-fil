import { useParams } from "react-router-dom";
import { useState, useEffect } from "react";
import useTitle from "@/hooks/useTitle";
import { EventCard, EventCardLoading } from "./EventCard";
import { InteractiveButton } from "./EventInteractions";
import { EventAPI } from "@/utils/api";
import EmptyState from "@/components/Error/EmptyState";


function EventImage({image, alt}) {
    if (!image){
        return null
    }

    return <img className="event-image" src={image} alt={alt} />;
}

function EventHeader({event}) {
    return (
        <header className={`relative h-[400px] flex items-end justify0between overflow-hidden;`} style={{background: `url(${event.image_url}) center / cover no-repeat`}}>
            <div className="event-interactions">
                <EventImage image={event?.image_url} alt={t("alt.image_url")} />
                <ul className="bare-list interactions">
                    <InteractiveButton type={"LIKE"} event={event} />
                    <InteractiveButton type={"ATTEND"} event={event} />
                    <InteractiveButton type={"SUPPORT"} event={event} />
                </ul>
            </div>
        </header>
    )
}

const Event = () => {
    const { id } = useParams();

    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);
    const [event, setEvent] = useState(null);

    console.log("prefetch");

    // Fetching cafe
    useEffect(() => {
        EventAPI.get(id, setIsLoading)
            .then((data) => {
                setEvent(data);
                console.log(data);
            })
            .catch((error) => {
                console.error(error);
                setError(error);
                console.log("yoooooo");
            })
    }, []);

    useTitle(event?.name && `${event.name} | ${APP_NAME}`)

    if (error) {
        if (error.status === 404) {
            throw new Response("Not found", { status: 404, statusText: t("error.404.cafe_not_found") });
        }

        return <EmptyState type="error" error={error} />;
    }

    if (isLoading) {
        return <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 py-8 animate-pulse duration-100"></div>
    }

    return (
        <div className="relative bottom-4 grid">
            <EventHeader event={event}></EventHeader>
            <section className="main-body">
                <div className="menu-section">
                    <div>
                        <h2 className="text-center my-0 text-3xl font-bold">Menu</h2>
                    </div>
                    <EventCardLoading />
                </div>
                <EventCard event={event} />
            </section>
        </div>
    )
}

export default Event;