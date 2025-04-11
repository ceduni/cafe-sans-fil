import { Link } from "react-router-dom";
import Card from "@/components/Card";
import { useAuth } from "@/hooks/useAuth";
import { useState } from "react";
import EventEditor from "@components/Event/EventEditor";
import { LikeButton, AttendButton, SupportButton } from "@components/Event/EventInteractions";
import { ArrowRightEndOnRectangleIcon as AttendIcon,
    HeartIcon as LikeIcon,
    HandRaisedIcon as SupportIcon,
    PencilIcon as EditIcon,
    CalendarIcon, ShareIcon, TicketIcon } from "@heroicons/react/24/outline";
import { HeartIcon as LikedIcon,
    ArrowRightEndOnRectangleIcon as AttendingIcon,
    HandRaisedIcon as SupportingIcon,
    PencilIcon as EditingIcon } from "@heroicons/react/24/solid";

const EventCard = ({event}) => {

    const { user, isLoggedIn } = useAuth();

    //TODO: change to isContributor after implementing contributor functionality
    const isCreator = true; //event.creator === user?.id;
    const hasTicketing = event?.ticket;
    const [isEditing, setIsEditing] = useState(false);
    const [viewMore, setViewMore] = useState(true);

    //a bit repetitive
    //const [likeCount, setLikeCount] = useState(event.interactions.likes.count);
    //const [attendanceCount, setAttendanceCount] = useState(event.interactions.attend.count);
    //const [supportCount, setSupportCount] = useState(event.interactions.support.count);

    //TODO: add a panel to show description and buttons
    //TODO: fix expandable on card click

    return (
        <Card>
            <div className="relative">
                <Card.Image src={event.image_url} alt={event.name} className="pointer-events-none"/>
                {isCreator && (
                    <button onClick={() => setIsEditing(!isEditing)} className="absolute top-2 right-2 shadow-sm top-2 right-2 bg-white size-10 flex items-center justify-center rounded-full">
                        <EditIcon  className="size-6 text-blue-500" />
                    </button>
                )}
            </div>
                  
            <Card.Header>
                <Card.Header.Title>{event.name}</Card.Header.Title>
                {viewMore && (
                    <div className="flex justify-between">
                        <Card.Header.Subtitle>{event.location}</Card.Header.Subtitle>
                        <Card.Header.Subtitle>{event.start_date}</Card.Header.Subtitle>
                    </div>
                )}
                
            </Card.Header>
            <Card.Body>
                {viewMore && (
                    <p>{event.description}</p>
                )}
                {isEditing && (
                    <EventEditor isNew={false} event={event} onClose={() => setIsEditing(false)}/>
                )}
            </Card.Body>
            <Card.Footer>
            <div className="buttons flex justify-between ">
                <div className="left-side flex gap-2">
                    <LikeButton event={event}/>
                    <AttendButton event={event}/>
                    <SupportButton event={event}/>
                </div>
                <div className="right-side flex gap-2">
                    <button><CalendarIcon className="size-6 text-blue-500" /></button>
                    <div className=""></div>
                    {hasTicketing && (
                        <button><TicketIcon className="size-6 text-blue-500" /></button>
                    )}
                    <button><ShareIcon className="size-6 text-blue-500" /></button>
                </div>
            </div>
            </Card.Footer>
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
