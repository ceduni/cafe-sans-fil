import 'dart:convert';

class Volunteer {
  String? id;
  String userId;
  String email;
  String matricule;
  String username;
  String hashedPassword;
  String firstName;
  String lastName;
  String photoUrl;
  int failedLoginAttempts;
  DateTime? lastFailedLoginAttempt;
  DateTime? lockoutUntil;
  bool isActive;

  Volunteer({
    this.id,
    required this.userId,
    required this.email,
    required this.matricule,
    required this.username,
    required this.hashedPassword,
    required this.firstName,
    required this.lastName,
    required this.photoUrl,
    required this.failedLoginAttempts,
    this.lastFailedLoginAttempt,
    this.lockoutUntil,
    required this.isActive,
  });

  factory Volunteer.fromJson(Map<String, dynamic> json) {
    return Volunteer(
      id: json['_id'],
      userId: json['user_id'],
      email: json['email'],
      matricule: json['matricule'],
      username: json['username'],
      hashedPassword: json['hashed_password'],
      firstName: json['first_name'],
      lastName: json['last_name'],
      photoUrl: json['photo_url'],
      failedLoginAttempts: json['failed_login_attempts'],
      lastFailedLoginAttempt: json['last_failed_login_attempt'] != null
          ? DateTime.parse(json['last_failed_login_attempt'])
          : null,
      lockoutUntil: json['lockout_until'] != null
          ? DateTime.parse(json['lockout_until'])
          : null,
      isActive: json['is_active'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      '_id': id,
      'user_id': userId,
      'email': email,
      'matricule': matricule,
      'username': username,
      'hashed_password': hashedPassword,
      'first_name': firstName,
      'last_name': lastName,
      'photo_url': photoUrl,
      'failed_login_attempts': failedLoginAttempts,
      'last_failed_login_attempt': lastFailedLoginAttempt?.toIso8601String(),
      'lockout_until': lockoutUntil?.toIso8601String(),
      'is_active': isActive,
    };
  }

  static List<Volunteer> fromJsonList(String jsonString) {
    final List<dynamic> jsonData = json.decode(jsonString);
    return jsonData.map((jsonItem) => Volunteer.fromJson(jsonItem)).toList();
  }

  static String toJsonList(List<Volunteer> volunteers) {
    final List<Map<String, dynamic>> jsonData =
        volunteers.map((volunteer) => volunteer.toJson()).toList();
    return json.encode(jsonData);
  }
}
