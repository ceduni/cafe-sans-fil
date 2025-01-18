import Input from "@/components/Widgets/Input";
import { PlusIcon, TrashIcon } from "@heroicons/react/24/solid";
import { useEffect, useState } from "react";

const EditOpeningHours = ({ cafeData, setCafeData }) => {
  const weekdays = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"];
  const remainingWeekdays = weekdays.filter((day) => !cafeData?.opening_hours.some((hours) => hours.day === day));

  const [selectedDayToAdd, setSelectedDayToAdd] = useState(remainingWeekdays[0]);
  useEffect(() => {
    setSelectedDayToAdd(remainingWeekdays[0]);
  }, [cafeData]);

  const addWeekday = () => {
    setCafeData({
      ...cafeData,
      opening_hours: [
        ...cafeData.opening_hours,
        {
          day: selectedDayToAdd,
          blocks: [{ start: "08:00", end: "18:00" }],
        },
      ],
    });
  };
  const removeWeekday = (index) => {
    const list = [...cafeData.opening_hours];
    list.splice(index, 1);
    setCafeData({ ...cafeData, opening_hours: list });
  };

  const handleChange = (e, index, blockIndex) => {
    const list = [...cafeData.opening_hours];
    list[index].blocks[blockIndex][e.target.name] = e.target.value;
    setCafeData({ ...cafeData, opening_hours: list });
  };

  const addBlock = (index) => {
    const list = [...cafeData.opening_hours];
    list[index].blocks.push({ start: "08:00", end: "18:00" });
    setCafeData({ ...cafeData, opening_hours: list });
  };
  const removeBlock = (index, blockIndex) => {
    const list = [...cafeData.opening_hours];
    list[index].blocks.splice(blockIndex, 1);
    setCafeData({ ...cafeData, opening_hours: list });
  };

  const isOverlapping = (day) => {
    const blocks = day.blocks;
    for (let i = 0; i < blocks.length; i++) {
      const block = blocks[i];
      for (let j = i + 1; j < blocks.length; j++) {
        const otherBlock = blocks[j];
        if (block.start < otherBlock.end && block.end > otherBlock.start) {
          return true;
        }
      }
    }
    return false;
  };

  return (
    <div className="mt-12">
      <h2 className="text-base font-semibold leading-7 text-gray-900">Horaires d'ouverture</h2>
      <p className="mt-1 text-sm leading-6 text-gray-600">
        Indiquez les horaires d'ouverture de votre café. N'ajoutez pas les jours où vous êtes fermés.
      </p>
      {cafeData?.opening_hours.map((hours, index) => (
        <div key={index} className="py-6">
          <div className="flex justify-between">
            <p className="font-medium">{hours.day}</p>
            <button
              type="button"
              className="text-sm text-red-600 hover:text-red-500 \
                focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
              onClick={() => removeWeekday(index)}>
              Supprimer
            </button>
          </div>

          {hours.blocks.map((block, blockIndex) => (
            <div key={blockIndex} className="space-y-2 mt-6">
              <div className="w-full flex justify-between items-end gap-6">
                <div className="grid grid-cols-2 gap-6 flex-grow">
                  <div className="space-y-2">
                    <label htmlFor={`opening_hours_${index}_start`} className="block text-sm font-medium text-gray-700">
                      Début intervalle {blockIndex + 1}
                    </label>
                    <Input
                      id={`opening_hours_${index}_start`}
                      name="start"
                      type="time"
                      value={block.start}
                      onChange={(e) => handleChange(e, index, blockIndex)}
                      required
                    />
                  </div>
                  <div className="space-y-2">
                    <label htmlFor={`opening_hours_${index}_end`} className="block text-sm font-medium text-gray-700">
                      Fin intervalle {blockIndex + 1}
                    </label>
                    <Input
                      id={`opening_hours_${index}_end`}
                      name="end"
                      type="time"
                      value={block.end}
                      onChange={(e) => handleChange(e, index, blockIndex)}
                      required
                    />
                  </div>
                </div>
                <button
                  type="button"
                  className="text-red-500 p-2 rounded-md hover:bg-gray-200 \
                  focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 \
                  disabled:opacity-50 disabled:cursor-not-allowed"
                  disabled={hours.blocks.length === 1}
                  onClick={() => removeBlock(index, blockIndex)}>
                  <TrashIcon className="w-5 h-5" />
                </button>
              </div>
            </div>
          ))}
          <p className="text-sm text-red-500 mt-4">{isOverlapping(hours) && "Les intervalles se chevauchent."}</p>
          <button
            type="button"
            className="mt-6 text-sm font-medium text-gray-700 hover:text-gray-500"
            onClick={() => addBlock(index)}>
            <PlusIcon className="w-5 h-5 inline-block mr-2 -mt-1" />
            Ajouter une intervalle
          </button>
        </div>
      ))}
      {remainingWeekdays.length > 0 && (
        <div className="mt-6 flex items-center gap-6">
          <select
            id="opening_hours_day"
            name="day"
            className="text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
            value={selectedDayToAdd}
            onChange={(e) => setSelectedDayToAdd(e.target.value)}>
            {remainingWeekdays.map((day) => (
              <option key={day}>{day}</option>
            ))}
          </select>
          <button type="button" className="text-sm font-medium text-gray-700 hover:text-gray-500" onClick={addWeekday}>
            <PlusIcon className="w-5 h-5 inline-block mr-2 -mt-1" />
            Ajouter {selectedDayToAdd}
          </button>
        </div>
      )}
    </div>
  );
};

export default EditOpeningHours;
