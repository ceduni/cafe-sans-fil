import useApi from "../hooks/useApi";
import Card from "../components/ui/Card";
import toast from "react-hot-toast";
import { useEffect } from "react";
import EmptyState from "./ui/EmptyState";

const CafeList = () => {
  const { data: cafeList, isLoading, error } = useApi("/cafes");

  useEffect(() => {
    if (error) {
      toast.error(`${error.status ? `${error.status} - ` : ""} ${error.statusText || error.message}`, {
        style: {
          padding: "16px",
        },
      });
      console.error(error);
    }
  }, [error]);

  if (isLoading) {
    return (
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 py-6 animate-pulse duration-100">
        {Array.from({ length: 8 }).map((_, i) => (
          <Card key={i}>
            <Card.Header>
              <Card.Header.Title as="div">
                <div className="h-3 bg-gray-200 rounded-full w-36 mb-4"></div>
              </Card.Header.Title>
              <Card.Header.Subtitle as="div">
                <div className="h-2.5 bg-gray-200 rounded-full w-48 mb-4"></div>
              </Card.Header.Subtitle>
            </Card.Header>
            <Card.Body>
              <div className="h-2 bg-gray-200 rounded-full mb-2.5"></div>
              <div className="h-2 bg-gray-200 rounded-full mb-2.5 w-3/4"></div>
              <div className="h-2 bg-gray-200 rounded-full mb-2.5"></div>
              <div className="h-2 bg-gray-200 rounded-full mb-2.5 w-3/4"></div>
              <div className="h-2 bg-gray-200 rounded-full"></div>
            </Card.Body>
          </Card>
        ))}
      </div>
    );
  }

  if (error || cafeList?.length === 0) {
    return <EmptyState itemName="café" />;
  }

  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 py-6">
      {cafeList.map((cafe) => (
        <Card key={cafe.name} link={`/cafes/${cafe.cafe_id}`}>
          <Card.Header>
            <Card.Header.Title>{cafe.name}</Card.Header.Title>
            <Card.Header.Subtitle>{cafe.location}</Card.Header.Subtitle>
          </Card.Header>
          <Card.Body>{cafe.description}</Card.Body>
        </Card>
      ))}
    </div>
  );
};

export default CafeList;
