const CafeDescriptionBoard = ({ cafe }) => {
    return (
      <div className="bg-white shadow rounded-lg p-4 mb-4">
        <div className="mb-2">
          <h3 className="text-lg font-bold text-gray-900">{cafe.name}</h3>
          <p className="text-sm text-gray-600">{cafe.description}</p>
        </div>
        <div className="mb-2">
          <strong>Appareils:</strong>
          <ul className="list-disc list-inside text-sm">
            {cafe.appareils.map((appareil, index) => (
              <li key={index}>{appareil}</li>
            ))}
          </ul>
        </div>
        <div className="flex justify-between items-center">
          <div>
            <strong>Staff:</strong>
            {cafe.staff.map((member, index) => (
              <div key={index} className="inline-block mr-2">
                <span className="text-sm">{member.name}</span>
              </div>
            ))}
          </div>
          <button className="text-sm text-blue-600 border border-blue-600 rounded py-1 px-3 hover:bg-blue-600 hover:text-white transition-colors duration-300">
            Devenir bénévole
          </button>
        </div>
      </div>
    );
  };
  
  export default CafeDescriptionBoard;