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


  static double  turnOver(List<Order> orders){
    double sum = 0;
    for( Order o in orders){
      sum += o.totalPrice;
    }
    return double.parse(sum.toStringAsFixed(4));
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