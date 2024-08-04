import 'package:app/modeles/Stock.dart';

import 'OrderItem.dart';

class Order {
  final String orderId;
  final int orderNumber;
  final String cafeName;
  final String cafeSlug;
  final String cafeImageUrl;
  final String userUsername;
  final List<OrderItem> items;
  final double totalPrice;
  final String status;
  final DateTime createdAt;
  final DateTime updatedAt;

  Order({
    required this.orderId,
    required this.orderNumber,
    required this.cafeName,
    required this.cafeSlug,
    required this.cafeImageUrl,
    required this.userUsername,
    required this.items,
    required this.totalPrice,
    required this.status,
    required this.createdAt,
    required this.updatedAt,
  });

  factory Order.fromJson(Map<String, dynamic> json) {
    var itemsFromJson = json['items'] as List;
    List<OrderItem> itemsList =
        itemsFromJson.map((i) => OrderItem.fromJson(i)).toList();

    return Order(
      orderId: json['order_id'],
      orderNumber: json['order_number'],
      cafeName: json['cafe_name'],
      cafeSlug: json['cafe_slug'],
      cafeImageUrl: json['cafe_image_url'],
      userUsername: json['user_username'],
      items: itemsList,
      totalPrice: (json['total_price'] as num).toDouble(),
      status: json['status'],
      createdAt: DateTime.parse(json['created_at']),
      updatedAt: DateTime.parse(json['updated_at']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'order_id': orderId,
      'order_number': orderNumber,
      'cafe_name': cafeName,
      'cafe_slug': cafeSlug,
      'cafe_image_url': cafeImageUrl,
      'user_username': userUsername,
      'items': items.map((item) => item.toJson()).toList(),
      'total_price': totalPrice,
      'status': status,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt.toIso8601String(),
    };
  }

/*
  static double turnOver(List<Order> orders,
      {String startDate = "date", String endDate = "Date"}) {
    print("IN TURNOVER");
    double sum = 0;
    if (startDate == "date" || endDate == "Date") {
      print("IN IF");
      DateTime startfallSemester = DateTime(DateTime.now().year, 9, 15);
      DateTime endfallSemester = DateTime(DateTime.now().year, 12, 31);

      DateTime startWinterSemester = DateTime(DateTime.now().year, 1, 15);
      DateTime endWinterSemester = DateTime(DateTime.now().year, 4, 31);

      for (Order o in orders) {
        if (isDateInRange(o.createdAt, startfallSemester, DateTime.now()) ||
            isDateInRange(o.createdAt, startWinterSemester, DateTime.now())) {
          sum += o.totalPrice;
        }
      }
    } else {
      print("IN ELSE");
      DateTime start = parseDate(startDate);
      DateTime end = parseDate(endDate);
      for (Order o in orders) {
        if (isDateInRange(o.createdAt, start, end)) {
          sum += o.totalPrice;
        }
      }
    }
    return double.parse(sum.toStringAsFixed(4));
  }
*/
  /// this function return a turnover of a given month
  /// given a list of orders and a month
  static double turnOverDate(List<Order> orders, int month) {
    double sum = 0;
    for (Order o in orders) {
      if (o.createdAt.month == month) {
        sum += o.totalPrice;
      }
    }
    return sum;
  }

  static int numOfOrder(List<Order> orders) {
    return orders.length;
  }

  static bool isDateInRange(
      DateTime date, DateTime startDate, DateTime endDate) {
    return date.isAfter(startDate) && date.isBefore(endDate) ||
        date.isAtSameMomentAs(startDate) ||
        date.isAtSameMomentAs(endDate);
  }

  static DateTime parseDate(String dateString) {
    List<String> parts = dateString.split('/');
    int day = int.parse(parts[0]);
    int month = int.parse(parts[1]);
    int year = int.parse(parts[2]);

    return DateTime(year, month, day);
  }

  static double calculateProfit(double turnOver) {
    return turnOver - 500;
  }

  static Map<String, dynamic> revenueByCategory(
      List<Order> orders, List<Stock> stock) {
    Map<String, dynamic> revenue = {};
    for (Order o in orders) {
      for (OrderItem item in o.items) {
        for (Stock s in stock) {
          if (item.itemSlug == s.itemName) {
            if (revenue.containsKey(s.category)) {
              revenue[s.category] += item.itemPrice;
            } else {
              revenue[s.category] = item.itemPrice;
            }
          }
        }
      }
    }
    return revenue;
  }

  @override
  String toString() {
    return '''
    {
      "order_id": "$orderId",
      "order_number": $orderNumber,
      "cafe_name": "$cafeName",
      "cafe_slug": "$cafeSlug",
      "cafe_image_url": "$cafeImageUrl",
      "user_username": "$userUsername",
      "items": ${items.map((item) => item.toString()).toList()},
      "total_price": $totalPrice,
      "status": "$status",
      "created_at": "$createdAt",
      "updated_at": "$updatedAt"
    }
    ''';
  }
}
