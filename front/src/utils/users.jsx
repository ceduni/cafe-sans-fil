import authenticatedRequest from "@/helpers/authenticatedRequest";
import toast from "react-hot-toast";

const getCurrentUser = async () => {
    try {
      const response = await authenticatedRequest.post("/auth/test-token");
      return response.data;
    } catch (error) {
      toast.error(error.message);
      return null;
    }
  };

  export default getCurrentUser