import { Outlet } from "react-router-dom";
import Navbar from "@/components/Navbar";
import ScrollToTop from "@/helpers/ScrollToTop";
import { AuthProvider } from "@/hooks/useAuth";
import { Toaster } from "react-hot-toast";
import Footer from "@/components/Footer";

const PageWrapper = () => {
  return (
    <AuthProvider>
      <ScrollToTop />
      <Navbar />
      <div id="content">
        <Outlet />
      </div>
      <Footer />
      <Toaster position="bottom-right" />
    </AuthProvider>
  );
};

export default PageWrapper;
