import { Outlet } from "react-router-dom";
import Navbar from "./Navbar";
import ScrollToTop from "../helpers/ScrollToTop";
import { AuthProvider } from "../hooks/useAuth";

const PageWrapper = () => {
  return (
    <AuthProvider>
      <ScrollToTop />
      <Navbar />
      <div id="content">
        <Outlet />
      </div>
    </AuthProvider>
  );
};

export default PageWrapper;
