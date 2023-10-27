import { Outlet } from "react-router-dom";
import Navbar from "./Navbar";
import ScrollToTop from "../helpers/ScrollToTop";
import { AuthProvider } from "../hooks/useAuth";
import { Toaster } from "react-hot-toast";

const PageWrapper = () => {
  return (
    <AuthProvider>
      <ScrollToTop />
      <Navbar />
      <div id="content">
        <Outlet />
      </div>
      <Toaster position="bottom-right" />
    </AuthProvider>
  );
};

export default PageWrapper;
