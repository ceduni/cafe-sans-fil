
import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import Container from "@/components/Container";
import useApi from "@/hooks/useApi";
import { Helmet } from "react-helmet-async";
import Breadcrumbs from "@/components/Breadcrumbs";

import AdminOnly from "@/helpers/AdminOnly";

import toast from 'react-hot-toast';
import { Link } from "react-router-dom";
import { ClockIcon,BellIcon, BellAlertIcon, HandThumbUpIcon} from "@heroicons/react/24/outline";
import NewsBoard from "./Board/NewsBoard";
import authenticatedRequest from "@/helpers/authenticatedRequest";

import { format, formatDistanceToNow } from 'date-fns';
import { fr } from 'date-fns/locale'; 

const EditNews = () => {
  const { id: cafeSlug } = useParams();
  const { announcementId } = useParams(); 
  const { data: cafeData, isLoading: cafeIsLoading, error: cafeError } = useApi(`/cafes/${cafeSlug}`);
  const { data: announcementsData, isLoading: announcementsIsLoading, error: announcementError, refetch: refetchAnnoucements } = useApi(`/announcements/`);
  const navigate = useNavigate();
  const [announcements, setAnnouncement] = useState([]);
  const [announcementData, setAnnouncementData] = useState({
    title: '',
    content: '',
    timePosted: new Date().toISOString(),
    tags: [],
    buttonText: '',
    likes: 0,
  });
  const [isLoading, setIsLoading] = useState(false);


  useEffect(() => {
    if (cafeData) {
      setAnnouncementData(prevState => ({
        ...prevState,
        cafe_id: cafeData.cafe_id,
      }));
    }
  }, [cafeData]);

  useEffect(() => {
    if (announcementsData) {
      setAnnouncementData(prevState => ({
        ...prevState,
        title: announcementsData[0].title,
        content: announcementsData[0].content,
        start_date: announcementsData[0].start_date || new Date().toISOString(),
        end_date: announcementsData[0].end_date,
        image_url: announcementsData[0].image_url,
      }));
    }
  }, [announcementsData]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setAnnouncementData(prevState => ({ ...prevState, [name]: value }));
  };

  
  const handleSubmit = async (e) => {
    const formattedData = {
      ...announcementData,
      tags: announcementData.tags.split(',').map(tag => tag.trim())  // Transforme la chaîne en tableau et retire les espaces superflus
  };
  
    e.preventDefault();
    toast.promise(
      authenticatedRequest.post('/announcements/', formattedData),
      {
        loading: 'Création de l\'annonce en cours...',
        success: 'Annonce créé avec succès!',
        error: 'Erreur lors de la création de l\'annonce!',
      }
    ).then(response => {
      console.log('Réponse de l\'API:', response.data);
      if (response.ok) {
        setAnnouncement([...announcements, response.data]);
        refetchAnnoucements(); // Met à jour la liste des événements
        navigate(`/cafe/${cafeSlug}`); // Redirigez l'utilisateur après la création
      } else {
     
      }
    }).catch(error => {
      console.error('Une erreur est survenue lors de la création de l\'annonce', error);
    });
  };

  return (
    <AdminOnly cafe={cafeData} error={cafeError}>
      <Helmet>
      <title>{`Édition des annonces de ${announcementData?.title || 'Café sans-fil'}`}</title>
      </Helmet>
      <Container className="py-10">
        <Breadcrumbs>
          <Breadcrumbs.Item link="/">Cafés</Breadcrumbs.Item>
          <Breadcrumbs.Item link={`/cafes/${cafeSlug}`} isLoading={cafeIsLoading}>
            {cafeData?.name}
          </Breadcrumbs.Item>
          <Breadcrumbs.Item>Modifier les annonces</Breadcrumbs.Item>
        </Breadcrumbs>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Formulaire similaire à EditEvent mais pour les annonces */}
          <div className="border-b border-gray-900/10 pb-6">
            <h2 className="text-2xl font-semibold text-gray-900">Éditer Annonce</h2>
            <label htmlFor="title" className="block text-sm font-medium text-gray-700 mt-2">Titre de l'annonce</label>
            <input
              id="title"
              name="title"
              type="text"
              value={announcementData.title}
              onChange={handleChange}
              placeholder="titre de l'annonce"
              required
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
            />
          </div>

          <div className="border-b border-gray-900/10 pb-6">
          <label htmlFor="description" className="block text-sm font-medium text-gray-700">Description</label>
      <textarea
       type="text"
        id="content"
        name="content"
        value={announcementData.description}
        placeholder="description"
        onChange={handleChange}
        required
        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
           
      />
      </div>

<div>
          <label htmlFor="timePosted" className="block text-sm font-medium text-gray-700">
            Temps de publication
          </label>
          {/* <div className="mt-1 flex rounded-md shadow-sm">
            <ClockIcon className="h-5 w-5 text-gray-400" aria-hidden="true" />
            <input
              type="text"
              name="timePosted"
              id="timePosted"
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
              placeholder="HH:mm, DD MM YYYY"
              value={announcementData.timePosted}
              onChange={handleChange}
              required
            />
          </div> */}
          <div className="mt-1 flex rounded-md shadow-sm">
              <ClockIcon className="h-5 w-5 text-gray-400" aria-hidden="true" />
              <input type="text" 
              name="timePosted" 
              id="timePosted" 
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50" 
              placeholder="HH:mm, DD MM YYYY" 
              value={announcementData.timePosted}
               onChange={handleChange} required />
            </div>
        </div>

<div>
          <label htmlFor="tags" className="block text-sm font-medium text-gray-700">
            Tags
          </label>
          <div className="mt-1 flex rounded-md shadow-sm">
            <ClockIcon className="h-5 w-5 text-gray-400" aria-hidden="true" />
            <input
              type="text"
              name="tags"
              id="tags"
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
              placeholder="tag1, tag2, tag3"
              value={announcementData.tags}
              onChange={handleChange}
            />
          </div>
        </div>
          
          {/* Répétez pour les autres champs du formulaire, tels que content, timePosted, etc. */}

          <div className="flex justify-end">
            <Link to={`/cafes/${cafeSlug}`}  className="text-sm text-gray-600 hover:underline">Annuler</Link>
            <button type="submit" className="ml-4 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700">
              {announcementId ? 'Mettre à jour' : 'Créer'} l'annonce
            </button>
          </div>
        </form>
        {announcements.map((news) => (
              <NewsBoard
                key={news.news_id}
                news={news}
              />
            ))}
      </Container>
    </AdminOnly>
  );
};

export default EditNews;
