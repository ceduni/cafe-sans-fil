import Container from "./Container";

const Footer = () => {
  return (
    <footer className="bg-white border-t border-gray-200">
      <div className="w-full max-w-screen-xl mx-auto p-5 md:py-8">
        <div className="flex items-center mb-4 sm:justify-center">
          <img src="/logo.png" class="h-24" alt="Logo de café sans-fil" />
        </div>
        <div class="block text-sm text-gray-500 sm:text-center">
          <p className="font-semibold">Café sans-fil</p>
          <p className="mb-3 italic">(Preview, version 0.1.0)</p>
          <p>
            Ceduni &bull; Projet disponible sur{" "}
            <a className="underline" href="https://github.com/ceduni/udem-cafe" target="_blank">
              GitHub
            </a>
          </p>
          <p>Développé par: Axel ZAREB et Southidej OUDANONH</p>
          <p className="mt-3">&copy; 2023, Café sans-fil</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
