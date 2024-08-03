import 'dart:convert';
import 'package:app/config.dart';
import 'package:http/http.dart' as http;
import '../modeles/Order models/Order.dart';

class ProductService {
  final String baseUrl = "${Config.baseUrl}/orders";

  ProductService({dynamic});

  Future<List<Order>> fetchOrders() async {
    var url = Uri.parse(baseUrl);
    var response = await http.get(url);

    if (response.statusCode == 200) {
      var jsonData = json.decode(response.body);

      if (jsonData['Sales'] != null) {
        print("in json sales tab");
        List<dynamic> salesJson = jsonData['Sales'];
        List<Order> orders =
            salesJson.map((json) => Order.fromJson(json)).toList();
        return orders;
      } else {
        throw Exception('Sales data is not available');
      }
    } else {
      throw Exception('Failed to load sales from $baseUrl');
    }
  }
}

/*
void main() async {
  var productService = new ProductService();

  List<Order> orders = await productService.fetchOrders();
  print(orders);
  double turnOver = Order.turnOver(orders);
  print(turnOver);
  int len = Order.numOfOrder(orders);
}
*/