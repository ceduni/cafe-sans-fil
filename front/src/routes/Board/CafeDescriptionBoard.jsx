import { EnvelopeIcon } from "@heroicons/react/24/outline";

const CafeDescriptionBoard = ({ cafe }) => {
  

  const handleEmailClick = () => {
    // Remplacez 'yourcafe@example.com' par l'adresse e-mail que vous souhaitez utiliser
    const mailto = `mailto:yourcafe@example.com`;
    window.location.href = mailto;
  };
  
  const additionalVolunteers = cafe.volunteers - cafe.staff.length;
  
  return (
    <div className="bg-white shadow rounded-lg p-4 mb-4">
      <div className="mb-4">
        <h2 className="text-xl font-bold text-gray-900">{cafe.name}</h2>
        <p className="text-xs text-gray-600">{cafe.location}</p>
        <p className="text-sm text-gray-600 pt-2">{cafe.description}</p>
        
      </div>
      <div className="mb-4">
        <strong>Appareils:</strong>
        <ul className="list-disc list-inside text-sm">
          {cafe.appareils.map((appareil, index) => (
            <li key={index}>{appareil}</li>
          ))}
        </ul>
      </div>
      <div>
      <div className="flex  items-center mb-4">
        <strong>Staff</strong>
        <button
          onClick={handleEmailClick}className=" hover:text-blue-800" >
          <EnvelopeIcon className="h-5 w-5 ml-2" aria-hidden="true" />

        </button>
      </div>
      <div className="flex flex-wrap items-center">
  {cafe.staff.slice(0, 2).map((member, index) => (
    <div key={index} className="flex items-center mr-4 mb-4">
      {member.image ? (
        <img
          src={member.image}
          alt={member.name}
          className="h-10 w-10 rounded-full mr-2"
        />
      ) : (
        <div className="h-10 w-10 rounded-full bg-gray-200 mr-2"></div>
      )}
      <span className="text-sm mr-2">{member.name}</span>
    </div>
  ))}
</div>
      </div>
      <div className="text-right mt-4">
        <button className="text-sm text-blue-600 border border-blue-600 rounded py-1 px-3 hover:bg-blue-600 hover:text-white transition-colors duration-300">
          Devenir bénévole
        </button>
      </div>
    </div>
  );
};

export default CafeDescriptionBoard;
