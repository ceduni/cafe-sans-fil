

class OrderItemOption {

  final double fee;
  final String type;
  final String value;

  OrderItemOption({
    required this.fee,
    required this.type,
    required this.value
  });

  factory OrderItemOption.fromJson(Map<String, dynamic> json){
    return OrderItemOption(
      fee: json['fee'].toDouble(),
      type: json['type'], 
      value: json['value']
    );

  }

  Map<String,dynamic> toJson(){
    return {
      'fee':fee,
      'type':type,
      'value':value
    };
  }

    @override
  String toString() {
    return '''
    {
      "fee": $fee,
      "type": "$type",
      "value": "$value"
    }
    ''';
  }


}