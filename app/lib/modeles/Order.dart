import 'OrderItem.dart';



class Order{
  final String cafeSlug;
  final DateTime createdAt;
  final List<OrderItem> items;
  final String orderId;
  final int orderNumber;
  final String status;
  final double totalPrice;
  final DateTime updatedAt;
  final String userUsername;

  Order({
    required this.cafeSlug,
    required this.createdAt,
    required this.items,
    required this.orderId,
    required this.orderNumber,
    required this.status,
    required this.totalPrice,
    required this.updatedAt,
    required this.userUsername,
    
  });

  factory Order.fromJson(Map<String, dynamic> json) {
    var itemsFromJson = json['items'] as List;
    List<OrderItem> itemsList = itemsFromJson.map((i) => OrderItem.fromJson(i)).toList();

    return Order(
      cafeSlug: json['cafe_slug'],
      createdAt: DateTime.parse(json['created_at']),
      items: itemsList,
      orderId: json['order_id'],
      orderNumber: json['order_number'],
      status: json['status'],
      totalPrice: json['total_price'].toDouble(),
      updatedAt: DateTime.parse(json['updated_at']),
      userUsername: json['user_username'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'cafe_slug': cafeSlug,
      'created_at': createdAt.toIso8601String(),
      'items': items.map((item) => item.toJson()).toList(),
      'order_id': orderId,
      'order_number': orderNumber,
      'status': status,
      'total_price': totalPrice,
      'updated_at': updatedAt.toIso8601String(),
      'user_username': userUsername,
    };
  }


  static double  turnOver(List<Order> orders, {String startDate = "date", String endDate = "Date"}){
    double sum = 0;
    if(startDate == "date" || endDate == "Date" ){
        for( Order o in orders){
        sum += o.totalPrice;
      }
    }
    else {
      DateTime start = parseDate(startDate);
      DateTime end = parseDate(endDate);
       for( Order o in orders){
        if(isDateInRange(o.createdAt, start, end)){
          sum += o.totalPrice;
        }
      }

    }
    return double.parse(sum.toStringAsFixed(4));
  }
/// this function return a turnover of a given month
/// given a list of orders and a month
  static double turnOverDate(List<Order> orders, int month){
    double sum = 0;
    for( Order o in orders){
        if(o.createdAt.month == month){
          sum += o.totalPrice;

        }
        
      }
    return  sum;

  }

  static int numOfOrder(List<Order> orders){
    return orders.length;
  }

  static bool isDateInRange(DateTime date, DateTime startDate, DateTime endDate) {
      return date.isAfter(startDate) && date.isBefore(endDate) || date.isAtSameMomentAs(startDate) || date.isAtSameMomentAs(endDate);
  }
  
  static DateTime parseDate(String dateString) {
    List<String> parts = dateString.split('/');
    int day = int.parse(parts[0]);
    int month = int.parse(parts[1]);
    int year = int.parse(parts[2]);

    return DateTime(year, month, day);
  }

  static double calculateProfit(double turnOver){
    return turnOver - 500 ;
  }

  
 @override
  String toString() {
    return '''
    {
      "cafe_slug": "$cafeSlug",
      "created_at": "${createdAt.toIso8601String()}",
      "items": ${items.map((item) => item.toString()).toList()},
      "order_id": "$orderId",
      "order_number": $orderNumber,
      "status": "$status",
      "total_price": $totalPrice,
      "updated_at": "${updatedAt.toIso8601String()}",
      "user_username": "$userUsername"
    }
    ''';
  }

  
}