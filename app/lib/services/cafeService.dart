import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:app/config.dart';
import 'package:app/modeles/Cafe.dart';

class CafeService {
  /*
  Future<List<Cafe>> fetchCafes() async {
    var url = Uri.parse('${Config.baseUrl}/cafes');
    var response = await http.get(url).timeout(const Duration(seconds: 25));

    if (response.statusCode == 200) {
      var jsonData = json.decode(response.body);

      if (jsonData['Cafes'] != null) {
        print("Cafe Service : json fetching");
        List<dynamic> cafesJson = jsonData['Cafes'];
        List<Cafe> cafes =
            cafesJson.map((json) => Cafe.fromJson(json)).toList();
        return cafes;
      } else {
        throw Exception('Cafes data is not available');
      }
    } else {
      throw Exception('Failed to load cafes from ${Config.baseUrl}');
    }
  }*/

  Future<Cafe> fetchCafeByName(String cafeName) async {
    var url = Uri.parse('${Config.baseUrl}/cafes/$cafeName');
    var response = await http.get(url).timeout(const Duration(seconds: 25));

    print("response : ${response.statusCode}");

    if (response.statusCode == 200) {
      var jsonData = json.decode(response.body);

      print("JSON : $jsonData");

      if (jsonData['cafe'] != null) {
        print("Cafe Service : json fetching cafe by cafeName");

        print("jsondata cafe: ${jsonData['cafe']}");

        // Pas besoin de mapper, car c'est déjà un seul objet
        Cafe cafe = Cafe.fromJson(jsonData['cafe']);
        print("cafe : $cafe");
        return cafe;
      } else {
        throw Exception('Cafe data is not available for cafeName $cafeName');
      }
    } else {
      throw Exception(
          'Failed to load cafe for name $cafeName from ${Config.baseUrl}');
    }
  }
}
