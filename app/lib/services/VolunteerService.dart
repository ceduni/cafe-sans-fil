import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:app/modeles/Volunteer.dart';

class VolunteerService {
  final String baseUrl =
      "http://10.51.252.166:3000/api/v1/cafes/Tore et fraction/volunteer";

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
}
