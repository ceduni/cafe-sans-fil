// import EventCard from "./EventCard";

// const EventBoard = ({ events }) => {
//     return (
//       <div className="container mx-auto my-8 p-4 bg-gray-100 rounded-lg shadow-lg">
//         <h2 className="text-3xl font-bold text-center text-gray-800 mb-8">Tableau d'affichage</h2>
//         <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
//           {/* {events.map((event, index) => (
//             <EventCard key={index} event={event} />
//           ))} */}
//           {events.map(event => (
//   <EventCard key={event.event_id} event={event} />
// ))}
//         </div>
//       </div>
//     );
//   };
  
//   export default EventBoard;

// import React, { useState } from 'react';
// import EventCard from './EventCard';

// const EventBoard = ({ events }) => {
//   const [currentIndex, setCurrentIndex] = useState(0);
//   const itemsPerPage = 3;
//   const maxIndex = Math.ceil(events.length / itemsPerPage) - 1;

//   const goToNext = () => {
//     setCurrentIndex((prevIndex) => (prevIndex < maxIndex ? prevIndex + 1 : prevIndex));
//   };

//   const goToPrevious = () => {
//     setCurrentIndex((prevIndex) => (prevIndex > 0 ? prevIndex - 1 : prevIndex));
//   };

//   const startIndex = currentIndex * itemsPerPage;
//   const endIndex = startIndex + itemsPerPage;
//   const itemsToShow = events.slice(startIndex, endIndex);

//   return (
//     <div className="container mx-auto my-8 p-4 bg-gray-100 rounded-lg shadow-lg">
//       <h2 className="text-3xl font-bold text-center text-gray-800 mb-8">Tableau d'affichage</h2>
//       <div className="flex overflow-hidden">
//         {itemsToShow.map((event) => (
//           <div key={event.event_id} className="min-w-0 flex-1 px-2">
//             <EventCard event={event} />
//           </div>
//         ))}
//       </div>
//       <div className="flex justify-center mt-4">
//         <button 
//           onClick={goToPrevious} 
//           className="mx-2 px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300"
//           disabled={currentIndex === 0}
//         >
//           Précédent
//         </button>
//         <button 
//           onClick={goToNext} 
//           className="mx-2 px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300"
//           disabled={currentIndex === maxIndex}
//         >
//           Suivant
//         </button>
//       </div>
//     </div>
//   );
// };

// export default EventBoard;


import React, { useState } from 'react';
import EventCard from './EventCard';

const EventBoard = ({ events }) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const itemsPerPage = 3;
  const maxIndex = Math.ceil(events.length / itemsPerPage) - 1;

  const goToNext = () => {
    setCurrentIndex((prevIndex) => (prevIndex < maxIndex ? prevIndex + 1 : prevIndex));
  };

  const goToPrevious = () => {
    setCurrentIndex((prevIndex) => (prevIndex > 0 ? prevIndex - 1 : prevIndex));
  };

  const startIndex = currentIndex * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const itemsToShow = events.slice(startIndex, endIndex);

  return (
    <div className="container mx-auto my-8 p-4 bg-gray-100 rounded-lg shadow-lg">
      <h2 className="text-3xl font-bold text-center text-gray-800 mb-8">Tableau d'affichage</h2>
      <div className="flex overflow-hidden">
        {itemsToShow.map((event) => (
          <div key={event.event_id} className="min-w-0 flex-1 px-2">
            <EventCard event={event} />
          </div>
        ))}
      </div>
      <div className="flex justify-center mt-4">
        <button 
          onClick={goToPrevious} 
          className="mx-2 px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300"
          disabled={currentIndex === 0}
        >
          Précédent
        </button>
        <button 
          onClick={goToNext} 
          className="mx-2 px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300"
          disabled={currentIndex === maxIndex}
        >
          Suivant
        </button>
      </div>
    </div>
  );
};

export default EventBoard;