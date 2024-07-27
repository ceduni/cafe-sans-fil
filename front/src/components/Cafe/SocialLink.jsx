import LogoInstagram from "@/assets/icons/logo-instagram.svg";
import LogoFacebook from "@/assets/icons/logo-facebook.svg";
import LogoX from "@/assets/icons/logo-x.svg";

const Logo = {
  facebook: LogoFacebook,
  instagram: LogoInstagram,
  x: LogoX
};

const SocialLink = ({ platform, url, container: Container = 'li' }) => {
  return (
    <Container className="social">
      <a className="social-link" href={url} target="_blank" rel="noopener noreferrer">
        <img className="social-img" src={Logo[platform]} alt={`${platform} logo`} />
      </a>
    </Container>
  );
};

export default SocialLink;
