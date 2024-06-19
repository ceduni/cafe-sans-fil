import Container from "@/components/Container";
import { Link } from "react-router-dom";

const ErrorState = ({ title, message, linkText, linkTo }) => {
  return (
    <Container className="h-[70vh] flex flex-col justify-center">
      <div className="mx-auto max-w-screen-sm text-center">
        <p className="mb-4 text-3xl tracking-tight font-bold text-gray-900 md:text-4xl">{title}</p>
        <p className="mb-4 text-lg font-light text-gray-500">{message}</p>
        <Link
          to={linkTo}
          className="inline-flex text-white bg-emerald-600 hover:bg-emerald-800 focus:ring-4 focus:outline-none focus:ring-emerald-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center my-4">
          {linkText}
        </Link>
      </div>
    </Container>
  );
};

export default ErrorState;
