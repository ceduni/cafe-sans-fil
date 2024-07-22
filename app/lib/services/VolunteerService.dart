import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:app/modeles/Volunteer.dart';

class Volunteerservice {
  final String baseUrl =
      "http://Localhost:3000/api/v1/cafes/Tore et fraction/volunteer";

  Volunteerservice({dynamic});

  Future<List<Volunteer>> fetchVolunteers() async {
    var url = Uri.parse(baseUrl);
    var response = await http.get(url);

    if (response.statusCode == 200) {
      var jsonData = json.decode(response.body);

      if (jsonData['cafes_Vonlunteer'] != null) {
        print("in json volunteers tab");
        List<dynamic> volunteersJson = jsonData['cafes_Vonlunteer'];
        List<Volunteer> volunteers =
            volunteersJson.map((json) => Volunteer.fromJson(json)).toList();
        return volunteers;
      } else {
        throw Exception('Volunteers data is not available');
      }
    } else {
      throw Exception('Failed to load volunteers from $baseUrl');
    }
  }
}

void main() async {
  var volunteerService = new Volunteerservice();
  List<Volunteer> volunteers = await volunteerService.fetchVolunteers();
  for (var volunteer in volunteers) {
    print(volunteer.firstName);
  }
}
