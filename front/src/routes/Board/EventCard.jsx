import { isAdmin } from "@/utils/admin";
import { useAuth } from "@/hooks/useAuth";
import useApi from "@/hooks/useApi";
import toast from "react-hot-toast";
import authenticatedRequest from "@/helpers/authenticatedRequest";
import { useNavigate } from "react-router-dom";


const EventCard = ({cafe, event}) => {
  // Convertir les chaînes de date de l'API en objets Date JavaScript
  const startDate = new Date(event.start_date);
  const endDate = new Date(event.end_date);
  const { user } = useAuth();

  // Formater les dates pour l'affichage
  const displayDate = startDate.toLocaleDateString("fr-FR", { day: 'numeric', month: 'long', year: 'numeric' });
  const displayStartTime = startDate.toLocaleTimeString("fr-FR", { hour: '2-digit', minute: '2-digit' });
  const displayEndTime = endDate.toLocaleTimeString("fr-FR", { hour: '2-digit', minute: '2-digit' });

  const navigate = useNavigate();

  // const handleEdit = () => {
  //   navigate(`/edit/events/${event.event_id}`); 
  // };
  
  const handleDelete = async () => {
    if (confirm('Êtes-vous sûr de vouloir supprimer cet événement ? Cette action est irréversible.')) {
      const toastId = toast.loading('Suppression de l\'événement...');
      try {
        await authenticatedRequest.delete(`/events/${event.event_id}`);
        toast.success('Événement supprimé avec succès', { id: toastId });
        window.location.reload() 
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
          {cafe && !isAdmin(cafe, user?.username) ? null : (
              <button
                  onClick={handleDelete}
                  className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
              >
                  Supprimer
              </button>
          )}
      </div>
  </div>
);
};

export default EventCard;

  