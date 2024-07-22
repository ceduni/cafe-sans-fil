import 'OrderItemOption.dart';

class OrderItem {
  final double itemPrice;
  final String itemSlug;
  final List<OrderItemOption> options;
  final int quantity;

  OrderItem(
      {required this.itemPrice,
      required this.itemSlug,
      required this.options,
      required this.quantity});

  factory OrderItem.fromJson(Map<String, dynamic> json) {
    var optionsFromJson = json['options'] as List;
    List<OrderItemOption> optionsList = optionsFromJson
        .map((option) => OrderItemOption.fromJson(option))
        .toList();

    return OrderItem(
        itemPrice: (json['item_price'] as num).toDouble(),
        itemSlug: json['item_slug'],
        options: optionsList,
        quantity: json['quantity']);
  }

  Map<String, dynamic> toJson() {
    return {
      'item_price': itemPrice,
      'item_slug': itemSlug,
      'options': options.map((option) => option.toJson()).toList(),
      'quantity': quantity
    };
  }

  @override
  String toString() {
    return '''
    {
      "item_price": $itemPrice,
      "item_slug": "$itemSlug",
      "options": ${options.map((option) => option.toString()).toList()},
      "quantity": $quantity
    }
    ''';
  }
}
