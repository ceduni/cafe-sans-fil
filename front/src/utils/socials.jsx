import { LinkIcon } from "@heroicons/react/24/solid";
import Instagram from "@/assets/icons/logo-instagram.svg";
import Facebook from "@/assets/icons/logo-facebook.svg";
import X from "@/assets/icons/logo-x.svg";

export const iconClassNames = "h-6 w-6 object-contain";

export const getPlatformIcon = (social) => {
  switch (social.platform_name) {
    case "Facebook":
      return <img src={Facebook} alt="Facebook logo" className={iconClassNames} />;
    case "Instagram":
      return <img src={Instagram} alt="Instagram logo" className={iconClassNames} />;
    case "Twitter":
    case "X":
      return <img src={X} alt="X (Twitter) logo" className={iconClassNames} />;
    default:
      return <LinkIcon className={iconClassNames} />;
  }
};

export const getPlatformName = (social) => {
  const platformName = social.platform_name;
  if (!platformName) {
    const url = new URL(social.link);
    return url.hostname;
  }
  if (platformName === "Twitter" || platformName === "X") {
    return "X (Twitter)";
  }
  return platformName;
};
