import 'dart:convert';
import 'package:app/config.dart';
import 'package:app/modeles/Order%20models/Order.dart';
import 'package:app/modeles/Order%20models/OrderItem.dart';
import 'package:http/http.dart' as http;

class OrderService {
  final String baseUrl = "${Config.baseUrl}/orders";

  Future<List<Order>> fetchOrders() async {
    var url = Uri.parse(baseUrl);
    var response = await http.get(url).timeout(const Duration(seconds: 25));

    if (response.statusCode == 200) {
      var jsonData = json.decode(response.body);

      if (jsonData['Sales'] != null) {
        print("Order Service : json fetching");
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

  double calculateTurnOverForACafe(List<Order> orders, String cafeSlug) {
    bool isFall = isFallSemester();
    bool isWinter = isWinterSemester();

    List<Order> filteredOrders = [];
    double turnOver = 0.0;

    if (isFall) {
      filteredOrders = getOrderInFallSemester(orders);
    } else if (isWinter) {
      filteredOrders = getOrderInWinterSemester(orders);
    }

    for (Order order in filteredOrders) {
      if (order.cafeSlug == cafeSlug) {
        turnOver += order.totalPrice;
      }
    }

    return double.parse(turnOver.toStringAsFixed(4));
  }

  double calculateTurnOverForACafeForAYear(
      List<Order> orders, int year, String cafeName) {
    List<Order> filteredOrders = getOrderByCafeName(orders, cafeName);
    filteredOrders =
        getOrderOverAPeriod(filteredOrders, DateTime(year), DateTime(year + 1));

    double turnOver = 0.0;
    for (Order order in filteredOrders) {
      turnOver += order.totalPrice;
    }

    return double.parse(turnOver.toStringAsFixed(4));
  }

  double calculateProfit(double turnOver) {
    return turnOver - 500;
  }

  List<List<double>> getTurnOverAndProfitForAYear(
      List<Order> orders, int year, String cafeName) {
    List<Order> filteredOrders = getOrderByCafeName(orders, cafeName);

    List<List<double>> turnOverAndProfitList = [];

    for (List<DateTime> dateList in getStartAndEndDatesOfMonths(year)) {
      List<Order> monthOrders =
          getOrderOverAPeriod(filteredOrders, dateList[0], dateList[1]);
      double turnOver = 0.0;
      for (Order order in monthOrders) {
        turnOver += order.totalPrice;
      }
      double profit = turnOver * 0.9;

      turnOverAndProfitList.add([turnOver, profit]);
    }

    print(turnOverAndProfitList);

    return turnOverAndProfitList;
  }

  Map<String, double> getTurnOverByCategoryForACafe(
      List<Order> orders, int year, String cafeName) {
    List<Order> filteredOrders = getOrderByCafeName(orders, cafeName);
    filteredOrders = getOrderOverAPeriod(
        filteredOrders, DateTime(year, 1, 1), DateTime(year, 12, 31));

    Map<String, String> categoriser = {
      "Latte ou Cappuccino": "Boissons Chaudes",
      "Chocolat chaud": "Boissons Chaudes",
      "Espresso Double": "Boissons Chaudes",
      "Espresso": "Boissons Chaudes",
      "Thé": "Boissons Chaudes",
      "Café régulier": "Boissons Chaudes",
      "Barre de chocolat": "Snacks",
      "Barre Spécial K": "Snacks",
      "Gomme": "Snacks",
      "Barre Kirkland": "Snacks",
      "Brookside": "Snacks",
      "Barre Val Nature": "Snacks",
      "LE BRIE": "Vins",
      "LE MOZZA": "Vins",
      "LE BLANC": "Vins",
      "LE MARBRÉ": "Vins",
      "Coca-Cola": "Boissons Froides",
      "Perrier": "Boissons Froides",
      "Jus V8": "Boissons Froides",
      "Arizona": "Autres"
    };

    Map<String, double> turnOverByCategory = {};

    for (Order order in filteredOrders) {
      for (OrderItem item in order.items) {
        String? category = categoriser[item.itemName];

        if (category != null) {
          if (turnOverByCategory.containsKey(category)) {
            turnOverByCategory[category] =
                turnOverByCategory[category]! + item.itemPrice * item.quantity;
          } else {
            turnOverByCategory[category] = item.itemPrice * item.quantity;
          }
        }
      }
    }

    return turnOverByCategory;
  }

  List<List<double>> getTurnOverAndProfitForAMonth(
      List<Order> orders, int year, int month, String cafeName) {
    List<Order> filteredOrders = getOrderByCafeName(orders, cafeName);
    List<List<double>> turnOverAndProfitList = [];

    for (DateTime date in getAllDaysOfMonth(year, month)) {
      List<Order> monthOrders = getOrderOverAPeriod(filteredOrders, date, date);
      double turnOver = 0.0;
      for (Order order in monthOrders) {
        turnOver += order.totalPrice;
      }
      double profit = turnOver * 0.9;

      turnOverAndProfitList.add([turnOver, profit]);
    }

    return turnOverAndProfitList;
  }

  List<Order> getOrderByCafeName(List<Order> orders, String cafeName) {
    List<Order> filteredOrders = [];
    for (Order order in orders) {
      if (order.cafeName == cafeName) {
        filteredOrders.add(order);
      }
    }
    return filteredOrders;
  }

  static bool isFallSemester() {
    DateTime startfallSemester = DateTime(DateTime.now().year, 9, 15);
    DateTime endfallSemester = DateTime(DateTime.now().year, 12, 31);
    if ((DateTime.now()).isAfter(startfallSemester) &&
        DateTime.now().isBefore(endfallSemester)) {
      return true;
    }
    return false;
  }

  static bool isWinterSemester() {
    DateTime startWinterSemester = DateTime(DateTime.now().year, 1, 15);
    DateTime endWinterSemester = DateTime(DateTime.now().year, 4, 31);
    if ((DateTime.now()).isAfter(startWinterSemester) &&
        DateTime.now().isBefore(endWinterSemester)) {
      return true;
    }
    return false;
  }

  List<Order> getOrderInFallSemester(List<Order> orders) {
    DateTime startfallSemester = DateTime(DateTime.now().year, 9, 15);
    DateTime endfallSemester = DateTime(DateTime.now().year, 12, 31);
    return getOrderOverAPeriod(orders, startfallSemester, endfallSemester);
  }

  List<Order> getOrderInWinterSemester(List<Order> orders) {
    DateTime startWinterSemester = DateTime(DateTime.now().year, 1, 15);
    DateTime endWinterSemester = DateTime(DateTime.now().year, 4, 31);
    return getOrderOverAPeriod(orders, startWinterSemester, endWinterSemester);
  }

  List<Order> getOrderOverAPeriod(
      List<Order> orders, DateTime startDate, DateTime endDate) {
    List<Order> filteredOrders = [];
    for (Order order in orders) {
      if ((order.createdAt).isAfter(startDate) &&
          (order.createdAt).isBefore(endDate)) {
        filteredOrders.add(order);
      }
    }
    return filteredOrders;
  }
}

List<List<DateTime>> getStartAndEndDatesOfMonths(int year) {
  List<List<DateTime>> months = [];

  for (int month = 1; month <= 12; month++) {
    DateTime firstDayOfMonth = DateTime(year, month, 1);
    DateTime lastDayOfMonth = (month < 12)
        ? DateTime(year, month + 1, 1).subtract(const Duration(days: 1))
        : DateTime(year + 1, 1, 1).subtract(const Duration(days: 1));

    months.add([firstDayOfMonth, lastDayOfMonth]);
  }

  return months;
}

List<DateTime> getAllDaysOfMonth(int year, int month) {
  List<DateTime> days = [];
  int daysInMonth =
      DateTime(year, month + 1, 1).subtract(const Duration(days: 1)).day;

  for (int day = 1; day <= daysInMonth; day++) {
    days.add(DateTime(year, month, day));
  }

  return days;
}
