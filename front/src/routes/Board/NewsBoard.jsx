import { ClockIcon, BellIcon, BellAlertIcon, HandThumbUpIcon } from "@heroicons/react/24/outline";
import { Transition } from '@headlessui/react';
import { isAdmin } from "@/utils/admin";
import { useAuth } from "@/hooks/useAuth";
import toast from "react-hot-toast";
import authenticatedRequest from "@/helpers/authenticatedRequest";
import { useState, useEffect } from "react";

const NewsBoard = ({ cafe, news }) => {
  const { user } = useAuth();
  const [visibleNews, setVisibleNews] = useState(2);
  const [likes, setLikes] = useState(news.map(n => n.likes.length));

  useEffect(() => {
    setLikes(news.map(n => n.likes.length));
  }, [news]);

  const handleLike = (index) => {
    const newLikes = [...likes];
    newLikes[index] += 1;
    setLikes(newLikes);
    // Ici, ppeler l'API pour mettre à jour les likes sur le serveur.
  };

  const handleMore = () => {
    setVisibleNews(prev => Math.min(news.length, prev + 2));
  };

  const handleLess = () => {
    setVisibleNews(prev => Math.max(2, prev - 2));
  };

  const handleDelete = async (announcementId) => {
    if (!announcementId) {
      console.error('Tentative de suppression sans ID valide');
      return toast.error('ID de l\'annonce non disponible.');
    }
    if (confirm('Êtes-vous sûr de vouloir supprimer cet annonce ? Cette action est irréversible.')) {
      const toastId = toast.loading('Suppression de l\'annonce...');
      try {
        await authenticatedRequest.delete(`/announcements/${announcementId}`);
        toast.success('Annonce supprimée avec succès', { id: toastId });
        window.location.reload();
      } catch (error) {
        toast.error('Échec de la suppression de l\'annonce: ' + error.message, { id: toastId });
      }
    }
  };

  return (
    <div className="bg-white shadow rounded-lg p-4">
      <h2 className="text-lg font-bold text-gray-800 flex items-center mb-4">
        Annonces
        <span className="ml-2 text-red-600 group">
          <BellIcon className="h-5 w-5 flex-shrink-0 text-gray-400 group-hover:hidden mr-2" aria-hidden="true"/>
          <BellAlertIcon className="h-5 w-5 flex-shrink-0 text-gray-400 hidden group-hover:block mr-2" aria-hidden="true"/>
        </span>
      </h2>
      {news.slice(0, visibleNews).map((item, index) => (
        <Transition
          show={true}
          enter="transition duration-500 ease-out"
          enterFrom="transform scale-95 opacity-0"
          enterTo="transform scale-100 opacity-100"
          leave="transition duration-500 ease-in"
          leaveFrom="transform scale-100 opacity-100"
          leaveTo="transform scale-95 opacity-0"
          key={item.announcement_id || index}
          className="mb-4 last:mb-0 bg-gray-400 p-3 rounded"
        >
          <div className="flex items-center justify-between">
            <h3 className="text-md font-semibold text-gray-900">{item.title}</h3>
            <span className="flex text-sm text-blue-600">
              <ClockIcon className="h-5 w-5 flex-shrink-0 text-blue-600 group-hover:text-gray-500 mr-2" aria-hidden="true"/>
              {item.timePosted ? new Date(item.timePosted).toLocaleString() : 'Date non spécifiée'}
            </span>
          </div>
          <p className="text-sm text-black mt-1">{item.content}</p>
          <div className="flex items-center mt-2">
            {item.tags.map((tag, idx) => (
              <span key={idx} className="text-xs font-semibold inline-block py-1 px-2 uppercase rounded text-blue-600 bg-blue-200 last:mr-0 mr-1">
                {tag}
              </span>
            ))}
          </div>
          <div className="flex items-center justify-between mt-2">
            {/* <button className="text-xs text-blue-600 border border-blue-600 rounded py-1 px-3 hover:bg-blue-600 hover:text-white transition-colors duration-300">
              {item.buttonText || "Learn More"}
            </button> */}
            {cafe && isAdmin(cafe, user?.username) && (
              <button
                onClick={() => handleDelete(item.announcement_id)}
                className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
              >
                Supprimer
              </button>
            )}
            <button onClick={() => handleLike(index)} className="flex items-center px-3 py-2 border border-blue-600 text-blue-600 hover:bg-blue-600 hover:text-white transition-colors duration-300 rounded">
    <HandThumbUpIcon className="h-5 w-5 flex-shrink-0 mr-2" aria-hidden="true"/>
    {likes[index]}
            </button>
          </div>
        </Transition>
      ))}
      <div className="flex justify-center mt-6 space-x-3">
        {visibleNews > 2 && (
          <button onClick={handleLess} className="text-md text-blue-600 hover:underline">
            Voir moins
          </button>
        )}
        {visibleNews < news.length && (
          <button onClick={handleMore} className="text-md text-blue-600 hover:underline">
            Voir plus
          </button>
        )}
      </div>
    </div>
  );
};

export default NewsBoard;
