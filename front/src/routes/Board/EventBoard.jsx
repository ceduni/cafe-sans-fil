import EventCard from "./EventCard";

const EventBoard = ({ events }) => {
    return (
      <div className="container mx-auto my-8 p-4 bg-gray-100 rounded-lg shadow-lg">
        <h2 className="text-3xl font-bold text-center text-gray-800 mb-8">Tableau d'affichage</h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
          {events.map((event, index) => (
            <EventCard key={index} event={event} />
          ))}
        </div>
      </div>
    );
  };
  
  export default EventBoard;