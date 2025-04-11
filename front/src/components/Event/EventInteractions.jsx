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


const LikeButton = ({event}) => {
    const { user, setUser, onAccountDelete, verifyPassword } = useAuth();

    const [count, setCount] = useState(event.interactions?.likes?.count);
    const [liked, setLiked] = useState(event.interactions?.likes?.me);

    console.log(event?.interactions?.likes?.me, event.name);

    const handleLike = async () => {
        setLiked(!liked);
        if (liked) {
            setCount((count) => count - 1);
        } else {
            setCount((count) => count + 1);
        }

        // Create/Replace Interaction
        const toastID = toast.loading("Ajout de l'évènement aux Favoris");
        authenticatedRequest
            .post(`/events/${event.id}/interactions/LIKE/@me`)
            .then((response) => {
                toast.success("Ajouter aux Favoris!");
            })
            .catch((error) => {
                toast.error(console.log(error));
            })
            .finally(() => {
                toast.dismiss(toastID);
            })


        console.log(liked);
    }

    let likeButton;
    if (liked) {
        likeButton = <LikedIcon className="size-6 text-red-500"/>
    } else {
        likeButton = <LikeIcon className="size-6 text-blue-500"/>
    }

    return (
        <div className="flex">
            <p>{count}</p>
            <button onClick={handleLike}>
                {likeButton}
            </button>
        </div>
    )
}

const AttendButton = ({num, state}) => {
    const [count, setCount] = useState(num);
    const [attend, setAttend] = useState(state);

    let attendButton;
    if (attend) {
        attendButton = <AttendingIcon className="size-6 text-blue-500"/>
    } else {
        attendButton = <AttendIcon className="size-6 text-blue-500"/>
    }

    return (
        <div className="flex">
            <p>{count}</p>
            <button onClick={() => {setAttend(!attend)} }>
                {attendButton}
            </button>
        </div>
    )
}

const SupportButton = ({num, state}) => {
    const [count, setCount] = useState(num);
    const [support, setSupport] = useState(state);

    let supportButton;
    if (support) {
        supportButton = <SupportingIcon className="size-6 text-blue-500"/>
    } else {
        supportButton = <SupportIcon className="size-6 text-blue-500"/>
    }

    return (
        <div className="flex">
            <p>{count}</p>
            <button onClick={() => setSupport(!support)}>
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