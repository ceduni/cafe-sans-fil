const EventCard = ({ event }) => {
    return (
      <div className="bg-white rounded-lg overflow-hidden shadow-lg transition duration-500 ease-in-out transform hover:-translate-y-1 hover:scale-105">
        <img className="w-full object-cover h-48" src={event.image} alt={event.title} />
        <div className="p-4">
          <h3 className="font-bold text-xl mb-2">{event.title}</h3>
          <p className="text-gray-700 text-base">{event.description}</p>
        </div>
        <div className="px-4 pt-4 pb-2">
          <span className="inline-block bg-blue-100 text-blue-800 rounded-full px-3 py-1 text-sm font-semibold mr-2 mb-2">{event.date}</span>
          <span className="inline-block bg-blue-100 text-blue-800 rounded-full px-3 py-1 text-sm font-semibold mb-2">{event.time}</span>
        </div>
        <div className="px-4 pb-4 flex justify-between">
          <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
            Je viens!
          </button>
          <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
            Je supporte!
          </button>
        </div>
      </div>
    );
  };
  
  export default EventCard;
  