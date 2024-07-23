import 'dart:convert';

class Stock {
  final String id;
  final String itemName;
  final String category;
  int quantity;

  Stock({
    required this.id,
    required this.itemName,
    required this.category,
    required this.quantity,
  });

  factory Stock.fromJson(Map<String, dynamic> json) {
    print("converting json to stock");
    return Stock(
      id: json['_id'],
      itemName: json['item_name'],
      category: json['category'],
      quantity: json['quantity'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'item_name': itemName,
      'category': category,
      'quantity': quantity,
    };
  }

  static List<Stock> lowQuantity(List<Stock> stocks) {
    List<Stock> lowStocks = [];
    for (Stock stock in stocks) {
      if (stock.quantity < 10) {
        // Example condition for low stock
        lowStocks.add(stock);
      }
    }
    return lowStocks;
  }

  @override
  String toString() {
    final jsonMap = toJson();
    return const JsonEncoder.withIndent('  ').convert(jsonMap);
  }
}
