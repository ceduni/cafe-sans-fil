import { useAuth } from "@/hooks/useAuth";
import { isMember } from "@/utils/admin";
import EmptyState from "@/components/Error/EmptyState";
import ErrorState from "@/components/Error/ErrorState";

const MemberOnly = ({ children, cafe, error }) => {
  const { user } = useAuth();

  if (error) {
    if (error.status === 404) {
      throw new Response("Not found", { status: 404, statusText: "Ce café n'existe pas" });
    }
    return <EmptyState type="error" error={error} />;
  }

  if (cafe && !isMember(cafe, user?.username)) {
    return (
      <ErrorState
        title="Accès refusé"
        message="Vous n'avez pas accès à cette page"
        linkText={`Retour à ${cafe.name}`}
        linkTo={`/cafes/${cafe.slug}`}
      />
    );
  }

  return children;
};

export default MemberOnly;
