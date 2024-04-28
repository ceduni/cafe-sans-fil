// const EventCard = ({ event }) => {
//     return (
//       <div className="bg-white rounded-lg overflow-hidden shadow-lg transition duration-500 ease-in-out transform hover:-translate-y-1 hover:scale-105">
//         <img className="w-full object-cover h-48" src={event.image_url} alt={event.title} />
//         <div className="p-4">
//           <h3 className="font-bold text-xl mb-2">{event.title}</h3>
//           <p className="text-gray-700 text-base">{event.description}</p>
//         </div>
//         <div className="px-4 pt-4 pb-2">
//           <span className="inline-block bg-blue-100 text-blue-800 rounded-full px-3 py-1 text-sm font-semibold mr-2 mb-2">{event.date}</span>
//           <span className="inline-block bg-blue-100 text-blue-800 rounded-full px-3 py-1 text-sm font-semibold mb-2">{event.time}</span>
//         </div>
//         <div className="px-4 pb-4 flex justify-between">
//           <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
//             Je viens!
//           </button>
//           <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
//             Je supporte!
//           </button>
//         </div>
//       </div>
//     );
//   };
  
//   export default EventCard;



// version 2 
// import AdminOnly from "@/helpers/AdminOnly";

// const EventCard = ({ event,onDelete}) => {
//   // Convertir les chaînes de date de l'API en objets Date JavaScript
//   const startDate = new Date(event.start_date);
//   const endDate = new Date(event.end_date);

//   // Formater les dates pour l'affichage
//   const displayDate = startDate.toLocaleDateString("fr-FR", { day: 'numeric', month: 'long', year: 'numeric' });
//   const displayStartTime = startDate.toLocaleTimeString("fr-FR", { hour: '2-digit', minute: '2-digit' });
//   const displayEndTime = endDate.toLocaleTimeString("fr-FR", { hour: '2-digit', minute: '2-digit' });

//   return (
//     <div className="bg-white rounded-lg overflow-hidden shadow-lg transition duration-500 ease-in-out transform hover:-translate-y-1 hover:scale-105">
//       <img className="w-full object-cover h-48" src={event.image_url} alt={event.title} />
//       <div className="p-4">
//         <h3 className="font-bold text-xl mb-2">{event.title}</h3>
//         <p className="text-gray-700 text-base">{event.description}</p>
//       </div>
//       <div className="px-4 pt-4 pb-2">
//         <span className="inline-block bg-blue-100 text-blue-800 rounded-full px-3 py-1 text-sm font-semibold mr-2 mb-2">{displayDate}</span>
//         <span className="inline-block bg-blue-100 text-blue-800 rounded-full px-3 py-1 text-sm font-semibold mb-2">{`${displayStartTime} - ${displayEndTime}`}</span>
//       </div>
//       <div className="px-4 pb-4 flex justify-between">
//         <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
//           Je viens!
//         </button>
//         <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
//           Je supporte!
//         </button>

//         <AdminOnly>
//         <button
//           onClick={() => onDelete(event.event_id)}
//           className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
//         >
//           Supprimer
//         </button>
//       </AdminOnly>

//       </div>
//     </div>
//   );
// };


import AdminOnly from "@/helpers/AdminOnly";
import useApi from "@/hooks/useApi";
import toast from "react-hot-toast";
import authenticatedRequest from "@/helpers/authenticatedRequest";


const EventCard = ({ event}) => {
  // Convertir les chaînes de date de l'API en objets Date JavaScript
  const startDate = new Date(event.start_date);
  const endDate = new Date(event.end_date);

  // Formater les dates pour l'affichage
  const displayDate = startDate.toLocaleDateString("fr-FR", { day: 'numeric', month: 'long', year: 'numeric' });
  const displayStartTime = startDate.toLocaleTimeString("fr-FR", { hour: '2-digit', minute: '2-digit' });
  const displayEndTime = endDate.toLocaleTimeString("fr-FR", { hour: '2-digit', minute: '2-digit' });

  
  
  const handleDelete = async () => {
    if (confirm('Êtes-vous sûr de vouloir supprimer cet événement ? Cette action est irréversible.')) {
      const toastId = toast.loading('Suppression de l\'événement...');
      try {
        await authenticatedRequest.delete(`/events/${event.event_id}`);
        toast.success('Événement supprimé avec succès', { id: toastId });
        window.location.reload() 
        // Vous devrez peut-être appeler une fonction pour rafraîchir la liste des événements ici, si cela fait partie d'un composant plus large qui affiche plusieurs événements.
      } catch (error) {
        toast.error('Échec de la suppression de l\'événement : ' + error.message, { id: toastId });
      }
    }
  };
return (
  <div className="bg-white rounded-lg overflow-hidden shadow-lg transition duration-500 ease-in-out transform hover:-translate-y-1 hover:scale-105">
      <img className="w-full object-cover h-48" src={event.image_url} alt={event.title} />
      <div className="p-4">
          <h3 className="font-bold text-xl mb-2">{event.title}</h3>
          <p className="text-gray-700 text-base">{event.description}</p>
      </div>
      <div className="px-4 pt-4 pb-2">
         <span className="inline-block bg-blue-100 text-blue-800 rounded-full px-3 py-1 text-sm font-semibold mr-2 mb-2">{displayDate}</span>
         <span className="inline-block bg-blue-100 text-blue-800 rounded-full px-3 py-1 text-sm font-semibold mb-2">{`${displayStartTime} - ${displayEndTime}`}</span>
     </div>
      <div className="px-4 pb-4 flex justify-between">
          <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
              Je viens!
          </button>
          <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
              Je supporte!
          </button>
          <AdminOnly>
              <button
                  onClick={handleDelete}
                  className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
              >
                  Supprimer
              </button>
          </AdminOnly>
      </div>
  </div>
);
};

export default EventCard;

  