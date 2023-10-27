import useApi from "../hooks/useApi";
import Card from "../components/ui/Card";
import EmptyState from "./ui/EmptyState";
import OpenIndicator from "./ui/OpenIndicator";

const CafeList = () => {
  const { data: cafeList, isLoading, error } = useApi("/cafes");

  if (error) {
    return <EmptyState type="error" error={error} />;
  }

  if (cafeList?.length === 0) {
    return <EmptyState name="café" />;
  }

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

  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 py-6">
      {cafeList.map((cafe) => (
        <Card key={cafe.name} link={`/cafes/${cafe.cafe_id}`}>
          <Card.Header>
            <Card.Header.Title>{cafe.name}</Card.Header.Title>
            <Card.Header.Subtitle>{cafe.location}</Card.Header.Subtitle>
            <OpenIndicator isOpen={cafe.is_open} size="xs" />
          </Card.Header>
          <Card.Body>{cafe.description}</Card.Body>
        </Card>
      ))}
    </div>
  );
};

export default CafeList;
