import 'dart:convert';
import 'package:app/config.dart';
import 'package:http/http.dart' as http;
import 'package:app/modeles/Volunteer.dart';

class VolunteerService {
  final String baseUrl = "${Config.baseUrl}/cafes/${Config.cafeName}/volunteer";

  VolunteerService({dynamic});

  Future<List<Volunteer>> fetchVolunteers() async {
    var url = Uri.parse(baseUrl);
    var response = await http.get(url);

    if (response.statusCode == 200) {
      var jsonData = json.decode(response.body);

      if (jsonData['volunteers'] != null) {
        print("in json volunteers tab");

        List<dynamic> volunteersJson = jsonData['volunteers'];

        List<Volunteer> volunteers =
            volunteersJson.map((json) => Volunteer.fromJson(json)).toList();

        print(volunteers);

        return volunteers;
      } else {
        throw Exception('Volunteers data is not available');
      }
    } else {
      throw Exception('Failed to load volunteers from $baseUrl');
    }
  }

  Future<String> postVolunteer(
      String cafeName, String matricule, String role) async {
    String message = "";
    final url = Uri.parse('${Config.baseUrl}/cafes/$cafeName/volunteer');
    final headers = {"Content-Type": "application/json"};
    final body = jsonEncode({"userName": matricule, "Role": role});
    final response = await http.post(url, headers: headers, body: body);
    if (response.statusCode == 200) {
      Map<String, dynamic> responseJson = jsonDecode(response.body);
      print(responseJson);
      message = responseJson['message'];
      message = 'Success: $message';
    } else {
      message = 'Failed: ${response.statusCode}';
    }
    return message;
  }
}
