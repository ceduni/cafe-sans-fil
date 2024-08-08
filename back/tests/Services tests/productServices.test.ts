import { MainController } from "../../src/contollers/mainController";
import { ProductService } from "../../src/services/productService";
import { IStock } from "../../src/models/StockModel";
import { Ordes } from "../../src/models/OrdeModel";

let server: MainController;
let productService: ProductService;

beforeAll(() => {
  server = new MainController();
  productService = new ProductService();
});

afterAll(async () => {
  await server.closeDatabaseConnection();
});

describe("ProductService test", () => {
  describe("getSales", () => {
    it("should fetch sales data from the database based on product name", async () => {
      //Arrange
      const productName = "ExampleProduct";

      //Act
      const salesData: (typeof Ordes)[] = await productService.getSales(
        "exampleCollection"
        // productName
      );

      //Assert
      expect(salesData).toBeDefined();
      //Add more specific assertions based on the expected data
    });
  });

  describe("getStock", () => {
    it("should fetch stock data from the database", async () => {
      // Act
      const stockData: IStock[] = await productService.getStock();

      // Assert
      expect(stockData).toBeDefined();
      // Add more specific assertions based on the expected data
    });
  });
});
