import 'OrderItemOption.dart';

class OrderItem {
  final String itemName;
  final String itemSlug;
  final String itemImageUrl;
  final double itemPrice;
  final int quantity;
  final List<OrderItemOption> options;
  

  OrderItem({

    required this.itemName,
    required this.itemSlug,
    required this.itemImageUrl,
    required this.itemPrice,
    required this.quantity,
    required this.options,
  });

  factory OrderItem.fromJson(Map<String, dynamic> json) {
    print(json);
    var optionsFromJson = json['options'] as List;
    List<OrderItemOption> optionsList = optionsFromJson
        .map((option) => OrderItemOption.fromJson(option))
        .toList();
      print(" this is what i wanted ${json['item_name']}");
    return OrderItem(
      
      itemName: json['item_name'],
      itemSlug: json['item_slug'],
      itemImageUrl: json['item_image_url'],
      itemPrice: json['item_price'],
      quantity: json['quantity'],
      options: optionsList,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'item_name': itemName,
      'item_slug': itemSlug,
      'item_image_url': itemImageUrl,
      'item_price': itemPrice,
      'quantity': quantity,
      'options': options.map((option) => option.toJson()).toList(),
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
