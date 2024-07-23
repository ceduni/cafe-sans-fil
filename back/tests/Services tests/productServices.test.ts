// import { MainController } from "../../contollers/mainController";
// import { ProductService } from "../../services/productService";
// import { OrdersModel } from "../../src/models/OrdersModel";
// import { IStock } from "../../src/models/StockModel";

// let server: MainController;
// let productService: ProductService;

// beforeAll(() => {
//   server = new MainController();
//   productService = new ProductService();
// });

// afterAll(async () => {
//   await server.closeDatabaseConnection();
// });

// describe("ProductService test", () => {
//   describe("getSales", () => {
//     it("should fetch sales data from the database based on product name", async () => {
//       // Arrange
//       const productName = "ExampleProduct";

//       // Act
//       const salesData: OrdersModel[] = await productService.getSales(
//         "exampleCollection",
//         productName
//       );

//       // Assert
//       expect(salesData).toBeDefined();
//       // Add more specific assertions based on the expected data
//     });
//   });

//   describe("getStock", () => {
//     it("should fetch stock data from the database", async () => {
//       // Act
//       const stockData: IStock[] = await productService.getStock();

//       // Assert
//       expect(stockData).toBeDefined();
//       // Add more specific assertions based on the expected data
//     });
//   });
// });
