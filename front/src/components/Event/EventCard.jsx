import { Link } from "react-router-dom";
import Card from "@/components/Card";
import { displayCafeLocation } from "@/utils/cafe";
import { CafeAPI } from "@/utils/api";

const EventCard = ({event}) => {

    const cafeLocation = displayCafeLocation(CafeAPI.get(event.id).location);

    return (
        <Link
            to={`/events/${event.slug}`}
            state={event}
            className="contents select-non"
            onKeyDown={(e) => e.key === "Enter" && e.target.click()}>
            <Card>
                <Card.Image src={event.image} alt={event.name} />
                <Card.Header>
                    <Card.Header.Title>{event.name}</Card.Header.Title>
                    <Card.Header.Subtitle>{cafeLocation}</Card.Header.Subtitle>
                    <Card.Header.Subtitle>{event.hours}</Card.Header.Subtitle>
                </Card.Header>
                <Card.Body>
                    <p>{event.description}</p>
                </Card.Body>
            </Card>
        </Link>
    )
}


const EventCardLoading = () => {
    return (
        <Card>
            <Card.Header>
                <Card.Header.Title as="div">
                    <div className="h-14 sm:h-16 bg-white rounded-full mb-2.5"></div>
                </Card.Header.Title>
                <Card.Header.Subtitle as="div">

                </Card.Header.Subtitle>
            </Card.Header>
            <Card.Body>
                <div className="h-2.5 bg-gray-200 rounded-full mb-2.5 w-3/4"></div>
                <div className="h-2.5 bg-gray-200 rounded-full mb-2.5"></div>
                <div className="h-2.5 bg-gray-200 rounded-full mb-2.5 w-3/4"></div>
            </Card.Body>
        </Card>
  );
};

export { EventCard, EventCardLoading };
