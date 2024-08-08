import { MainController } from "../../src/contollers/mainController";
import UserService from "../../src/services/userServices";
import { IUser } from "../../src/models/DatabaseModels/userModel";

let server: MainController;
let userService: UserService;

beforeAll(() => {
  server = new MainController();
  userService = new UserService();
});

afterAll(async () => {
  await server.closeDatabaseConnection();
});

describe("UserService Tests - getUser method", () => {
  it("should return an array of users", async () => {
    const users: IUser[] = await userService.getUser();
    expect(users).toBeInstanceOf(Array);
  });
});

describe("UserService Tests - getUserByEmail method", () => {
  it("should return a user by email", async () => {
    const email = "francois.morin@umontreal.ca"; // existing user
    const user: IUser | null = await userService.getUserByEmail(email);
    if (user) {
      expect(user.email).toEqual(email);
    } else {
      expect(true).toBe(false); // User not found, test should fail
    }
  });

  it("should return null for non-existing user", async () => {
    const email = "nonexisting@example.com";
    const user: IUser | null = await userService.getUserByEmail(email);
    expect(user).toBeNull();
  });
});

describe("UserService Tests - getUserByMatricule method", () => {
  it("should return a user by matricule", async () => {
    const matricule = "20281527"; // existing user
    const user: IUser | null = await userService.getUserByMatricule(matricule);
    if (user) {
      expect(user.matricule).toEqual(matricule);
    } else {
      expect(true).toBe(false); // User not found, test should fail
    }
  });

  it("should return null for non-existing user", async () => {
    const matricule = "nonexistingmatricule";
    const user: IUser | null = await userService.getUserByMatricule(matricule);
    expect(user).toBeNull();
  });
});
