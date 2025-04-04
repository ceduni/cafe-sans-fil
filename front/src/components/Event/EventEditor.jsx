import authenticatedRequest from "@/helpers/authenticatedRequest";
import { useState, useEffect } from "react";
import { useLocation, useNavigate, useParams } from "react-router-dom";
import { EventCard } from "@components/Event/EventCard";
import Input from "@/components/Widgets/Input";
import toast from "react-hot-toast";
import { createPortal } from "react-dom";
import { useAuth } from "@/hooks/useAuth";

const EventEditor = ({isNew, event, onClose}) => {
    const location = useLocation();
    const navigate = useNavigate();
    const [previousPage, setPreviousPage] = useState(null);

    // Déterminer la page d'origine de l'action edit/create
    useEffect(() => {
        setPreviousPage(location.state?.from || "/");
    }, [location]);


    //const [ event, setEvent ] = useState(null);
    const { user, setUser, onAccountDelete, verifyPassword } = useAuth();
    const [eventData, setEventData] = useState({
        name: event.name,
        description: event.description,
        start_date: event.start_date.substr(0,16),
        end_date: event.end_date.substr(0,16),
        image_url: event.image_url,
        location: event.location,
      });

    // useEffect(() => {
    //     const fetchEvent = async () => {
    //         authenticatedRequest
    //             .get(`/events/`)
    //             .then((response) => {
    //                 const event = response.data.filter((event) => event.id === eventID);
    //                 setEvent(event);
    //                 if (!event) {
    //                     //handle event doesnt exist
    //                 }
    //             })
    //             .catch((error) => {
    //                 //handle error
    //             })
    //     }
    // })

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (isNew) {
            toast.promise(
                (await authenticatedRequest.post('/events/'), eventData),
                {
                    loading: 'Création de l\'événement en cours...',
                    success: 'Événement créé avec succès!',
                    error: 'Erreur lors de la création de l\'événement!',
                }
            ).then((response) => {
                if (response.ok) {
                    //navigate('/'); //eventually redirect to /me/events
                }
            })
        } else {
            toast.promise(
                authenticatedRequest.put(`/events/${event.id}`, eventData),
                {
                    loading: "Mise à jour de l'évènement",
                    success: "Évènement mis à jour avec succès!",
                    error: "Erreur survenue lors de la mise à jour"
                }
            )
        }
        //navigate(previousPage);
    };

    const handleChange = (e) => {
        setEventData({ ...eventData, [e.target.name]: e.target.value });
    };

    //TODO: add management section for adding contributors and ticketing link...

    return (
        <div>
        <form onSubmit={handleSubmit} className="space-y-6">
        <h2 className="text-2xl font-semibold text-gray-900">Édition d'événement</h2>
          <div className="border-b border-gray-900/10 pb-6">
            <label htmlFor="title" className="block text-sm font-medium text-gray-700 mt-2">
              Titre de l'événement
            </label>
            <Input
              id="title"
              name="title"
              value={eventData.name}
              onChange={handleChange}
              placeholder="Titre de l'événement"
              required
            />
          </div>

          <div className="border-b border-gray-900/10 pb-6">
            <label htmlFor="description" className="block text-sm font-medium text-gray-700 mt-2">Description</label>
            <textarea
              id="description"
              name="description"
              value={eventData.description}
              onChange={handleChange}
              rows={6}
              placeholder="Description de l'événement"
              required
              className="px-4 mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
            />
          </div>

          <div className="border-b border-gray-900/10 pb-6">
            <label htmlFor="start_date">Date et heure de début</label>
            <Input
              id="start_date"
              name="start_date"
              type="datetime-local"
              value={eventData.start_date}
              onChange={handleChange}
              required
            />
          </div>

          <div className="border-b border-gray-900/10 pb-6">
            <label htmlFor="end_date">Date et heure de fin</label>
            <Input
              id="end_date"
              name="end_date"
              type="datetime-local"
              value={eventData.end_date}
              onChange={handleChange}
            />
          </div>

          <div>
            <label htmlFor="image_url">URL de l'image</label>
            <Input
              id="image_url"
              name="image_url"
              type="url"
              value={eventData.image_url}
              onChange={handleChange}
              placeholder="https://exemple.com/image.jpg"
              className="px-4"
            />
          </div>
          <div>
            <label htmlFor="image_url">Lieu</label>
            <Input
              id="location"
              name="location"
              value={eventData.location}
              onChange={handleChange}
              placeholder="Palais Sans-Souci"
              />
          </div>
        
            <div className="flex items-center justify-end gap-x-6">
                <button 
                    onClick={onClose}
                    className="rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-sm \
                    hover:bg-red-500 focus-visible:outline focus-visible:outline-2 \
                    focus-visible:outline-offset-2 focus-visible:outline-red-600">
                    Annuler</button>
                <br/>
                <button 
                    type="submit"
                    className="rounded-md bg-emerald-600 px-3 py-2 text-sm font-semibold text-white shadow-sm \
                    hover:bg-emerald-500 focus-visible:outline focus-visible:outline-2 \
                    focus-visible:outline-offset-2 focus-visible:outline-emerald-600">
                    Sauvegarder</button>
            </div>
        </form>
      </div>
    );

};

export default EventEditor;