import Avatar from "@/components/Avatar";
import Container from "@/components/Container";

const people = [
  {
    name: "Leslie Alexander",
    email: "leslie.alexander@umontreal.ca",
    role: "Administrateur",
  },
  {
    name: "Michael Foster",
    email: "michael.foster@umontreal.ca",
    role: "Administrateur",
  },
  {
    name: "Dries Vincent",
    email: "dries.vincent@umontreal.ca",
    role: "Bénévole",
  },
  {
    name: "Lindsay Walton",
    email: "lindsay.walton@umontreal.ca",
    role: "Bénévole",
  },
  {
    name: "Courtney Henry",
    email: "courtney.henry@umontreal.ca",
    role: "Bénévole",
  },
  {
    name: "Tom Cook",
    email: "tom.cook@umontreal.ca",
    role: "Bénévole",
  },
];

const StaffList = () => {
  return (
    <Container className="py-10">
      <ul role="list" className="divide-y divide-gray-100">
        {people.map((person) => (
          <li key={person.email} className="flex justify-between gap-x-6 py-5">
            <div className="flex min-w-0 gap-x-4">
              <Avatar name={person.name} />
              <div className="min-w-0 flex-auto">
                <p className="text-sm font-semibold leading-6 text-gray-900">{person.name}</p>
                <p className="mt-1 truncate text-xs leading-5 text-gray-500">{person.email}</p>
              </div>
            </div>
            <div className="hidden shrink-0 sm:flex sm:flex-col sm:items-end">
              <p className="text-sm leading-6 text-gray-900">{person.role}</p>
            </div>
          </li>
        ))}
      </ul>
    </Container>
  );
};

export default StaffList;
