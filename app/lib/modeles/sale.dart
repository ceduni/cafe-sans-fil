



class Sale{
  final String id;
  final String name;
  final String category;
  final int quantity;
  final DateTime date;
  final int v ;

  Sale({
    required this.id,
    required this.name,
    required this.category,
    required this.quantity,
    required this.date,
    required this.v

  });

  String get formattedDAte => "${date.day}/${date.month}/${date.year}";
  double get totalRevenue => 20.0 * quantity;

  factory Sale.fromJson(Map<String,dynamic> json){
    return Sale(
      id:json['id'],
      name: json['name'],
      category: json['name'],
      quantity: json['quantity'],
      date:DateTime.parse(json['date']),
      v: json['__v']

    );

  }


  Map<String, dynamic> toJson() => {
        'id': id,
        'name':name,
        'category': category,
        'quantity': quantity,
        'date': date.toIso8601String(),
        'v': v,
  };


  
}