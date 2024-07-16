import request from "supertest";
import { MainController } from "../contollers/mainController";
import UserService from "../services/userServices";

/*
get /cafes : doit retourner une liste vide ou une liste non vide 
get /cafes/:cafeName  : retourne un cafe sinon retourne  null et message (cafe not foound) 
get /cafes/:cafeName/volunteer : retourne la liste des volontaires ou une liste vides 
*/
let server: MainController;
let userService: UserService;

beforeAll(() => {
  server = new MainController();
  userService = new UserService();
});

afterAll(async () => {
  await server.closeDatabaseConnection();
});

describe("GET /api/v1/users", () => {
  it("should return a list of users", async () => {
    const response = await request(server.App).get("/api/v1/users");
    expect(response.status).toBe(200);
    expect(response.body).toHaveProperty("Users");
    expect(response.body.Users).toBeInstanceOf(Array);
  });
});

describe("GET /api/v1/users/email/:email", () => {
  it("should return a user by email", async () => {
    const email = "francois.morin@umontreal.ca"; // existing user
    const user = await userService.getUserByEmail(email);

    if (user) {
      const response = await request(server.App).get(
        `/api/v1/users/email/${email}`
      );
      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty("User");
      expect(response.body).toEqual(user.toJSON());
    } else {
      expect(true).toBe(false); // User not found, test should fail
    }
  });
});

describe("GET /api/v1/users/email/:email", () => {
  it("should return a null because email not found", async () => {
    const email = "notfound@example..com"; // non existing user
    const response = await request(server.App).get(
      `/api/v1/users/email/${email}`
    );
    expect(response.status).toBe(200);
    expect(response.body).toHaveProperty("User");
    expect(response.body.User).toEqual(null);
  });
});

describe("GET /api/v1/users/matricule/:matricule", () => {
  it("should return a user by matricule", async () => {
    const matricule = "20281527"; // existing user
    const user = await userService.getUserByMatricule(matricule);
    if (user) {
      const response = await request(server.App).get(
        `/api/v1/users/matricule/${matricule}`
      );
      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty("User");
      // à revoir expect(response.body).toEqual(user.toJSON());
    } else {
      expect(true).toBe(false); // User not found, test should fail
    }
  });
});

describe("GET /api/v1/users/matricule/:matricule", () => {
  it("should return a null because matricule not found", async () => {
    const matricule = "90000000"; // non existing user
    const response = await request(server.App).get(
      `/api/v1/users/matricule/${matricule}`
    );
    expect(response.status).toBe(200);
    expect(response.body).toHaveProperty("User");
    // à revoir expect(response.body.User).toEqual(null);
  });
});
