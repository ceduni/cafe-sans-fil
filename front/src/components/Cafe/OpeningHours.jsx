const OpeningHours = ({ openingHours = [] } = {}) => {
  // Ce composant prend un objet de type
  // [{ "day": "string", "blocks": [{"start": "string (HH:mm format)", "end": "string (HH:mm format)" }] }]
  // et le transforme en une liste d'éléments HTML avec chaque jour et ses horaires.

  return (
    <div className="mt-10">
      <h2 className="text-2xl font-bold tracking-tight text-gray-900">Horaires d'ouverture</h2>
      <div className="mt-6 gap-4 md:gap-6 grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
        {openingHours.map((day) => (
          <div key={day.day}>
            <h3 className="text-lg font-semibold text-gray-900 capitalize">{day.day}</h3>
            <ul className="mt-3 text-base text-gray-500">
              {day.blocks.length === 0 && <li>Fermé</li>}
              {day.blocks.map((block) => (
                <li key={block.start}>
                  {block.start}&nbsp;-&nbsp;{block.end}
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
};

export default OpeningHours;
