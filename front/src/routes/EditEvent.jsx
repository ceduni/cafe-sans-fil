// import { useState, useEffect } from "react";
// import { useParams } from "react-router-dom";
// import Container from "@/components/Container";
// import useApi from "@/hooks/useApi";
// import { Helmet } from "react-helmet-async";
// import Breadcrumbs from "@/components/Breadcrumbs";
// import LoadingSpinner from "@/components/LoadingSpinner";
// import MemberOnly from "@/helpers/MemberOnly";
// import EventForm from "./Form/EventForm";

// const EditEvent = () => {
//   const { id: cafeSlug } = useParams();
//   const { data, isLoading, error, refetch } = useApi(`/cafes/${cafeSlug}/events`);
//   const [events, setEvents] = useState([]);

//   useEffect(() => {
//     if (data && data.events) {
//       setEvents(data.events);
//     }
//   }, [data]);

//   const handleEventUpdate = () => refetch();

//   return (
//     <MemberOnly>
//       <Helmet>{data && <title>Édition des événements de {data.name} | Café sans-fil</title>}</Helmet>
//       <Container className="py-10">
//         <Breadcrumbs>
//           <Breadcrumbs.Item link="/">Cafés</Breadcrumbs.Item>
//           <Breadcrumbs.Item link={`/cafes/${cafeSlug}`} isLoading={isLoading}>
//             {data?.name}
//           </Breadcrumbs.Item>
//           <Breadcrumbs.Item>Modifier les événements</Breadcrumbs.Item>
//         </Breadcrumbs>

//         {isLoading && <LoadingSpinner />}

//         {!isLoading && (
//           <>
//             <EventForm cafeSlug={cafeSlug} onEventUpdate={handleEventUpdate} />
//           </>
//         )}
//       </Container>
//     </MemberOnly>
//   );
// };

// export default EditEvent;

import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import Container from "@/components/Container";
import useApi from "@/hooks/useApi";
import { Helmet } from "react-helmet-async";
import Breadcrumbs from "@/components/Breadcrumbs";
import LoadingSpinner from "@/components/LoadingSpinner";
import AdminOnly from "@/helpers/AdminOnly";
import EventCard from "./Board/EventCard";
import toast from 'react-hot-toast';
import { Link } from "react-router-dom";
import authenticatedRequest from "@/helpers/authenticatedRequest";

const EditEvent = () => {
  const { id: cafeSlug } = useParams();
  const navigate = useNavigate();
  const { data, isLoading, error, refetch } = useApi(`/events/`);
  const [events, setEvents] = useState([]);
  const [eventData, setEventData] = useState({
    title: '',
    description: '',
    start_date: '',
    end_date: '',
    image_url: '',
    // ... autres champs si nécessaire
  });

  useEffect(() => {
    if (data && data.events) {
      setEvents(data.events);
    }
  }, [data]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setEventData(prevState => ({ ...prevState, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    toast.promise(  
      authenticatedRequest.post('/events/', eventData),
      {
        loading: 'Création de l\'événement en cours...',
        success: 'Événement créé avec succès!',
        error: 'Erreur lors de la création de l\'événement!',
      }
    ).then(response => {
      if (response.ok) {
        refetch(); // Met à jour la liste des événements
        navigate(`/events`); // Redirigez l'utilisateur après la création
      } else {
        // Gérer les erreurs de réponse ici
      }
    }).catch(error => {
      console.error('Une erreur est survenue lors de la création de l\'événement', error);
    });
  };
  
  

  
 

  return (
    <AdminOnly>
      <Helmet>
      <title>{`Édition des événements de ${data?.name || 'Café sans-fil'}`}</title>
      </Helmet>
      <Container className="py-10">
        <Breadcrumbs>
          <Breadcrumbs.Item link="/">Cafés</Breadcrumbs.Item>
          <Breadcrumbs.Item link={`/cafes/${cafeSlug}`} isLoading={isLoading}>
            {data?.name}
          </Breadcrumbs.Item>
           <Breadcrumbs.Item>Modifier les événements</Breadcrumbs.Item>
         </Breadcrumbs>
        {isLoading && <LoadingSpinner />}

        {!isLoading && (
  <>
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="border-b border-gray-900/10 pb-6">
        <h2 className="text-2xl font-semibold text-gray-900">Éditer Événement</h2>

        <label htmlFor="title" className="block text-sm font-medium text-gray-700 mt-2">
          Titre de l'événement
        </label>
        <input
          id="title"
          name="title"
          type="text"
          value={eventData.title}
          onChange={handleChange}
          placeholder="Titre de l'événement"
          required
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
        />
      </div>
      
      <div className="border-b border-gray-900/10 pb-6">
        <label htmlFor="description" className="block text-sm font-medium text-gray-700 mt-2">Description</label>
        <textarea
          id="description"
          name="description"
          value={eventData.description}
          onChange={handleChange}
          placeholder="Description de l'événement"
          required
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
        />
      </div>

      <div className="border-b border-gray-900/10 pb-6">
        <label htmlFor="start_date">Date et heure de début</label>
        <input
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
        <input
          id="end_date"
          name="end_date"
          type="datetime-local"
          value={eventData.end_date}
          onChange={handleChange}
          
        />
      </div>

      <div>
        <label htmlFor="image_url">URL de l'image</label>
        <input
          id="image_url"
          name="image_url"
          type="url"
          value={eventData.image_url}
          onChange={handleChange}
          placeholder="https://exemple.com/image.jpg"
          required
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
        />
      </div>

      <Link to={`/cafes/${cafeSlug}`} className="leading-6 text-gray-900 px-3 py-2">
              Annuler
            </Link>

      <button type="submit">Sauvegarder l'événement</button>
    </form>

    {events.map((event) => (
      <EventCard
        key={event.event_id}
        event={event}
      />
    ))}
  </>
)}
      </Container>
    </AdminOnly>
  );

};

export default EditEvent;
