import 'dart:convert';
import 'package:http/http.dart' as http;
import '../modeles/sale.dart';

class ProductService {
  final String baseUrl;

  ProductService({required this.baseUrl});
 
  Future<List<Sale>> fetchSales() async {
     

    var url = Uri.parse(baseUrl);
    var response = await http.get(url);
    print("wait for the answer");
    
    if(response.statusCode == 200){
      print("in here");
      var jsonData = json.decode(response.body);
      print("this is thr salesJson: ${json.decode(response.body)}");
      if(jsonData['Sales']!=null){
        print("in json sales tab");
        List<dynamic> salesJson = jsonData['Sales'];
        return salesJson.map((json) => Sale.fromJson(json)).toList();
      }
      else{
        throw Exception('Sales data is not available');
      }
    }
    else{
      throw Exception('Failed to load sales from $baseUrl');
    }
  }


}