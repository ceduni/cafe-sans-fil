/*look at the file productModel.ts, productRoutes.ts, productService.ts, MainController.ts and t
ake them  as inspiration for generate for me all the test for productServices.test.ts */

import { MainController } from "../../src/contollers/mainController";
import CafeService from "../../src/services/cafeServices";
import { ICafe } from "../../src/models/DatabaseModels/cafeModel";
import { IUser } from "../../src/models/DatabaseModels/userModel";

let server: MainController;
let cafeService: CafeService;

beforeAll(() => {
  server = new MainController();
  cafeService = new CafeService();
});

afterAll(async () => {
  await server.closeDatabaseConnection();
});

describe("CafeService test", () => {
  describe("getCafe", () => {
    it("should return an array of cafes", async () => {
      const cafes: ICafe[] = await cafeService.getCafe();
      expect(cafes).toBeInstanceOf(Array);
    });
  });

  describe("getCafeByName", () => {
    it("should return a cafe by name", async () => {
      const cafeName = "CaféKine";
      const cafe: ICafe | null = await cafeService.getCafeByName(cafeName);
      expect(cafe).toBeInstanceOf(Object);
      if (cafe) {
        expect(cafe.name).toEqual(cafeName);
      }
    });

    it("should return null if cafe is not found", async () => {
      const cafeName = "NonExistentCafe";
      const cafe: ICafe | null = await cafeService.getCafeByName(cafeName);
      expect(cafe).toBeNull();
    });
  });

  describe("getCafesVonlunteer", () => {
    it("should return a list of volunteers by cafe name", async () => {
      const cafeName = "CaféKine";
      const volunteers: IUser[] = await cafeService.getCafesVonlunteer(
        cafeName
      );
      expect(volunteers).toBeInstanceOf(Array);
    });
  });

  describe("addVolunteerToCafeBy", () => {
    it("should add a volunteer to a cafe", async () => {
      const cafeName = "CaféKine";
      const matricule = "123456";
      await cafeService.addVolunteerToCafeBy(cafeName, matricule);
      // Add assertions to check that the volunteer was added to the cafe
    });
  });
});
