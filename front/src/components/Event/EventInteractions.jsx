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


const registerInteraction = async (type, state, event) => {
    if (state) {
        authenticatedRequest
            .delete(`/events/${event.id}/interactions/${type}/@me`)
            .then((response) => {
                //toast.success("Favoris!");
            })
            .catch((error) => {
                toast.error(console.log(error));
            })
    } else {
        authenticatedRequest
            .post(`/events/${event.id}/interactions/${type}/@me`)
            .then((response) => {
                toast.success("Ajouter"); //custome message per interaction type
            })
            .catch((error) => {
                toast.error(console.log(error));
            })
    }
}

// TODO: Refactor

const LikeButton = ({event}) => {
    const { user, setUser, onAccountDelete, verifyPassword } = useAuth();

    const [count, setCount] = useState(event.interactions?.likes?.count);
    const [liked, setLiked] = useState(event.interactions?.likes?.me || false);

    let likeButton;
    if (liked) {
        likeButton = <LikedIcon className="size-6 text-red-500"/>
    } else {
        likeButton = <LikeIcon className="size-6 text-blue-500"/>
    }

    const handleClick = () => {
        setLiked(!liked);
        if (liked) {
            setCount(count - 1);
        } else {
            setCount(count + 1);
        }

        registerInteraction("LIKE", liked, event);
    }

    return (
        <div className="flex">
            <p>{count}</p>
            <button onClick={handleClick}>
                {likeButton}
            </button>
        </div>
    )
}

const AttendButton = ({event}) => {
    const [count, setCount] = useState(event.interactions?.attend?.count);
    const [attend, setAttend] = useState(event.interactions?.attend?.me);

    let attendButton;
    if (attend) {
        attendButton = <AttendingIcon className="size-6 text-blue-500"/>
    } else {
        attendButton = <AttendIcon className="size-6 text-blue-500"/>
    }

    const handleClick = () => {
        setAttend(!attend);
        if (attend) {
            setCount(count - 1);
        } else {
            setCount(count + 1);
        }

        registerInteraction("ATTEND", attend, event);
    }

    return (
        <div className="flex">
            <p>{count}</p>
            <button onClick={handleClick}>
                {attendButton}
            </button>
        </div>
    )
}

const SupportButton = ({event}) => {
    const [count, setCount] = useState(event.interactions?.support?.count);
    const [support, setSupport] = useState(event.interactions?.support?.me);

    let supportButton;
    if (support) {
        supportButton = <SupportingIcon className="size-6 text-blue-500"/>
    } else {
        supportButton = <SupportIcon className="size-6 text-blue-500"/>
    }

    const handleClick = () => {
        setSupport(!support);
        if (support) {
            setCount(count - 1);
        } else {
            setCount(count + 1);
        }

        registerInteraction("SUPPORT", support, event);
    }

    return (
        <div className="flex">
            <p>{count}</p>
            <button onClick={handleClick}>
                {supportButton}
                <span className="absolute bottom-full mb-2 left-1/2 -translate-x-1/2 
                   bg-gray-800 text-white text-xs rounded py-1 px-2 
                   opacity-0 hover:opacity-100 transition">
            Supporter
            </span>
            </button>
            
        </div>
    )
}

export {LikeButton, AttendButton, SupportButton};