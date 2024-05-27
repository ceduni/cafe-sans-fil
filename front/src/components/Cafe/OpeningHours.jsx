const OpeningHours = ({ openingHours = [] }) => {
  return (
    <div className="bg-black bg-opacity-60 p-4 rounded-lg text-white max-w-xs">
      <ul>
        {openingHours.map((day) => (
          <li key={day.day} className=" py-1">
            <span className="font-bold text-lg">{day.day}</span>
            <span className="text-sm">
              {day.blocks.map((block, index) => (
                <span key={index} className="ml-2">
                  {block.start} - {block.end}
                </span>
              ))}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default OpeningHours;
