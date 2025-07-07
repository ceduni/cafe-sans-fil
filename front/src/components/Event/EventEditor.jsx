import authenticatedRequest from "@/helpers/authenticatedRequest";
import { useAuth } from "@/hooks/useAuth";
import { useState, useEffect } from "react";
import { useLocation, useNavigate, useParams } from "react-router-dom";
import { EventAPI } from "@/utils/api";
import { EventCard } from "@components/Event/EventCard";
import Input from "@/components/Widgets/Input";
import toast from "react-hot-toast";
import { createPortal } from "react-dom";
import Container from "@/components/Layout/Container";
import { Cafe, CafeMenu, CafeMenuItem, Order, User, Event } from "@/models";

const EventEditor = ({isNew}) => {
  const { id } = useParams();
  const {user} = useAuth();
  const location = useLocation();
  const navigate = useNavigate();
  const [event, setEvent] = useState({max_support:3});
  const [cafes, setCafes] = useState([]);


  useEffect(() => {
    //fetching cafes data
    authenticatedRequest.get('/cafes/')
        .then(response => {
          let cafes = response.data.items.map(item => new Cafe(item));
          setCafes(cafes);
        })
        .catch(error => console.error(error));

    //fetch event data
    if (id) authenticatedRequest.get(`/events/${id}`)
        .then(response => setEvent(new Event(response.data)))
        .catch((error) => console.error(error))


  }, []);

  const handleCafeToggle = (cafeId) => {
    const updatedCafes = event?.cafe_ids || [];
    if (updatedCafes.includes(cafeId)) {
        setEvent({ ...event, cafe_ids: updatedCafes.filter(id => id !== cafeId) });
    } else {
        setEvent({ ...event, cafe_ids: [...updatedCafes, cafeId] });
    }
  };

  // What to do if event does exist
  // if (isLoading && isEmpty(storedEvents)) {
  //   return renderEmpty();
  // }


  //const [ event, setEvent ] = useState(null);

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
      console.log(event);
      console.log(isNew);
      if (isNew) {
        //setEvent({ ...event, creator: user.id });
        toast.promise(
            authenticatedRequest.post('/events/', event),
            {
                loading: 'Création de l\'événement en cours...',
                success: 'Événement créé avec succès!',
                error: 'Erreur lors de la création de l\'événement!',
            }
        ).then((response) => {
            console.log(response.data);
            if (response.ok) navigate(location);
        })
      } else {
          toast.promise(
              authenticatedRequest.put(`/events/${event.id}`, event),
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
      setEvent({ ...event, [e.target.name]: e.target.value });
  };

  return (
    <Container>
      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="flex">
          <Container className="w-1/2">
            <h2 className="text-2xl font-semibold text-gray-900">{isNew ? "Creation d'Evenement" : "Édition d'événement"}</h2>
            <div className="border-b border-gray-900/10 pb-6">
              <label htmlFor="title" className="block text-sm font-medium text-gray-700 mt-2">
                Titre de l'événement
              </label>
              <Input
                id="name"
                name="name"
                value={event?.name}
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
                value={event?.description}
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
                value={event?.start_date?.slice(0, 16)}
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
                value={event?.end_date?.slice(0, 16)}
                onChange={handleChange}
              />
            </div>

            <div className="border-b border-gray-900/10 pb-6">
              <label htmlFor="image_url">URL de l'image</label>
              <Input
                id="image_url"
                name="image_url"
                type="url"
                value={event?.image_url}
                onChange={handleChange}
                placeholder="https://exemple.com/image.jpg"
                className="px-4"
              />
            </div>
            <div className="border-b border-gray-900/10 pb-6">
              <label htmlFor="location">Lieu</label>
              <Input
                id="location"
                name="location"
                value={event?.location}
                onChange={handleChange}
                placeholder="Palais Sans-Souci"
                required
                />
            </div>
            <div className="border-b border-gray-900/10 pb-6">
              <label htmlFor="ticket_url">URL de la billeterie</label>
              <Input
                id="ticket_url"
                name="ticket_url"
                type="url"
                value={event?.ticket?.ticket_url}
                onChange={handleChange}
                placeholder="https://exemple.com/tickets"
                className="px-4"
              />
            </div>
            <div className="border-b border-gray-900/10 pb-6">
              <label htmlFor="ticket_price">Prix du billet</label>
              <Input
                id="ticket_price"
                name="ticket_price"
                type="text"
                value={event?.ticket?.ticket_price}
                onChange={handleChange}
                placeholder="30"
                className="px-4"
              />
            </div>
          </Container>
          <div>
            <Container>
              <h2 className="text-2xl font-semibold text-gray-900">Contributeurs</h2>
              <div>
                <label htmlFor="editor">Choisir editeurs</label>
                <Input
                  id="editor"
                  name="editors"
                  value={event?.editors}
                  onChange={handleChange}
                  />
              </div>
              <div>
                <label>Choisir quantité de supporteur</label>
                <div className="flex items-center space-x-2 mt-2">
                  <button
                    type="button"
                    onClick={() => setEvent({ ...event, max_support: Math.max(0, event.max_support - 1) })}
                    className="px-3 py-1 bg-gray-300 rounded hover:bg-gray-400"
                  >
                    ➖
                  </button>
                  <span className="w-6 text-center">{event?.max_support ?? 3}</span>
                  <button
                    type="button"
                    onClick={() => setEvent({ ...event, max_support: Math.min(10, event.max_support + 1) })}
                    className="px-3 py-1 bg-gray-300 rounded hover:bg-gray-400"
                  >
                    ➕
                  </button>
                </div>
              </div>
            </Container>
            <Container>
              <h2 className="text-2xl font-semibold text-gray-900">Publications</h2>
              <div className="grid grid-cols-2 gap-4">
                {cafes.map(cafe => (
                  <label key={cafe.id} className="flex items-center space-x-2">
                    <input
                      type="checkbox"
                      checked={event?.cafe_ids?.includes(cafe.id) || false}
                      onChange={() => handleCafeToggle(cafe.id)}
                    />
                    <span>{cafe.name}</span>
                  </label>
                ))}
              </div>
            </Container>
          </div>
        
        </div>
        <div className="flex items-center justify-between gap-x-6">
          <button
            type="button"
            className="rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-sm \
            hover:bg-red-500 focus-visible:outline focus-visible:outline-2 \
            focus-visible:outline-offset-2 focus-visible:outline-red-600">
            Annuler
          </button>
          <br/>
          <button 
              type="submit"
              className="rounded-md bg-emerald-600 px-3 py-2 text-sm font-semibold text-white shadow-sm \
              hover:bg-emerald-500 focus-visible:outline focus-visible:outline-2 \
              focus-visible:outline-offset-2 focus-visible:outline-emerald-600">
              Sauvegarder
          </button>
        </div>
      </form>
    </Container>
  );

};

export default EventEditor;