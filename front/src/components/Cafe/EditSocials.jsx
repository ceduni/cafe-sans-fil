import { getPlatformIcon, getPlatformName, supportedPlatforms, DEFAULT_PLATFORM } from "@/utils/socials";
import Input from "@/components/Widgets/Input";
import { PlusIcon } from "@heroicons/react/24/solid";

const EditSocials = ({ cafeData, setCafeData }) => {
  const handleSocialChange = (index, link) => {
    const newCafeData = { ...cafeData };
    if (newCafeData.social_media[index].platform_name === DEFAULT_PLATFORM) {
      newCafeData.social_media[index].platform_name = getPlatformName(link);
    }
    newCafeData.social_media[index].link = link;
    setCafeData(newCafeData);
  };

  const addSocial = (platform) => {
    const newCafeData = { ...cafeData };
    newCafeData.social_media.push({ platform_name: platform, link: null });
    setCafeData(newCafeData);
  };

  const removeSocial = (index) => {
    const newCafeData = { ...cafeData };
    newCafeData.social_media.splice(index, 1);
    setCafeData(newCafeData);
  };

  const cafeSocials = cafeData?.social_media;

  const supportedPlatformsNotInCafeSocials = supportedPlatforms.filter(
    (platform) => !cafeSocials?.some((social) => getPlatformName(social) === platform)
  );

  const isDuplicatePair = (social) => {
    const platformName = getPlatformName(social);
    const link = social.link;
    return cafeSocials?.some(
      (s) =>
        getPlatformName(s) === platformName && s.link === link && cafeSocials.indexOf(s) !== cafeSocials.indexOf(social)
    );
  };

  return (
    <div className="mt-6">
      {cafeSocials?.map((social, index) => (
        <div className="space-y-3 mt-6" key={social.platform_name + index}>
          <div className="flex justify-between">
            <div className="flex items-center gap-4">
              <span className="opacity-80">{getPlatformIcon(social)}</span>
              <label className="block text-sm font-medium text-gray-700" htmlFor={social.platform_name}>
                {getPlatformName(social)}
              </label>
            </div>
            <button
              type="button"
              className="text-sm text-red-600 hover:text-red-500"
              onClick={() => removeSocial(index)}>
              Supprimer
            </button>
          </div>
          <Input
            id={social.platform_name}
            type="url"
            value={social.link || ""}
            onChange={(e) => handleSocialChange(index, e.target.value)}
            required
          />
          {isDuplicatePair(social) && <p className="text-sm text-red-600">Ces liens sont en double.</p>}
        </div>
      ))}

      {supportedPlatformsNotInCafeSocials?.map((platform) => (
        <div className="space-y-3 mt-6" key={platform}>
          <div className="flex items-center gap-4">
            <span className="opacity-80">{getPlatformIcon({ platform_name: platform })}</span>
            <p className="text-sm font-medium text-gray-700">{platform}</p>
          </div>
          <button
            type="button"
            className="mt-6 text-sm text-gray-500 hover:text-gray-500"
            onClick={() => addSocial(platform)}>
            <PlusIcon className="w-5 h-5 inline-block mr-2 -mt-1" />
            Ajouter un lien {platform}
          </button>
        </div>
      ))}

      <div className="space-y-3 mt-6">
        <div className="flex items-center gap-4">
          <span className="opacity-80">{getPlatformIcon({ platform_name: DEFAULT_PLATFORM })}</span>
          <p className="text-sm font-medium text-gray-700">Autre</p>
        </div>
        <button
          type="button"
          className="mt-6 text-sm text-gray-500 hover:text-gray-500"
          onClick={() => addSocial(DEFAULT_PLATFORM)}>
          <PlusIcon className="w-5 h-5 inline-block mr-2 -mt-1" />
          Ajouter un lien autre
        </button>
      </div>
    </div>
  );
};

export default EditSocials;
