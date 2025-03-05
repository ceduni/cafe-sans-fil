import { useEffect } from "react";

// Custom hook to update the document title
const useTitle = (title) => {
  useEffect(() => {
    document.title = title;
  }, [title]); // Update the title whenever the `title` prop changes
};

export default useTitle;
