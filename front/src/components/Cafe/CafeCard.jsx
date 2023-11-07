import { Link } from "react-router-dom";
import OpenIndicator from "@/components/Cafe/OpenIndicator";
import Card from "@/components/Card";

const CafeCard = ({ cafe }) => {
  return (
    <Link to={`/cafes/${cafe.cafe_id}`} className="contents" onKeyDown={(e) => e.key === "Enter" && e.target.click()}>
      <Card>
        <Card.Header>
          <Card.Header.Title>{cafe.name}</Card.Header.Title>
          <Card.Header.Subtitle>{cafe.location}</Card.Header.Subtitle>
          <OpenIndicator isOpen={cafe.is_open} size="xs" />
        </Card.Header>
        <Card.Body>{cafe.description}</Card.Body>
      </Card>
    </Link>
  );
};

const CafeCardLoading = () => {
  return (
    <Card>
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
  );
};

export { CafeCard, CafeCardLoading };
