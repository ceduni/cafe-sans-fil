import { Link } from "react-router-dom";
import Card from "@/components/Card";
import { useAuth } from "@/hooks/useAuth";
import { useState } from "react";
import EventEditor from "@components/Event/EventEditor";


const EventCard = ({event}) => {

    const { user, isLoggedIn } = useAuth();
    const isCreator = event.creator === user?.id;
    const [isEditing, setIsEditing] = useState(false);

    //add a panel to show description and buttons
    //if logged in user is the creator, add button to edit event

    return (
        <Card>
            <Card.Image src={event.image_url} alt={event.name} />
            <Card.Header>
                <Card.Header.Title>{event.name}</Card.Header.Title>
                <Card.Header.Subtitle>{event.location}</Card.Header.Subtitle>
                <Card.Header.Subtitle>{event.hours}</Card.Header.Subtitle>
            </Card.Header>
            <Card.Body>
                <p>{event.description}</p>
                <div>
                    <button onClick={() => setIsEditing(true)}>Modifier</button>

                    {isEditing && (
                        <EventEditor isNew={false} event={event} onClose={() => setIsEditing(false)}/>
                    )}

                </div>
            </Card.Body>
        </Card>
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
