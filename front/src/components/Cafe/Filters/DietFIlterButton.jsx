import React from 'react';
import Switch from "@/components/CustomSwitch";

const DietFilterButton = ({ name, icon, label, active, activeDiets, setActiveDiets }) => {
  return (
    <div className="flex flex-col items-center justify-center space-y-1 mr-2">
      <div
        className={`relative flex items-center px-4 py-2 rounded-lg cursor-pointer 
                    ${active ? 'bg-emerald-500 text-white' : 'bg-gray-200 text-gray-700'}
                    transition-colors duration-200 ease-in-out`}
        onClick={() => setActiveDiets({ ...activeDiets, [name]: !active })}
      >
        {/* <Switch
          checked={active}
          onChange={(e) => setActiveDiets({ ...activeDiets, [name]: e })}
          className="absolute inset-0 opacity-0 w-full h-full"
        /> */}
        <div className="flex items-center space-x-2">
          <span className="text-sm font-medium">{label}</span>
        </div>
      </div>
    </div>
  );
};

export default DietFilterButton;
