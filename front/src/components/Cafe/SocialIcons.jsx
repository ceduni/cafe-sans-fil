import { getPlatformIcon } from "@/utils/socials";

const SocialIcons = ({ socialMedia }) => {
  return (
    <div className="flex items-center gap-x-4 py-3 ">
      {socialMedia?.map((s, index) => (
        <a href={s.link} key={index} target="_blank" rel="noreferrer" className="opacity-90 hover:opacity-100 ml-5 bg-white rounded-sm">
          {getPlatformIcon(s)}
        </a>
      ))}
    </div>
  );
};

export default SocialIcons;
