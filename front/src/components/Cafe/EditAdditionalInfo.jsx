import moment from "moment-timezone";
import Input from "@/components/Input";
import { PlusIcon } from "@heroicons/react/24/solid";
import toast from "react-hot-toast";

const EditAdditionalInfo = ({ cafeData, setCafeData }) => {
  const handleAdditionalInfoChange = (e, index) => {
    let { name, value } = e.target;
    if (name === "start" || name === "end") {
      if (value === "") {
        value = null;
      }
    }
    const list = [...cafeData.additional_info];
    list[index][name] = value;
    setCafeData({ ...cafeData, additional_info: list });
  };

  const formatDatetimeForInput = (datetime) => {
    if (!datetime) return "";
    return moment(datetime).tz("America/Montreal").format("YYYY-MM-DDTHH:mm:ss");
  };

  const addAdditionalInfo = () => {
    if (cafeData.additional_info.length >= 3) {
      toast.error("N'abusons pas, 3 messages c'est déjà pas mal!");
      return;
    }
    setCafeData({
      ...cafeData,
      additional_info: [...cafeData.additional_info, { end: null, start: null, type: "", value: "" }],
    });
  };

  const removeAdditionalInfo = (index) => {
    const list = [...cafeData.additional_info];
    list.splice(index, 1);
    setCafeData({ ...cafeData, additional_info: list });
  };

  return (
    <div className="mt-6">
      {cafeData?.additional_info.map((info, index) => (
        <div key={index} className="py-6">
          <div className="flex justify-between">
            <p className="font-medium">Message {index + 1}</p>
            <button
              type="button"
              className="text-sm text-red-600 hover:text-red-500"
              onClick={() => removeAdditionalInfo(index)}>
              Supprimer
            </button>
          </div>
          {index === 0 && (
            <p className="text-sm text-gray-500">C'est ce message qui sera affiché sur la page d'accueil du site.</p>
          )}

          <div className="space-y-2 mt-6">
            <label htmlFor={`additional_info_${index}_type`} className="block text-sm font-medium text-gray-700">
              Titre
            </label>
            <Input
              id={`additional_info_${index}_type`}
              name="type"
              type="text"
              value={info.type}
              onChange={(e) => handleAdditionalInfoChange(e, index)}
              placeholder="Ex: Promotion, Nouveauté, etc."
            />
            {!info.type && <p className="text-sm text-red-500">Le type ne peut pas être vide.</p>}
          </div>

          <div className="space-y-2 mt-6">
            <label htmlFor={`additional_info_${index}_value`} className="block text-sm font-medium text-gray-700">
              Message
            </label>
            <Input
              id={`additional_info_${index}_value`}
              name="value"
              type="text"
              value={info.value}
              onChange={(e) => handleAdditionalInfoChange(e, index)}
            />
            {!info.value && <p className="text-sm text-red-500">Le message ne peut pas être vide.</p>}
          </div>

          <div className="space-y-2 mt-6">
            <label htmlFor={`additional_info_${index}_start`} className="block text-sm font-medium text-gray-700">
              Début de l'affichage
            </label>
            <Input
              id={`additional_info_${index}_start`}
              name="start"
              type="datetime-local"
              value={formatDatetimeForInput(info.start)}
              onChange={(e) => handleAdditionalInfoChange(e, index)}
            />
            <p className="text-sm text-gray-500">Laisser vide pour afficher immédiatement.</p>
          </div>

          <div className="space-y-2 mt-6">
            <label htmlFor={`additional_info_${index}_end`} className="block text-sm font-medium text-gray-700">
              Fin de l'affichage
            </label>
            <Input
              id={`additional_info_${index}_end`}
              name="end"
              type="datetime-local"
              value={formatDatetimeForInput(info.end)}
              onChange={(e) => handleAdditionalInfoChange(e, index)}
            />
            <p className="text-sm text-gray-500">Laisser vide pour afficher indéfiniment.</p>
          </div>
        </div>
      ))}
      <button
        type="button"
        className="mt-6 text-sm font-medium text-gray-700 hover:text-gray-500"
        onClick={addAdditionalInfo}>
        <PlusIcon className="w-5 h-5 inline-block mr-2 -mt-1" />
        Ajouter une info
      </button>
    </div>
  );
};

export default EditAdditionalInfo;
