import 'package:app/config.dart';
import 'package:app/modeles/Volunteer.dart';
import 'package:app/services/volunteerService.dart';
import 'package:flutter/material.dart';

class VolunteerProvider with ChangeNotifier {
  List<Volunteer> _Volunteers = [];
  String cafeName = Config.cafeName;
  bool _isLoading = false;
  String? _errorMessage;

  get Volunteers => _Volunteers;
  get isLoading => _isLoading;
  get errorMessage => _errorMessage;
  bool get hasError => _errorMessage != null && _errorMessage!.isNotEmpty;

  VolunteerProvider() {
    fetchVolunteer();
  }

  Future<void> fetchVolunteer() async {
    _isLoading = true;
    try {
      _Volunteers = await VolunteerService().fetchVolunteers();
      _isLoading = false;
    } catch (e) {
      // Handle error
      _errorMessage = e.toString();
      _isLoading = false;
      print(e);
    }

    notifyListeners();
  }
}
