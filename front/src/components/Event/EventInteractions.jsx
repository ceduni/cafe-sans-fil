import authenticatedRequest from "@/helpers/authenticatedRequest";
import { useState, useEffect } from "react";
import { useAuth } from "@/hooks/useAuth";
import toast from "react-hot-toast";
import { ArrowRightCircleIcon as AttendIcon,
    HeartIcon as LikeIcon,
    HandRaisedIcon as SupportIcon,
    PencilIcon as EditIcon,
    CalendarIcon, ShareIcon, TicketIcon } from "@heroicons/react/24/outline";
import { HeartIcon as LikedIcon,
    CheckCircleIcon as AttendingIcon,
    HandRaisedIcon as SupportingIcon,
    PencilIcon as EditingIcon } from "@heroicons/react/24/solid";

const InteractiveButton = ({type, event, onclick}) => {
    const [state, setState] = useState(event.interactions?.[type]?.me || false);
    const [count, setCount] = useState(event.interactions?.[type]?.count || 0);

    let activeIcon, inactiveIcon;

    switch (type) {
        case "LIKE":
            activeIcon = <LikedIcon className="size-6 text-red-500"/>
            inactiveIcon= <LikeIcon className="size-6 text-blue-500"/>
            break;
        case "DISLIKE":
            activeIcon = <LikedIcon className="size-6 text-red-500"/>
            inactiveIcon= <LikeIcon className="size-6 text-blue-500"/>
            break;
        case "ATTEND":
            activeIcon = <AttendingIcon className="size-6 text-blue-500"/>
            inactiveIcon= <AttendIcon className="size-6 text-blue-500"/>
            break;
        case "SUPPORT":
            activeIcon = <SupportingIcon className="size-6 text-blue-500"/>
            inactiveIcon= <SupportIcon className="size-6 text-blue-500"/>
            break;
        default:
            console.log("Unknown type");
    }

    const handleClick = () => {
        if (state) {
            setCount(count - 1);
            authenticatedRequest
                .delete(`/events/${event.id}/interactions/${type}/@me`)
                .then((response) => {
                    toast.success("Favoris!");
                })
                .catch((error) => {
                    toast.error("Erreur");
                })
        } else {
            setCount(count + 1);
            authenticatedRequest
                .post(`/events/${event.id}/interactions/${type}/@me`)
                .then((response) => {
                    toast.success("Ajouter"); //custome message per interaction type
                })
                .catch((error) => {
                    toast.error(console.log(error));
                })
        }
        setState(!state);
    }

    return (
        <div className="flex">
            <p>{count}</p>
            <button onClick={handleClick}>
                {state ? activeIcon : inactiveIcon}
            </button>
        </div>
    )
}

export { InteractiveButton };